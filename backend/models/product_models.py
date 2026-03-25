"""
Product catalog and matching models for the Multi-Agent RFP System.

This module defines SQLAlchemy ORM models and Pydantic schemas for
product catalog management, product matching, and similarity scoring
used by the Technical Match Agent.
"""

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import uuid

from core.database import Base


class ProductCategoryEnum(str, Enum):
    """Enumeration of product categories."""
    HARDWARE = "hardware"
    SOFTWARE = "software"
    SERVICE = "service"
    CONSULTING = "consulting"
    TRAINING = "training"
    SUPPORT = "support"
    INTEGRATION = "integration"
    CUSTOM = "custom"


class ComplianceLevelEnum(str, Enum):
    """Enumeration of compliance levels for product matches."""
    FULL_COMPLIANCE = "full_compliance"
    PARTIAL_COMPLIANCE = "partial_compliance"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"


# SQLAlchemy ORM Models

class Product(Base):
    """
    SQLAlchemy model for product catalog items.
    
    Stores all available products/services that can be matched
    to RFP requirements, including specifications and pricing.
    """
    __tablename__ = "products"
    
    # Primary key
    sku = Column(String(100), primary_key=True)
    
    # Basic product information
    name = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    
    # Technical specifications (stored as JSON)
    specifications = Column(JSON)
    technical_details = Column(JSON)
    
    # Pricing information
    base_price = Column(Float)
    currency = Column(String(3), default="USD")
    pricing_model = Column(String(50))  # per_unit, per_hour, fixed, etc.
    
    # Availability and status
    availability = Column(Boolean, default=True)
    stock_quantity = Column(Integer)
    lead_time_days = Column(Integer)
    
    # Vendor information
    vendor_name = Column(String(200))
    vendor_contact = Column(String(200))
    
    # Compliance and certifications
    certifications = Column(JSON)  # List of certifications
    compliance_standards = Column(JSON)  # Compliance standards met
    
    # Search and matching optimization
    search_keywords = Column(Text)  # Keywords for text matching
    feature_vector = Column(JSON)  # ML feature vector for similarity
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    product_matches = relationship("ProductMatch", back_populates="product")
    
    def __repr__(self):
        return f"<Product(sku='{self.sku}', name='{self.name[:50]}...', category='{self.category}')>"


class ProductMatch(Base):
    """
    SQLAlchemy model for product matches to RFP requirements.
    
    Stores the results of matching products to specific requirements,
    including similarity scores and explanations.
    """
    __tablename__ = "product_matches"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirements.id"), nullable=False, index=True)
    product_sku = Column(String(100), ForeignKey("products.sku"), nullable=False, index=True)
    
    # Matching scores and metrics
    similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence_score = Column(Float)  # Confidence in the match
    relevance_score = Column(Float)  # How relevant is this match
    
    # Compliance assessment
    compliance_level = Column(String(50))
    compliance_score = Column(Float)
    compliance_gaps = Column(JSON)  # List of compliance issues
    
    # Explanation and reasoning
    explanation = Column(Text)
    match_reasoning = Column(JSON)  # Structured reasoning data
    feature_matches = Column(JSON)  # Which features matched
    
    # Agent processing information
    processing_agent = Column(String(100))
    processing_version = Column(String(50))
    processing_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Manual review flags
    requires_human_review = Column(Boolean, default=False)
    human_reviewed = Column(Boolean, default=False)
    human_approval = Column(Boolean)
    review_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="product_matches")
    product = relationship("Product", back_populates="product_matches")
    
    def __repr__(self):
        return f"<ProductMatch(id={self.id}, similarity={self.similarity_score:.3f}, compliance='{self.compliance_level}')>"


# Pydantic Schemas for API

class ProductBase(BaseModel):
    """Base Pydantic schema for products."""
    name: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    base_price: Optional[float] = None
    currency: str = "USD"
    pricing_model: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating new products."""
    sku: str = Field(..., min_length=1, max_length=100)
    specifications: Optional[Dict[str, Any]] = None
    technical_details: Optional[Dict[str, Any]] = None
    availability: bool = True
    stock_quantity: Optional[int] = None
    lead_time_days: Optional[int] = None
    vendor_name: Optional[str] = None
    vendor_contact: Optional[str] = None
    certifications: Optional[List[str]] = None
    compliance_standards: Optional[List[str]] = None
    search_keywords: Optional[str] = None


class ProductUpdate(BaseModel):
    """Schema for updating products."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    technical_details: Optional[Dict[str, Any]] = None
    base_price: Optional[float] = None
    availability: Optional[bool] = None
    stock_quantity: Optional[int] = None
    lead_time_days: Optional[int] = None


class ProductResponse(ProductBase):
    """Schema for product API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    sku: str
    specifications: Optional[Dict[str, Any]] = None
    technical_details: Optional[Dict[str, Any]] = None
    availability: bool
    stock_quantity: Optional[int] = None
    lead_time_days: Optional[int] = None
    vendor_name: Optional[str] = None
    vendor_contact: Optional[str] = None
    certifications: Optional[List[str]] = None
    compliance_standards: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class ProductMatchBase(BaseModel):
    """Base Pydantic schema for product matches."""
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: Optional[float] = None
    relevance_score: Optional[float] = None
    compliance_level: str
    explanation: Optional[str] = None


class ProductMatchCreate(ProductMatchBase):
    """Schema for creating new product matches."""
    requirement_id: uuid.UUID
    product_sku: str
    compliance_score: Optional[float] = None
    compliance_gaps: Optional[List[str]] = None
    match_reasoning: Optional[Dict[str, Any]] = None
    feature_matches: Optional[Dict[str, Any]] = None
    processing_agent: str
    processing_version: Optional[str] = None


class ProductMatchResponse(ProductMatchBase):
    """Schema for product match API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    requirement_id: uuid.UUID
    product_sku: str
    compliance_score: Optional[float] = None
    compliance_gaps: Optional[List[str]] = None
    match_reasoning: Optional[Dict[str, Any]] = None
    feature_matches: Optional[Dict[str, Any]] = None
    processing_agent: str
    processing_version: Optional[str] = None
    processing_timestamp: datetime
    requires_human_review: bool
    human_reviewed: bool
    human_approval: Optional[bool] = None
    review_notes: Optional[str] = None
    created_at: datetime
    
    # Include related product information
    product: Optional[ProductResponse] = None


class ProductMatchSummary(BaseModel):
    """Schema for product match summary information."""
    requirement_id: uuid.UUID
    product_sku: str
    product_name: str
    similarity_score: float
    compliance_level: str
    explanation: str
    requires_review: bool


class ProductSearchRequest(BaseModel):
    """Schema for product search requests."""
    query: str = Field(..., min_length=1)
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    availability_only: bool = True
    limit: int = Field(default=20, le=100)


class ProductSearchResponse(BaseModel):
    """Schema for product search results."""
    products: List[ProductResponse]
    total_count: int
    search_time_ms: float
    query: str