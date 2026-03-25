"""
Audit and logging models for the Multi-Agent RFP System.

This module defines SQLAlchemy ORM models and Pydantic schemas for
comprehensive audit trails, agent actions, and system events used
for compliance and monitoring purposes.
"""

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import uuid

from core.database import Base


class ActionTypeEnum(str, Enum):
    """Enumeration of agent action types."""
    RFP_DETECTED = "rfp_detected"
    RFP_CLASSIFIED = "rfp_classified"
    REQUIREMENTS_EXTRACTED = "requirements_extracted"
    PRODUCTS_MATCHED = "products_matched"
    PRICING_CALCULATED = "pricing_calculated"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    HUMAN_REVIEW = "human_review"
    APPROVAL_GRANTED = "approval_granted"
    SUBMISSION_SENT = "submission_sent"
    ERROR_OCCURRED = "error_occurred"


class EventSeverityEnum(str, Enum):
    """Enumeration of event severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AgentTypeEnum(str, Enum):
    """Enumeration of agent types."""
    RFP_IDENTIFICATION = "rfp_identification"
    ORCHESTRATOR = "orchestrator"
    TECHNICAL_MATCH = "technical_match"
    PRICING = "pricing"
    SYSTEM = "system"
    HUMAN = "human"


# SQLAlchemy ORM Models

class AuditLog(Base):
    """
    SQLAlchemy model for comprehensive audit logging.
    
    Stores all significant actions and events in the system for
    compliance, debugging, and performance analysis purposes.
    """
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event identification
    event_type = Column(SQLEnum(ActionTypeEnum), nullable=False, index=True)
    event_category = Column(String(100), index=True)
    event_description = Column(Text, nullable=False)
    
    # Severity and importance
    severity = Column(SQLEnum(EventSeverityEnum), default=EventSeverityEnum.INFO, index=True)
    importance_score = Column(Float, default=0.5)  # 0.0 to 1.0
    
    # Source information
    source_agent = Column(SQLEnum(AgentTypeEnum), index=True)
    source_component = Column(String(200))
    source_function = Column(String(200))
    
    # Related entities
    rfp_id = Column(UUID(as_uuid=True), ForeignKey("rfp_documents.id"), index=True)
    user_id = Column(String(100), index=True)  # For human actions
    session_id = Column(String(200))
    
    # Event data and context
    event_data = Column(JSON)  # Structured event data
    context_data = Column(JSON)  # Additional context information
    
    # Performance metrics
    execution_time_ms = Column(Float)  # How long the action took
    memory_usage_mb = Column(Float)    # Memory usage during action
    
    # Request/Response information
    request_id = Column(String(200), index=True)
    correlation_id = Column(String(200), index=True)  # For tracing across services
    
    # Error information (if applicable)
    error_code = Column(String(100))
    error_message = Column(Text)
    stack_trace = Column(Text)
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, severity={self.severity})>"


class AgentAction(Base):
    """
    SQLAlchemy model for tracking specific agent actions.
    
    Stores detailed information about actions performed by each agent,
    including inputs, outputs, and decision reasoning.
    """
    __tablename__ = "agent_actions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Agent information
    agent_type = Column(SQLEnum(AgentTypeEnum), nullable=False, index=True)
    agent_instance_id = Column(String(200))
    agent_version = Column(String(50))
    
    # Action details
    action_type = Column(SQLEnum(ActionTypeEnum), nullable=False, index=True)
    action_name = Column(String(200), nullable=False)
    action_description = Column(Text)
    
    # Related RFP
    rfp_id = Column(UUID(as_uuid=True), ForeignKey("rfp_documents.id"), index=True)
    
    # Input and output data
    input_data = Column(JSON)   # What the agent received
    output_data = Column(JSON)  # What the agent produced
    
    # Decision making information
    decision_reasoning = Column(JSON)  # Why the agent made this decision
    confidence_score = Column(Float)   # Agent's confidence in the action
    alternative_options = Column(JSON) # Other options considered
    
    # Performance metrics
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    cpu_usage_percent = Column(Float)
    memory_peak_mb = Column(Float)
    
    # Success and error tracking
    success = Column(Boolean, default=True)
    error_details = Column(JSON)
    retry_count = Column(Integer, default=0)
    
    # Quality metrics
    quality_score = Column(Float)  # Quality of the output (if measurable)
    human_feedback = Column(JSON)  # Feedback from human reviewers
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AgentAction(id={self.id}, agent={self.agent_type}, action={self.action_type})>"


class SystemEvent(Base):
    """
    SQLAlchemy model for system-level events and monitoring.
    
    Stores information about system health, performance, and
    infrastructure events for operational monitoring.
    """
    __tablename__ = "system_events"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event classification
    event_type = Column(String(100), nullable=False, index=True)
    event_category = Column(String(100), index=True)
    severity = Column(SQLEnum(EventSeverityEnum), default=EventSeverityEnum.INFO, index=True)
    
    # Event details
    title = Column(String(500), nullable=False)
    description = Column(Text)
    
    # System component information
    component = Column(String(200), index=True)  # database, redis, agent, etc.
    service_name = Column(String(200))
    host_name = Column(String(200))
    
    # Metrics and measurements
    metrics = Column(JSON)  # Performance metrics, resource usage, etc.
    
    # Alert and notification
    alert_triggered = Column(Boolean, default=False)
    notification_sent = Column(Boolean, default=False)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String(200))
    acknowledged_at = Column(DateTime(timezone=True))
    
    # Resolution tracking
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
    resolved_by = Column(String(200))
    resolved_at = Column(DateTime(timezone=True))
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SystemEvent(id={self.id}, type={self.event_type}, severity={self.severity})>"


# Pydantic Schemas for API

class AuditLogBase(BaseModel):
    """Base Pydantic schema for audit logs."""
    event_type: ActionTypeEnum
    event_category: Optional[str] = None
    event_description: str = Field(..., min_length=1)
    severity: EventSeverityEnum = EventSeverityEnum.INFO


class AuditLogCreate(AuditLogBase):
    """Schema for creating new audit log entries."""
    source_agent: Optional[AgentTypeEnum] = None
    source_component: Optional[str] = None
    source_function: Optional[str] = None
    rfp_id: Optional[uuid.UUID] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    event_data: Optional[Dict[str, Any]] = None
    context_data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    """Schema for audit log API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    source_agent: Optional[AgentTypeEnum] = None
    source_component: Optional[str] = None
    rfp_id: Optional[uuid.UUID] = None
    user_id: Optional[str] = None
    event_data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: datetime


