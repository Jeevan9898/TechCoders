"""
RFP management API endpoints for the Multi-Agent RFP System.

This module provides REST API endpoints for managing RFP documents,
requirements, and processing workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
import uuid
import structlog

from core.database import get_db
from models.rfp_models import (
    RFPDocument, Requirement, RFPStatusEnum, RFPPriorityEnum,
    RFPDocumentCreate, RFPDocumentUpdate, RFPDocumentResponse,
    RequirementCreate, RequirementResponse, RFPSummary, RFPProcessingStatus
)
from models.audit_models import AuditLog, ActionTypeEnum, AgentTypeEnum
from services.orchestrator_service import OrchestratorService

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[RFPSummary])
async def list_rfps(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    status: Optional[RFPStatusEnum] = None,
    priority: Optional[RFPPriorityEnum] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of RFP documents with filtering and pagination.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        status: Filter by RFP status
        priority: Filter by RFP priority
        search: Search term for title/description
        db: Database session
        
    Returns:
        List of RFP summaries matching the criteria
    """
    try:
        # Build query with filters
        query = select(RFPDocument)
        
        if status:
            query = query.where(RFPDocument.status == status)
        if priority:
            query = query.where(RFPDocument.priority == priority)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    RFPDocument.title.ilike(search_term),
                    RFPDocument.description.ilike(search_term)
                )
            )
        
        # Add pagination and ordering
        query = query.order_by(RFPDocument.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        rfps = result.scalars().all()
        
        # Convert to summary format
        rfp_summaries = []
        for rfp in rfps:
            # Count requirements for each RFP
            req_count_query = select(func.count(Requirement.id)).where(Requirement.rfp_id == rfp.id)
            req_count_result = await db.execute(req_count_query)
            requirements_count = req_count_result.scalar() or 0
            
            rfp_summaries.append(RFPSummary(
                id=rfp.id,
                title=rfp.title,
                status=rfp.status,
                priority=rfp.priority,
                due_date=rfp.due_date,
                project_value=rfp.project_value,
                priority_score=rfp.priority_score,
                requirements_count=requirements_count,
                created_at=rfp.created_at
            ))
        
        logger.info("RFPs retrieved", count=len(rfp_summaries), filters={"status": status, "priority": priority})
        return rfp_summaries
        
    except Exception as e:
        logger.error("Failed to retrieve RFPs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve RFPs")


@router.post("/", response_model=RFPDocumentResponse)
async def create_rfp(
    rfp_data: RFPDocumentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new RFP document and trigger processing workflow.
    
    Args:
        rfp_data: RFP document data
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Created RFP document with assigned ID
    """
    try:
        # Create new RFP document
        rfp = RFPDocument(
            **rfp_data.model_dump(exclude_unset=True),
            detected_at=func.now()
        )
        
        db.add(rfp)
        await db.commit()
        await db.refresh(rfp)
        
        # Log the creation
        audit_log = AuditLog(
            event_type=ActionTypeEnum.RFP_DETECTED,
            event_category="rfp_management",
            event_description=f"New RFP created: {rfp.title}",
            source_agent=AgentTypeEnum.SYSTEM,
            rfp_id=rfp.id,
            event_data={"rfp_id": str(rfp.id), "title": rfp.title}
        )
        db.add(audit_log)
        await db.commit()
        
        # Trigger processing workflow in background
        background_tasks.add_task(trigger_rfp_processing, str(rfp.id))
        
        logger.info("RFP created", rfp_id=str(rfp.id), title=rfp.title)
        
        return RFPDocumentResponse.model_validate(rfp)
        
    except Exception as e:
        logger.error("Failed to create RFP", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create RFP")


@router.get("/{rfp_id}", response_model=RFPDocumentResponse)
async def get_rfp(
    rfp_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a specific RFP document by ID.
    
    Args:
        rfp_id: UUID of the RFP document
        db: Database session
        
    Returns:
        RFP document details
    """
    try:
        query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        result = await db.execute(query)
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        # Count related requirements and matches
        req_count_query = select(func.count(Requirement.id)).where(Requirement.rfp_id == rfp_id)
        req_count_result = await db.execute(req_count_query)
        requirements_count = req_count_result.scalar() or 0
        
        # Create response with counts
        rfp_response = RFPDocumentResponse.model_validate(rfp)
        rfp_response.requirements_count = requirements_count
        
        return rfp_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve RFP", rfp_id=str(rfp_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve RFP")


@router.put("/{rfp_id}", response_model=RFPDocumentResponse)
async def update_rfp(
    rfp_id: uuid.UUID,
    rfp_update: RFPDocumentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing RFP document.
    
    Args:
        rfp_id: UUID of the RFP document
        rfp_update: Updated RFP data
        db: Database session
        
    Returns:
        Updated RFP document
    """
    try:
        query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        result = await db.execute(query)
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        # Update fields
        update_data = rfp_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rfp, field, value)
        
        await db.commit()
        await db.refresh(rfp)
        
        logger.info("RFP updated", rfp_id=str(rfp_id), updated_fields=list(update_data.keys()))
        
        return RFPDocumentResponse.model_validate(rfp)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update RFP", rfp_id=str(rfp_id), error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update RFP")


@router.delete("/{rfp_id}")
async def delete_rfp(
    rfp_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an RFP document and all related data.
    
    Args:
        rfp_id: UUID of the RFP document
        db: Database session
        
    Returns:
        Success message
    """
    try:
        query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        result = await db.execute(query)
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        await db.delete(rfp)
        await db.commit()
        
        logger.info("RFP deleted", rfp_id=str(rfp_id))
        
        return {"message": "RFP deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete RFP", rfp_id=str(rfp_id), error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete RFP")


@router.get("/{rfp_id}/requirements", response_model=List[RequirementResponse])
async def get_rfp_requirements(
    rfp_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all requirements for a specific RFP.
    
    Args:
        rfp_id: UUID of the RFP document
        db: Database session
        
    Returns:
        List of requirements for the RFP
    """
    try:
        # Verify RFP exists
        rfp_query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        rfp_result = await db.execute(rfp_query)
        if not rfp_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="RFP not found")
        
        # Get requirements
        query = select(Requirement).where(Requirement.rfp_id == rfp_id).order_by(Requirement.created_at)
        result = await db.execute(query)
        requirements = result.scalars().all()
        
        return [RequirementResponse.model_validate(req) for req in requirements]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve requirements", rfp_id=str(rfp_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve requirements")


@router.post("/{rfp_id}/process")
async def trigger_rfp_processing(
    rfp_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger RFP processing workflow.
    
    Args:
        rfp_id: UUID of the RFP document
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Processing status message
    """
    try:
        # Verify RFP exists and is in correct state
        query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        result = await db.execute(query)
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        if rfp.status in [RFPStatusEnum.PROCESSING, RFPStatusEnum.SUBMITTED]:
            raise HTTPException(status_code=400, detail=f"RFP is already {rfp.status}")
        
        # Update status to processing
        rfp.status = RFPStatusEnum.PROCESSING
        await db.commit()
        
        # Trigger processing in background
        background_tasks.add_task(trigger_rfp_processing, str(rfp_id))
        
        logger.info("RFP processing triggered", rfp_id=str(rfp_id))
        
        return {"message": "RFP processing started", "rfp_id": str(rfp_id), "status": "processing"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to trigger RFP processing", rfp_id=str(rfp_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to trigger processing")


@router.get("/{rfp_id}/status", response_model=RFPProcessingStatus)
async def get_rfp_processing_status(
    rfp_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current processing status of an RFP.
    
    Args:
        rfp_id: UUID of the RFP document
        db: Database session
        
    Returns:
        Current processing status and progress
    """
    try:
        # Get RFP
        query = select(RFPDocument).where(RFPDocument.id == rfp_id)
        result = await db.execute(query)
        rfp = result.scalar_one_or_none()
        
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        
        # Calculate progress based on status
        progress_map = {
            RFPStatusEnum.DETECTED: 10.0,
            RFPStatusEnum.PROCESSING: 50.0,
            RFPStatusEnum.MATCHED: 70.0,
            RFPStatusEnum.PRICED: 85.0,
            RFPStatusEnum.REVIEWED: 95.0,
            RFPStatusEnum.SUBMITTED: 100.0,
            RFPStatusEnum.REJECTED: 0.0
        }
        
        # Mock agent status (in real implementation, this would come from agent monitoring)
        agent_status = {
            "rfp_identification": "completed",
            "orchestrator": "active" if rfp.status == RFPStatusEnum.PROCESSING else "idle",
            "technical_match": "completed" if rfp.status in [RFPStatusEnum.MATCHED, RFPStatusEnum.PRICED, RFPStatusEnum.REVIEWED, RFPStatusEnum.SUBMITTED] else "pending",
            "pricing": "completed" if rfp.status in [RFPStatusEnum.PRICED, RFPStatusEnum.REVIEWED, RFPStatusEnum.SUBMITTED] else "pending"
        }
        
        return RFPProcessingStatus(
            rfp_id=rfp_id,
            status=rfp.status,
            progress_percentage=progress_map.get(rfp.status, 0.0),
            current_stage=rfp.status.value.replace("_", " ").title(),
            agent_status=agent_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get processing status", rfp_id=str(rfp_id), error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get processing status")


async def trigger_rfp_processing(rfp_id: str):
    """
    Background task to trigger RFP processing workflow.
    
    This function would normally interface with the Orchestrator Agent
    to start the multi-agent processing pipeline.
    
    Args:
        rfp_id: String UUID of the RFP to process
    """
    try:
        # In a real implementation, this would:
        # 1. Send message to Orchestrator Agent via Redis
        # 2. Orchestrator would coordinate other agents
        # 3. Each agent would update the RFP status as they complete their work
        
        logger.info("Background RFP processing started", rfp_id=rfp_id)
        
        # For now, we'll just log that processing would start
        # TODO: Implement actual agent coordination
        
    except Exception as e:
        logger.error("Background RFP processing failed", rfp_id=rfp_id, error=str(e))