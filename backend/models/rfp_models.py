"""
RFP-related data models for the Multi-Agent RFP System.

This module defines SQLAlchemy ORM models and Pydantic schemas for
RFP documents, requirements, and related entities used throughout
the RFP processing pipeline.
"""

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Enum as SQLEnum
try:
    from sqlalchemy.dialects.postgresql import UUID
    UUID_TYPE = UUID(as_uuid=True)
except ImportError:
    UUID_TYPE = String(36)  # Fallback for SQLite
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import uuid

from core.database import Base


class RFPStatusEnum(str, Enum):
    """Enumeration of possible RFP processing statuses."""
    DETECTED = "detected"
    PROCESSING = "processing"
    MATCHED = "matched"
    PRICED = "priced"
    REVIEWED = "reviewed"
    SUBMITTED = "submitted"
    REJECTED = "rejected"


class RFPPriorityEnum(str, Enum):
    """Enumeration of RFP priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# SQLAlchemy ORM Models

class RFPDocument(Base):
    """
    SQLAlchemy model for RFP documents.
    
    Stores all information about detected RFPs including metadata,
    processing status, and relationships to requirements and matches.
    """
    __tablename__ = "rfp_documents"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic RFP information
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    source_url = Column(String(1000))
    source_name = Column(String(200))
    
    # Important dates
    due_date = Column(DateTime(timezone=True))
    submission_deadline = Column(DateTime(timezone=True))
    
    # Financial information
    project_value = Column(Float)
    estimated_budget = Column(Float)
    
    # Processing status
    status = Column(SQLEnum(RFPStatusEnum), default=RFPStatusEnum.DETECTED, index=True)
    priority = Column(SQLEnum(RFPPriorityEnum), default=RFPPriorityEnum.MEDIUM, index=True)
    priority_score = Column(Float, default=0.0)
    
    # ML classification results
    classification_confidence = Column(Float)
    relevance_score = Column(Float)
    
    # Document content
    raw_content = Column(Text)
    processed_content = Column(Text)
    document_metadata = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    detected_at = Column(DateTime(timezone=True))
    
    # Relationships
    requirements = relationship("Requirement", back_populates="rfp_document", cascade="all, delete-orphan")
    pricing_calculations = relationship("PricingCalculation", back_populates="rfp_document")
    
    def __repr__(self):
        return f"<RFPDocument(id={self.id}, title='{self.title[:50]}...', status={self.status})>"


class Requirement(Base):
    """
    SQLAlchemy model for extracted requirements from RFP documents.
    
    Stores individual requirements extracted from RFPs using NLP processing,
    including categorization and confidence scores.
    """
    __tablename__ = "requirements"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key to RFP document
    rfp_id = Column(String(36), ForeignKey("rfp_documents.id"), nullable=False, index=True)
    
    # Requirement content
    text = Column(Text, nullable=False)
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    
    # Requirement properties
    mandatory = Column(Boolean, default=True)
    priority_level = Column(String(50))
    
    # NLP extraction results
    extracted_specs = Column(JSON)  # Technical specifications extracted
    confidence_score = Column(Float)
    extraction_method = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rfp_document = relationship("RFPDocument", back_populates="requirements")
    product_matches = relationship("ProductMatch", back_populates="requirement")
    
    def __repr__(self):
        return f"<Requirement(id={self.id}, category='{self.category}', mandatory={self.mandatory})>"


# Pydantic Schemas for API

class RFPDocumentBase(BaseModel):
    """Base Pydantic schema for RFP documents."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    due_date: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    project_value: Optional[float] = None
    estimated_budget: Optional[float] = None


class RFPDocumentCreate(RFPDocumentBase):
    """Schema for creating new RFP documents."""
    raw_content: Optional[str] = None
    document_metadata: Optional[Dict[str, Any]] = None


class RFPDocumentUpdate(BaseModel):
    """Schema for updating RFP documents."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RFPStatusEnum] = None
    priority: Optional[RFPPriorityEnum] = None
    priority_score: Optional[float] = None
    processed_content: Optional[str] = None


class RFPDocumentResponse(RFPDocumentBase):
    """Schema for RFP document API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    status: RFPStatusEnum
    priority: RFPPriorityEnum
    priority_score: float
    classification_confidence: Optional[float] = None
    relevance_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    detected_at: Optional[datetime] = None
    
    # Related data counts
    requirements_count: Optional[int] = None
    matches_count: Optional[int] = None


class RequirementBase(BaseModel):
    """Base Pydantic schema for requirements."""
    text: str = Field(..., min_length=1)
    category: Optional[str] = None
    subcategory: Optional[str] = None
    mandatory: bool = True
    priority_level: Optional[str] = None


class RequirementCreate(RequirementBase):
    """Schema for creating new requirements."""
    rfp_id: uuid.UUID
    extracted_specs: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    extraction_method: Optional[str] = None


class RequirementResponse(RequirementBase):
    """Schema for requirement API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    rfp_id: uuid.UUID
    extracted_specs: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    extraction_method: Optional[str] = None
    created_at: datetime


class RFPSummary(BaseModel):
    """Schema for RFP summary information."""
    id: uuid.UUID
    title: str
    status: RFPStatusEnum
    priority: RFPPriorityEnum
    due_date: Optional[datetime] = None
    project_value: Optional[float] = None
    priority_score: float
    requirements_count: int
    created_at: datetime


class RFPProcessingStatus(BaseModel):
    """Schema for RFP processing status updates."""
    rfp_id: uuid.UUID
    status: RFPStatusEnum
    progress_percentage: float
    current_stage: str
    estimated_completion: Optional[datetime] = None
    agent_status: Dict[str, str]  # agent_name -> status