class AgentActionBase(BaseModel):
    """Base Pydantic schema for agent actions."""
    agent_type: AgentTypeEnum
    action_type: ActionTypeEnum
    action_name: str = Field(..., min_length=1, max_length=200)
    action_description: Optional[str] = None


class AgentActionCreate(AgentActionBase):
    """Schema for creating new agent actions."""
    agent_instance_id: Optional[str] = None
    agent_version: Optional[str] = None
    rfp_id: Optional[uuid.UUID] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    decision_reasoning: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    success: bool = True
    error_details: Optional[Dict[str, Any]] = None


class AgentActionResponse(AgentActionBase):
    """Schema for agent action API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    agent_instance_id: Optional[str] = None
    agent_version: Optional[str] = None
    rfp_id: Optional[uuid.UUID] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    decision_reasoning: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    duration_seconds: Optional[float] = None
    success: bool
    quality_score: Optional[float] = None
    created_at: datetime


class SystemEventBase(BaseModel):
    """Base Pydantic schema for system events."""
    event_type: str = Field(..., min_length=1, max_length=100)
    event_category: Optional[str] = None
    severity: EventSeverityEnum = EventSeverityEnum.INFO
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None


class SystemEventCreate(SystemEventBase):
    """Schema for creating new system events."""
    component: Optional[str] = None
    service_name: Optional[str] = None
    host_name: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    alert_triggered: bool = False


class SystemEventResponse(SystemEventBase):
    """Schema for system event API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    component: Optional[str] = None
    service_name: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    alert_triggered: bool
    notification_sent: bool
    acknowledged: bool
    resolved: bool
    timestamp: datetime


class AuditSearchRequest(BaseModel):
    """Schema for audit log search requests."""
    event_types: Optional[List[ActionTypeEnum]] = None
    severity_levels: Optional[List[EventSeverityEnum]] = None
    source_agents: Optional[List[AgentTypeEnum]] = None
    rfp_id: Optional[uuid.UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)


class AuditSearchResponse(BaseModel):
    """Schema for audit log search results."""
    logs: List[AuditLogResponse]
    total_count: int
    search_time_ms: float