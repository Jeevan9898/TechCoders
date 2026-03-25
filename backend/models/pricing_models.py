"""
Pricing and cost calculation models for the Multi-Agent RFP System.

This module defines SQLAlchemy ORM models and Pydantic schemas for
pricing calculations, cost breakdowns, and strategic pricing decisions
used by the Pricing Agent.
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


class PricingStrategyEnum(str, Enum):
    """Enumeration of pricing strategies."""
    COMPETITIVE = "competitive"
    PREMIUM = "premium"
    PENETRATION = "penetration"
    VALUE_BASED = "value_based"
    COST_PLUS = "cost_plus"
    DYNAMIC = "dynamic"


class RiskLevelEnum(str, Enum):
    """Enumeration of risk levels for pricing decisions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# SQLAlchemy ORM Models

class PricingCalculation(Base):
    """
    SQLAlchemy model for pricing calculations.
    
    Stores comprehensive pricing analysis for RFPs including cost breakdowns,
    strategic recommendations, and risk assessments.
    """
    __tablename__ = "pricing_calculations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to RFP document
    rfp_id = Column(UUID(as_uuid=True), ForeignKey("rfp_documents.id"), nullable=False, index=True)
    
    # Basic pricing information
    total_cost = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # Cost breakdown components
    material_cost = Column(Float, default=0.0)
    service_cost = Column(Float, default=0.0)
    testing_cost = Column(Float, default=0.0)
    overhead_cost = Column(Float, default=0.0)
    labor_cost = Column(Float, default=0.0)
    
    # Margin and profit analysis
    gross_margin = Column(Float)  # Percentage
    net_margin = Column(Float)   # Percentage
    profit_amount = Column(Float)
    
    # Strategic pricing
    strategy_type = Column(String(50))
    recommended_discount = Column(Float, default=0.0)  # Percentage
    discount_amount = Column(Float, default=0.0)
    final_price = Column(Float)
    
    # Market analysis
    market_price_min = Column(Float)
    market_price_max = Column(Float)
    market_price_avg = Column(Float)
    competitive_position = Column(String(50))  # below, at, above market
    
    # Risk assessment
    risk_level = Column(String(20))
    risk_factors = Column(JSON)  # List of risk factors
    risk_score = Column(Float)  # 0.0 to 1.0
    
    # Win probability analysis
    win_probability = Column(Float)  # 0.0 to 1.0
    confidence_interval = Column(JSON)  # [lower, upper] bounds
    
    # Detailed cost breakdown (JSON structure)
    cost_breakdown = Column(JSON)
    pricing_strategy = Column(JSON)
    market_analysis = Column(JSON)
    
    # Processing information
    calculation_method = Column(String(100))
    processing_agent = Column(String(100))
    calculation_version = Column(String(50))
    
    # External data sources used
    commodity_prices = Column(JSON)  # Snapshot of commodity prices used
    market_data_sources = Column(JSON)  # List of data sources
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rfp_document = relationship("RFPDocument", back_populates="pricing_calculations")
    scenarios = relationship("PricingScenario", back_populates="pricing_calculation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PricingCalculation(id={self.id}, total_price={self.total_price}, strategy='{self.strategy_type}')>"


class PricingScenario(Base):
    """
    SQLAlchemy model for pricing scenarios and simulations.
    
    Stores different pricing scenarios generated through Monte Carlo
    simulations and sensitivity analysis.
    """
    __tablename__ = "pricing_scenarios"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to pricing calculation
    pricing_calculation_id = Column(UUID(as_uuid=True), ForeignKey("pricing_calculations.id"), nullable=False)
    
    # Scenario information
    scenario_name = Column(String(200), nullable=False)
    scenario_description = Column(Text)
    scenario_type = Column(String(50))  # optimistic, pessimistic, realistic, etc.
    
    # Scenario parameters
    parameters = Column(JSON)  # Input parameters for this scenario
    assumptions = Column(JSON)  # Key assumptions made
    
    # Scenario results
    total_price = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    margin_percentage = Column(Float)
    win_probability = Column(Float)
    
    # Risk metrics for this scenario
    risk_score = Column(Float)
    sensitivity_factors = Column(JSON)  # Which factors most affect outcome
    
    # Simulation metadata
    simulation_runs = Column(Integer)  # Number of Monte Carlo runs
    confidence_level = Column(Float)   # Confidence level (e.g., 0.95)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    pricing_calculation = relationship("PricingCalculation", back_populates="scenarios")
    
    def __repr__(self):
        return f"<PricingScenario(id={self.id}, name='{self.scenario_name}', price={self.total_price})>"


# Pydantic Schemas for API

class CostBreakdownSchema(BaseModel):
    """Schema for detailed cost breakdown."""
    material_cost: float = 0.0
    service_cost: float = 0.0
    testing_cost: float = 0.0
    overhead_cost: float = 0.0
    labor_cost: float = 0.0
    total_cost: float


class PricingStrategySchema(BaseModel):
    """Schema for pricing strategy information."""
    strategy_type: PricingStrategyEnum
    recommended_discount: float = 0.0
    discount_reasoning: Optional[str] = None
    market_position: Optional[str] = None
    competitive_factors: Optional[List[str]] = None


class MarketAnalysisSchema(BaseModel):
    """Schema for market analysis data."""
    market_price_min: Optional[float] = None
    market_price_max: Optional[float] = None
    market_price_avg: Optional[float] = None
    competitive_position: str
    market_trends: Optional[List[str]] = None
    data_sources: Optional[List[str]] = None


class RiskAssessmentSchema(BaseModel):
    """Schema for risk assessment information."""
    risk_level: RiskLevelEnum
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_factors: List[str]
    mitigation_strategies: Optional[List[str]] = None


class PricingCalculationBase(BaseModel):
    """Base Pydantic schema for pricing calculations."""
    total_cost: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    currency: str = "USD"
    strategy_type: PricingStrategyEnum
    recommended_discount: float = Field(default=0.0, ge=0.0, le=100.0)


class PricingCalculationCreate(PricingCalculationBase):
    """Schema for creating new pricing calculations."""
    rfp_id: uuid.UUID
    cost_breakdown: CostBreakdownSchema
    pricing_strategy: PricingStrategySchema
    market_analysis: Optional[MarketAnalysisSchema] = None
    risk_assessment: Optional[RiskAssessmentSchema] = None
    calculation_method: str
    processing_agent: str
    commodity_prices: Optional[Dict[str, float]] = None


class PricingCalculationUpdate(BaseModel):
    """Schema for updating pricing calculations."""
    total_cost: Optional[float] = None
    total_price: Optional[float] = None
    strategy_type: Optional[PricingStrategyEnum] = None
    recommended_discount: Optional[float] = None
    final_price: Optional[float] = None
    win_probability: Optional[float] = None
    risk_level: Optional[RiskLevelEnum] = None


class PricingCalculationResponse(PricingCalculationBase):
    """Schema for pricing calculation API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    rfp_id: uuid.UUID
    
    # Cost breakdown
    material_cost: float
    service_cost: float
    testing_cost: float
    overhead_cost: float
    labor_cost: float
    
    # Margin analysis
    gross_margin: Optional[float] = None
    net_margin: Optional[float] = None
    profit_amount: Optional[float] = None
    
    # Strategic pricing
    discount_amount: float
    final_price: Optional[float] = None
    
    # Market analysis
    market_price_min: Optional[float] = None
    market_price_max: Optional[float] = None
    market_price_avg: Optional[float] = None
    competitive_position: Optional[str] = None
    
    # Risk and probability
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    win_probability: Optional[float] = None
    
    # Processing info
    calculation_method: Optional[str] = None
    processing_agent: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    calculated_at: datetime


class PricingScenarioBase(BaseModel):
    """Base Pydantic schema for pricing scenarios."""
    scenario_name: str = Field(..., min_length=1, max_length=200)
    scenario_description: Optional[str] = None
    scenario_type: str
    total_price: float = Field(..., gt=0)
    total_cost: float = Field(..., gt=0)


class PricingScenarioCreate(PricingScenarioBase):
    """Schema for creating new pricing scenarios."""
    pricing_calculation_id: uuid.UUID
    parameters: Optional[Dict[str, Any]] = None
    assumptions: Optional[Dict[str, Any]] = None
    margin_percentage: Optional[float] = None
    win_probability: Optional[float] = None
    risk_score: Optional[float] = None
    simulation_runs: Optional[int] = None
    confidence_level: Optional[float] = None


class PricingScenarioResponse(PricingScenarioBase):
    """Schema for pricing scenario API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    pricing_calculation_id: uuid.UUID
    parameters: Optional[Dict[str, Any]] = None
    assumptions: Optional[Dict[str, Any]] = None
    margin_percentage: Optional[float] = None
    win_probability: Optional[float] = None
    risk_score: Optional[float] = None
    sensitivity_factors: Optional[Dict[str, Any]] = None
    simulation_runs: Optional[int] = None
    confidence_level: Optional[float] = None
    created_at: datetime


class PricingSummary(BaseModel):
    """Schema for pricing summary information."""
    rfp_id: uuid.UUID
    total_price: float
    recommended_discount: float
    final_price: float
    win_probability: float
    risk_level: str
    competitive_position: str
    margin_percentage: float


class PriceOptimizationRequest(BaseModel):
    """Schema for price optimization requests."""
    rfp_id: uuid.UUID
    target_win_probability: float = Field(..., ge=0.0, le=1.0)
    max_discount: float = Field(default=20.0, ge=0.0, le=50.0)
    risk_tolerance: RiskLevelEnum = RiskLevelEnum.MEDIUM
    constraints: Optional[Dict[str, Any]] = None