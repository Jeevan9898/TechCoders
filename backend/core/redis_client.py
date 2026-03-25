"""
Redis client configuration and utilities for the Multi-Agent RFP System.

This module provides Redis connection management, message queue operations,
and caching utilities for inter-agent communication and data storage.
"""

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

import json
import structlog
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta

from core.config import get_redis_url, settings

logger = structlog.get_logger(__name__)

# Global Redis connection pool
redis_pool: Optional[redis.ConnectionPool] = None
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """
    Initialize Redis connection pool and client.
    
    Sets up the global Redis connection that will be used throughout
    the application for message queuing and caching operations.
    Falls back to in-memory implementation if Redis is not available.
    """
    global redis_pool, redis_client
    
    try:
        redis_url = get_redis_url()
        
        if redis_url == "memory://" or not REDIS_AVAILABLE:
            # Use in-memory fallback
            from core.memory_redis import get_memory_redis
            redis_client = get_memory_redis()
            logger.info("Using in-memory Redis fallback for demo")
        else:
            # Create connection pool
            redis_pool = redis.ConnectionPool.from_url(
                redis_url,
                password=settings.REDIS_PASSWORD,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={},
            )
            
            # Create Redis client
            redis_client = redis.Redis(connection_pool=redis_pool)
            
            # Test connection
            await redis_client.ping()
            
            logger.info("Redis connection established successfully")
        
    except Exception as e:
        logger.warning("Redis not available, using in-memory fallback", error=str(e))
        from core.memory_redis import get_memory_redis
        redis_client = get_memory_redis()


async def close_redis() -> None:
    """
    Close Redis connections and cleanup resources.
    
    Should be called during application shutdown to properly close
    all Redis connections.
    """
    global redis_client, redis_pool
    
    try:
        if redis_client:
            await redis_client.close()
        if redis_pool:
            await redis_pool.disconnect()
            
        logger.info("Redis connections closed")
        
    except Exception as e:
        logger.error("Error closing Redis connections", error=str(e))


def get_redis() -> redis.Redis:
    """
    Get the Redis client instance.
    
    Returns:
        redis.Redis: The global Redis client
        
    Raises:
        RuntimeError: If Redis is not initialized
    """
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client


class MessageQueue:
    """
    Redis-based message queue for inter-agent communication.
    
    Provides publish/subscribe functionality and task queue operations
    for coordinating work between the different AI agents.
    """
    
    def __init__(self):
        self.redis = get_redis()
    
    async def publish_message(self, channel: str, message: Dict[str, Any]) -> None:
        """
        Publish a message to a Redis channel.
        
        Args:
            channel: The channel name to publish to
            message: The message data to publish
        """
        try:
            message_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": message
            }
            
            await self.redis.publish(
                channel, 
                json.dumps(message_data, default=str)
            )
            
            logger.info("Message published", channel=channel, message_id=message.get("id"))
            
        except Exception as e:
            logger.error("Failed to publish message", channel=channel, error=str(e))
            raise
    
    async def subscribe_to_channel(self, channel: str):
        """
        Subscribe to a Redis channel for receiving messages.
        
        Args:
            channel: The channel name to subscribe to
            
        Yields:
            Dict: Parsed message data from the channel
        """
        try:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(channel)
            
            logger.info("Subscribed to channel", channel=channel)
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        yield data
                    except json.JSONDecodeError as e:
                        logger.error("Failed to parse message", error=str(e))
                        
        except Exception as e:
            logger.error("Subscription error", channel=channel, error=str(e))
            raise
    
    async def add_task_to_queue(self, queue_name: str, task_data: Dict[str, Any]) -> None:
        """
        Add a task to a Redis list-based queue.
        
        Args:
            queue_name: Name of the task queue
            task_data: Task data to add to the queue
        """
        try:
            task_json = json.dumps(task_data, default=str)
            await self.redis.lpush(queue_name, task_json)
            
            logger.info("Task added to queue", queue=queue_name, task_id=task_data.get("id"))
            
        except Exception as e:
            logger.error("Failed to add task to queue", queue=queue_name, error=str(e))
            raise
    
    async def get_task_from_queue(self, queue_name: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Get a task from a Redis queue with blocking pop.
        
        Args:
            queue_name: Name of the task queue
            timeout: Timeout in seconds for blocking operation
            
        Returns:
            Optional[Dict]: Task data if available, None if timeout
        """
        try:
            result = await self.redis.brpop(queue_name, timeout=timeout)
            
            if result:
                _, task_json = result
                task_data = json.loads(task_json)
                
                logger.info("Task retrieved from queue", queue=queue_name, task_id=task_data.get("id"))
                return task_data
                
            return None
            
        except Exception as e:
            logger.error("Failed to get task from queue", queue=queue_name, error=str(e))
            raise


class CacheManager:
    """
    Redis-based caching utilities for storing temporary data and results.
    
    Provides methods for caching agent results, session data, and
    frequently accessed information with TTL support.
    """
    
    def __init__(self):
        self.redis = get_redis()
    
    async def set_cache(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Set a value in the cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 1 hour)
        """
        try:
            value_json = json.dumps(value, default=str)
            await self.redis.setex(key, ttl, value_json)
            
            logger.debug("Cache set", key=key, ttl=ttl)
            
        except Exception as e:
            logger.error("Failed to set cache", key=key, error=str(e))
            raise
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Optional[Any]: Cached value if exists, None otherwise
        """
        try:
            value_json = await self.redis.get(key)
            
            if value_json:
                return json.loads(value_json)
            return None
            
        except Exception as e:
            logger.error("Failed to get cache", key=key, error=str(e))
            return None
    
    async def delete_cache(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key to delete
        """
        try:
            await self.redis.delete(key)
            logger.debug("Cache deleted", key=key)
            
        except Exception as e:
            logger.error("Failed to delete cache", key=key, error=str(e))
    
    async def cache_agent_result(self, agent_name: str, rfp_id: str, result: Dict[str, Any]) -> None:
        """
        Cache an agent's processing result for an RFP.
        
        Args:
            agent_name: Name of the agent
            rfp_id: RFP identifier
            result: Agent processing result
        """
        cache_key = f"agent_result:{agent_name}:{rfp_id}"
        await self.set_cache(cache_key, result, ttl=7200)  # 2 hours


# Global instances (initialized after Redis setup)
message_queue = None
cache_manager = None

def get_message_queue():
    """Get the global message queue instance."""
    global message_queue
    if message_queue is None:
        message_queue = MessageQueue()
    return message_queue

def get_cache_manager():
    """Get the global cache manager instance."""
    global cache_manager
    if cache_manager is None:
        cache_manager = CacheManager()
    return cache_manager