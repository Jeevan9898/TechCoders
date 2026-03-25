"""
Base Agent class for the Multi-Agent RFP System.

This module provides the foundational framework that all specialized agents
inherit from, including common functionality for messaging, logging,
error handling, and performance monitoring.
"""

import asyncio
import json
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
import structlog

from core.redis_client import MessageQueue, CacheManager
from core.database import AsyncSessionLocal
from models.audit_models import AgentAction, ActionTypeEnum, AgentTypeEnum
from models.rfp_models import RFPDocument, RFPStatusEnum


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the RFP system.
    
    Provides common functionality including:
    - Message queue communication
    - Database session management
    - Audit logging and performance tracking
    - Error handling and recovery
    - Configuration management
    """
    
    def __init__(self, agent_type: AgentTypeEnum, instance_id: Optional[str] = None):
        """
        Initialize the base agent.
        
        Args:
            agent_type: The type of agent (from AgentTypeEnum)
            instance_id: Unique identifier for this agent instance
        """
        self.agent_type = agent_type
        self.instance_id = instance_id or str(uuid.uuid4())
        self.version = "1.0.0"
        self.is_running = False
        self.is_healthy = True
        
        # Initialize logging
        self.logger = structlog.get_logger(
            agent_type=agent_type.value,
            instance_id=self.instance_id
        )
        
        # Initialize messaging and caching
        self.message_queue = MessageQueue()
        self.cache_manager = CacheManager()
        
        # Performance tracking
        self.start_time = None
        self.processed_count = 0
        self.error_count = 0
        self.last_activity = None
        
        # Configuration (can be overridden by subclasses)
        self.config = {
            "max_concurrent_tasks": 5,
            "task_timeout": 300,  # 5 minutes
            "retry_attempts": 3,
            "retry_delay": 5,  # seconds
            "health_check_interval": 60,  # seconds
        }
        
        self.logger.info("Agent initialized", version=self.version)
    
    async def start(self) -> None:
        """
        Start the agent and begin processing tasks.
        
        This method sets up the agent's main processing loop and
        starts listening for messages from the message queue.
        """
        if self.is_running:
            self.logger.warning("Agent is already running")
            return
        
        self.is_running = True
        self.start_time = datetime.utcnow()
        
        self.logger.info("Starting agent")
        
        try:
            # Start the main processing loop
            await self._main_loop()
            
        except Exception as e:
            self.logger.error("Agent startup failed", error=str(e))
            self.is_running = False
            self.is_healthy = False
            raise
    
    async def stop(self) -> None:
        """
        Stop the agent gracefully.
        
        Completes any ongoing tasks and shuts down the agent cleanly.
        """
        self.logger.info("Stopping agent")
        self.is_running = False
        
        # Allow time for current tasks to complete
        await asyncio.sleep(1)
        
        self.logger.info("Agent stopped", 
                        processed_count=self.processed_count,
                        error_count=self.error_count)
    
    async def _main_loop(self) -> None:
        """
        Main processing loop for the agent.
        
        Continuously listens for messages and processes tasks.
        """
        queue_name = f"{self.agent_type.value}_tasks"
        
        while self.is_running:
            try:
                # Get task from queue with timeout
                task_data = await self.message_queue.get_task_from_queue(
                    queue_name, 
                    timeout=10
                )
                
                if task_data:
                    await self._process_task(task_data)
                    self.last_activity = datetime.utcnow()
                
                # Periodic health check
                if self._should_run_health_check():
                    await self._health_check()
                
            except Exception as e:
                self.logger.error("Error in main loop", error=str(e))
                self.error_count += 1
                await asyncio.sleep(self.config["retry_delay"])
    
    async def _process_task(self, task_data: Dict[str, Any]) -> None:
        """
        Process a single task with error handling and logging.
        
        Args:
            task_data: Task information from the message queue
        """
        task_id = task_data.get("id", "unknown")
        action_type = task_data.get("action_type", "unknown")
        
        start_time = time.time()
        
        try:
            self.logger.info("Processing task", task_id=task_id, action_type=action_type)
            
            # Log the start of the action
            await self._log_agent_action(
                action_type=ActionTypeEnum(action_type) if action_type in ActionTypeEnum.__members__ else ActionTypeEnum.WORKFLOW_STARTED,
                action_name=f"process_{action_type}",
                input_data=task_data,
                start_time=datetime.utcnow()
            )
            
            # Process the task (implemented by subclasses)
            result = await self.process_task(task_data)
            
            # Calculate processing time
            duration = time.time() - start_time
            
            # Log successful completion
            await self._log_agent_action(
                action_type=ActionTypeEnum(action_type) if action_type in ActionTypeEnum.__members__ else ActionTypeEnum.WORKFLOW_COMPLETED,
                action_name=f"process_{action_type}",
                input_data=task_data,
                output_data=result,
                start_time=datetime.utcnow() - timedelta(seconds=duration),
                end_time=datetime.utcnow(),
                success=True,
                duration_seconds=duration
            )
            
            self.processed_count += 1
            self.logger.info("Task completed", 
                           task_id=task_id, 
                           duration_seconds=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            self.error_count += 1
            
            # Log the error
            await self._log_agent_action(
                action_type=ActionTypeEnum.ERROR_OCCURRED,
                action_name=f"process_{action_type}",
                input_data=task_data,
                start_time=datetime.utcnow() - timedelta(seconds=duration),
                end_time=datetime.utcnow(),
                success=False,
                duration_seconds=duration,
                error_details={"error": str(e), "type": type(e).__name__}
            )
            
            self.logger.error("Task processing failed", 
                            task_id=task_id, 
                            error=str(e),
                            duration_seconds=duration)
            
            # Optionally retry the task
            if task_data.get("retry_count", 0) < self.config["retry_attempts"]:
                await self._retry_task(task_data)
    
    async def _retry_task(self, task_data: Dict[str, Any]) -> None:
        """
        Retry a failed task after a delay.
        
        Args:
            task_data: Original task data
        """
        retry_count = task_data.get("retry_count", 0) + 1
        task_data["retry_count"] = retry_count
        
        self.logger.info("Retrying task", 
                        task_id=task_data.get("id"),
                        retry_count=retry_count)
        
        # Add delay before retry
        await asyncio.sleep(self.config["retry_delay"] * retry_count)
        
        # Re-queue the task
        queue_name = f"{self.agent_type.value}_tasks"
        await self.message_queue.add_task_to_queue(queue_name, task_data)
    
    async def _log_agent_action(self, **kwargs) -> None:
        """
        Log an agent action to the database.
        
        Args:
            **kwargs: Action data to log
        """
        try:
            async with AsyncSessionLocal() as db:
                action = AgentAction(
                    agent_type=self.agent_type,
                    agent_instance_id=self.instance_id,
                    agent_version=self.version,
                    **kwargs
                )
                db.add(action)
                await db.commit()
                
        except Exception as e:
            self.logger.error("Failed to log agent action", error=str(e))
    
    def _should_run_health_check(self) -> bool:
        """
        Determine if it's time to run a health check.
        
        Returns:
            bool: True if health check should be run
        """
        if not hasattr(self, '_last_health_check'):
            self._last_health_check = datetime.utcnow()
            return True
        
        time_since_check = (datetime.utcnow() - self._last_health_check).total_seconds()
        return time_since_check >= self.config["health_check_interval"]
    
    async def _health_check(self) -> None:
        """
        Perform a health check and update agent status.
        """
        try:
            # Check database connectivity
            async with AsyncSessionLocal() as db:
                await db.execute("SELECT 1")
            
            # Check Redis connectivity
            await self.message_queue.redis.ping()
            
            # Update health status
            self.is_healthy = True
            self._last_health_check = datetime.utcnow()
            
            # Cache health status
            await self.cache_manager.set_cache(
                f"agent_health:{self.agent_type.value}:{self.instance_id}",
                {
                    "healthy": True,
                    "last_check": datetime.utcnow().isoformat(),
                    "processed_count": self.processed_count,
                    "error_count": self.error_count,
                    "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
                },
                ttl=120  # 2 minutes
            )
            
        except Exception as e:
            self.is_healthy = False
            self.logger.error("Health check failed", error=str(e))
    
    async def send_message(self, channel: str, message: Dict[str, Any]) -> None:
        """
        Send a message to other agents via Redis pub/sub.
        
        Args:
            channel: Channel name to publish to
            message: Message data to send
        """
        try:
            message["source_agent"] = self.agent_type.value
            message["source_instance"] = self.instance_id
            message["timestamp"] = datetime.utcnow().isoformat()
            
            await self.message_queue.publish_message(channel, message)
            
        except Exception as e:
            self.logger.error("Failed to send message", channel=channel, error=str(e))
    
    async def get_rfp_by_id(self, rfp_id: str) -> Optional[RFPDocument]:
        """
        Retrieve an RFP document from the database.
        
        Args:
            rfp_id: UUID string of the RFP
            
        Returns:
            RFPDocument if found, None otherwise
        """
        try:
            async with AsyncSessionLocal() as db:
                from sqlalchemy import select
                query = select(RFPDocument).where(RFPDocument.id == rfp_id)
                result = await db.execute(query)
                return result.scalar_one_or_none()
                
        except Exception as e:
            self.logger.error("Failed to retrieve RFP", rfp_id=rfp_id, error=str(e))
            return None
    
    async def update_rfp_status(self, rfp_id: str, status: RFPStatusEnum) -> bool:
        """
        Update the status of an RFP document.
        
        Args:
            rfp_id: UUID string of the RFP
            status: New status to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with AsyncSessionLocal() as db:
                from sqlalchemy import select
                query = select(RFPDocument).where(RFPDocument.id == rfp_id)
                result = await db.execute(query)
                rfp = result.scalar_one_or_none()
                
                if rfp:
                    rfp.status = status
                    await db.commit()
                    
                    self.logger.info("RFP status updated", 
                                   rfp_id=rfp_id, 
                                   new_status=status.value)
                    return True
                    
                return False
                
        except Exception as e:
            self.logger.error("Failed to update RFP status", 
                            rfp_id=rfp_id, 
                            status=status.value, 
                            error=str(e))
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dict containing agent status information
        """
        uptime = (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            "agent_type": self.agent_type.value,
            "instance_id": self.instance_id,
            "version": self.version,
            "is_running": self.is_running,
            "is_healthy": self.is_healthy,
            "uptime_seconds": uptime,
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "config": self.config
        }
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a specific task. Must be implemented by subclasses.
        
        Args:
            task_data: Task information and parameters
            
        Returns:
            Dict containing the results of processing
        """
        pass