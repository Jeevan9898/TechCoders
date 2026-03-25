"""
RFP Identification Agent for the Multi-Agent RFP System.

This agent continuously monitors specified web sources to detect new RFPs,
classifies them using machine learning, and triggers the processing workflow
for relevant opportunities.
"""

import asyncio
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
import structlog

from agents.base_agent import BaseAgent
from models.audit_models import AgentTypeEnum, ActionTypeEnum
from models.rfp_models import RFPDocument, RFPStatusEnum, RFPPriorityEnum
from core.database import AsyncSessionLocal
from core.config import settings


class RFPIdentificationAgent(BaseAgent):
    """
    Specialized agent for RFP detection and classification.
    
    Responsibilities:
    - Monitor configured web sources for new RFPs
    - Extract RFP metadata and content
    - Classify RFPs using ML models for relevance
    - Prioritize urgent RFPs (< 3 months due date)
    - Trigger processing workflow for qualified RFPs
    """
    
    def __init__(self, instance_id: Optional[str] = None):
        """Initialize the RFP Identification Agent."""
        super().__init__(AgentTypeEnum.RFP_IDENTIFICATION, instance_id)
        
        # Agent-specific configuration
        self.config.update({
            "monitoring_interval": settings.RFP_MONITORING_INTERVAL,
            "max_concurrent_sources": 5,
            "classification_threshold": 0.7,
            "urgent_days_threshold": 90,  # 3 months
            "max_rfps_per_run": 50,
        })
        
        # Web scraping configuration
        self.scraping_config = {
            "user_agent": settings.SCRAPING_USER_AGENT,
            "delay_between_requests": settings.SCRAPING_DELAY,
            "timeout": 30,
            "max_retries": 3,
        }
        
        # Mock web sources (in production, these would be configurable)
        self.web_sources = [
            {
                "name": "Government Contracts Portal",
                "url": "https://example-gov-contracts.com/rfps",
                "type": "government",
                "selectors": {
                    "rfp_links": ".rfp-listing a",
                    "title": "h1.rfp-title",
                    "description": ".rfp-description",
                    "due_date": ".due-date",
                    "value": ".project-value"
                }
            },
            {
                "name": "Business RFP Platform",
                "url": "https://example-business-rfps.com/opportunities",
                "type": "business",
                "selectors": {
                    "rfp_links": ".opportunity-card a",
                    "title": ".opp-title",
                    "description": ".opp-summary",
                    "due_date": ".deadline",
                    "value": ".budget"
                }
            }
        ]
        
        self.logger.info("RFP Identification Agent initialized", 
                        sources_count=len(self.web_sources))
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process RFP identification tasks.
        
        Args:
            task_data: Task information containing action type and parameters
            
        Returns:
            Dict containing processing results
        """
        action_type = task_data.get("action_type", "monitor_sources")
        
        if action_type == "monitor_sources":
            return await self._monitor_all_sources()
        elif action_type == "scan_source":
            source_config = task_data.get("source_config")
            return await self._scan_single_source(source_config)
        elif action_type == "classify_rfp":
            rfp_data = task_data.get("rfp_data")
            return await self._classify_rfp(rfp_data)
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    async def _monitor_all_sources(self) -> Dict[str, Any]:
        """
        Monitor all configured web sources for new RFPs.
        
        Returns:
            Dict containing monitoring results and statistics
        """
        self.logger.info("Starting RFP monitoring cycle")
        
        results = {
            "sources_scanned": 0,
            "rfps_found": 0,
            "rfps_classified": 0,
            "urgent_rfps": 0,
            "errors": []
        }
        
        # Process sources concurrently
        semaphore = asyncio.Semaphore(self.config["max_concurrent_sources"])
        tasks = []
        
        for source in self.web_sources:
            task = self._scan_source_with_semaphore(semaphore, source)
            tasks.append(task)
        
        # Wait for all sources to complete
        source_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        for i, result in enumerate(source_results):
            if isinstance(result, Exception):
                error_msg = f"Source {self.web_sources[i]['name']} failed: {str(result)}"
                results["errors"].append(error_msg)
                self.logger.error("Source monitoring failed", 
                                source=self.web_sources[i]['name'], 
                                error=str(result))
            else:
                results["sources_scanned"] += 1
                results["rfps_found"] += result.get("rfps_found", 0)
                results["rfps_classified"] += result.get("rfps_classified", 0)
                results["urgent_rfps"] += result.get("urgent_rfps", 0)
        
        self.logger.info("RFP monitoring cycle completed", **results)
        return results
    
    async def _scan_source_with_semaphore(self, semaphore: asyncio.Semaphore, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan a single source with concurrency control.
        
        Args:
            semaphore: Asyncio semaphore for concurrency control
            source: Source configuration
            
        Returns:
            Dict containing scan results
        """
        async with semaphore:
            return await self._scan_single_source(source)
    
    async def _scan_single_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan a single web source for new RFPs.
        
        Args:
            source: Source configuration with URL and selectors
            
        Returns:
            Dict containing scan results
        """
        source_name = source["name"]
        self.logger.info("Scanning source", source=source_name)
        
        results = {
            "source_name": source_name,
            "rfps_found": 0,
            "rfps_classified": 0,
            "urgent_rfps": 0,
            "new_rfps": []
        }
        
        try:
            # Fetch the source page
            async with httpx.AsyncClient(timeout=self.scraping_config["timeout"]) as client:
                response = await client.get(
                    source["url"],
                    headers={"User-Agent": self.scraping_config["user_agent"]}
                )
                response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract RFP links
            rfp_links = soup.select(source["selectors"]["rfp_links"])
            
            for link in rfp_links[:self.config["max_rfps_per_run"]]:
                try:
                    rfp_url = urljoin(source["url"], link.get("href", ""))
                    
                    # Check if we've already processed this RFP
                    if await self._is_rfp_already_processed(rfp_url):
                        continue
                    
                    # Extract RFP details
                    rfp_data = await self._extract_rfp_details(rfp_url, source)
                    
                    if rfp_data:
                        # Classify the RFP
                        classification = await self._classify_rfp(rfp_data)
                        
                        if classification["is_relevant"]:
                            # Store the RFP in database
                            rfp_id = await self._store_rfp(rfp_data, classification)
                            
                            if rfp_id:
                                results["rfps_found"] += 1
                                results["rfps_classified"] += 1
                                results["new_rfps"].append(rfp_id)
                                
                                # Check if urgent
                                if classification["is_urgent"]:
                                    results["urgent_rfps"] += 1
                                    await self._trigger_urgent_processing(rfp_id)
                    
                    # Respect rate limiting
                    await asyncio.sleep(self.scraping_config["delay_between_requests"])
                    
                except Exception as e:
                    self.logger.error("Failed to process RFP link", 
                                    source=source_name, 
                                    link=link.get("href", ""), 
                                    error=str(e))
        
        except Exception as e:
            self.logger.error("Failed to scan source", source=source_name, error=str(e))
            raise
        
        return results
    
    async def _extract_rfp_details(self, rfp_url: str, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract detailed information from an RFP page.
        
        Args:
            rfp_url: URL of the RFP page
            source: Source configuration with selectors
            
        Returns:
            Dict containing extracted RFP data or None if extraction fails
        """
        try:
            async with httpx.AsyncClient(timeout=self.scraping_config["timeout"]) as client:
                response = await client.get(
                    rfp_url,
                    headers={"User-Agent": self.scraping_config["user_agent"]}
                )
                response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title_elem = soup.select_one(source["selectors"]["title"])
            desc_elem = soup.select_one(source["selectors"]["description"])
            due_date_elem = soup.select_one(source["selectors"]["due_date"])
            value_elem = soup.select_one(source["selectors"]["value"])
            
            # Clean and extract text
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Parse due date
            due_date = None
            if due_date_elem:
                due_date_text = due_date_elem.get_text(strip=True)
                due_date = self._parse_date(due_date_text)
            
            # Parse project value
            project_value = None
            if value_elem:
                value_text = value_elem.get_text(strip=True)
                project_value = self._parse_currency(value_text)
            
            # Get full page content for classification
            raw_content = soup.get_text()
            
            return {
                "title": title,
                "description": description,
                "source_url": rfp_url,
                "source_name": source["name"],
                "due_date": due_date,
                "project_value": project_value,
                "raw_content": raw_content,
                "detected_at": datetime.utcnow()
            }
            
        except Exception as e:
            self.logger.error("Failed to extract RFP details", url=rfp_url, error=str(e))
            return None
    
    async def _classify_rfp(self, rfp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify an RFP for relevance and urgency using ML models.
        
        Args:
            rfp_data: RFP information to classify
            
        Returns:
            Dict containing classification results
        """
        # Mock ML classification (in production, this would use actual ML models)
        title = rfp_data.get("title", "").lower()
        description = rfp_data.get("description", "").lower()
        content = f"{title} {description}"
        
        # Simple keyword-based classification for demo
        relevant_keywords = [
            "software", "technology", "it", "system", "platform", "application",
            "development", "integration", "consulting", "services", "support"
        ]
        
        # Calculate relevance score
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword in content)
        relevance_score = min(keyword_matches / len(relevant_keywords), 1.0)
        
        is_relevant = relevance_score >= self.config["classification_threshold"]
        
        # Check urgency based on due date
        is_urgent = False
        due_date = rfp_data.get("due_date")
        if due_date:
            days_until_due = (due_date - datetime.utcnow()).days
            is_urgent = days_until_due <= self.config["urgent_days_threshold"]
        
        # Determine priority
        if is_urgent and relevance_score > 0.8:
            priority = RFPPriorityEnum.URGENT
        elif relevance_score > 0.8:
            priority = RFPPriorityEnum.HIGH
        elif relevance_score > 0.6:
            priority = RFPPriorityEnum.MEDIUM
        else:
            priority = RFPPriorityEnum.LOW
        
        classification = {
            "is_relevant": is_relevant,
            "is_urgent": is_urgent,
            "relevance_score": relevance_score,
            "priority": priority,
            "confidence": min(relevance_score + 0.2, 1.0),  # Mock confidence
            "classification_reasoning": {
                "keyword_matches": keyword_matches,
                "total_keywords": len(relevant_keywords),
                "days_until_due": (due_date - datetime.utcnow()).days if due_date else None
            }
        }
        
        self.logger.info("RFP classified", 
                        title=rfp_data.get("title", "")[:50],
                        is_relevant=is_relevant,
                        is_urgent=is_urgent,
                        relevance_score=relevance_score)
        
        return classification
    
    async def _store_rfp(self, rfp_data: Dict[str, Any], classification: Dict[str, Any]) -> Optional[str]:
        """
        Store a new RFP in the database.
        
        Args:
            rfp_data: RFP information
            classification: Classification results
            
        Returns:
            String UUID of the stored RFP or None if storage fails
        """
        try:
            async with AsyncSessionLocal() as db:
                rfp = RFPDocument(
                    title=rfp_data["title"],
                    description=rfp_data["description"],
                    source_url=rfp_data["source_url"],
                    source_name=rfp_data["source_name"],
                    due_date=rfp_data.get("due_date"),
                    project_value=rfp_data.get("project_value"),
                    status=RFPStatusEnum.DETECTED,
                    priority=classification["priority"],
                    priority_score=classification["relevance_score"],
                    classification_confidence=classification["confidence"],
                    relevance_score=classification["relevance_score"],
                    raw_content=rfp_data["raw_content"],
                    detected_at=rfp_data["detected_at"]
                )
                
                db.add(rfp)
                await db.commit()
                await db.refresh(rfp)
                
                self.logger.info("RFP stored", rfp_id=str(rfp.id), title=rfp.title[:50])
                return str(rfp.id)
                
        except Exception as e:
            self.logger.error("Failed to store RFP", error=str(e))
            return None
    
    async def _is_rfp_already_processed(self, rfp_url: str) -> bool:
        """
        Check if an RFP has already been processed.
        
        Args:
            rfp_url: URL of the RFP to check
            
        Returns:
            bool: True if already processed, False otherwise
        """
        try:
            async with AsyncSessionLocal() as db:
                from sqlalchemy import select
                query = select(RFPDocument).where(RFPDocument.source_url == rfp_url)
                result = await db.execute(query)
                return result.scalar_one_or_none() is not None
                
        except Exception as e:
            self.logger.error("Failed to check RFP existence", url=rfp_url, error=str(e))
            return False
    
    async def _trigger_urgent_processing(self, rfp_id: str) -> None:
        """
        Trigger immediate processing for urgent RFPs.
        
        Args:
            rfp_id: UUID of the urgent RFP
        """
        try:
            # Send message to orchestrator for immediate processing
            await self.send_message("orchestrator_urgent", {
                "action": "process_urgent_rfp",
                "rfp_id": rfp_id,
                "priority": "urgent",
                "requested_by": self.agent_type.value
            })
            
            self.logger.info("Urgent RFP processing triggered", rfp_id=rfp_id)
            
        except Exception as e:
            self.logger.error("Failed to trigger urgent processing", rfp_id=rfp_id, error=str(e))
    
    def _parse_date(self, date_text: str) -> Optional[datetime]:
        """
        Parse a date string into a datetime object.
        
        Args:
            date_text: Date string to parse
            
        Returns:
            datetime object or None if parsing fails
        """
        # Common date patterns
        patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    if pattern == patterns[0]:  # MM/DD/YYYY
                        month, day, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                    elif pattern == patterns[1]:  # YYYY-MM-DD
                        year, month, day = match.groups()
                        return datetime(int(year), int(month), int(day))
                    elif pattern == patterns[2]:  # DD-MM-YYYY
                        day, month, year = match.groups()
                        return datetime(int(year), int(month), int(day))
                except ValueError:
                    continue
        
        return None
    
    def _parse_currency(self, currency_text: str) -> Optional[float]:
        """
        Parse a currency string into a float value.
        
        Args:
            currency_text: Currency string to parse
            
        Returns:
            float value or None if parsing fails
        """
        # Remove currency symbols and commas
        cleaned = re.sub(r'[^\d.]', '', currency_text)
        
        try:
            return float(cleaned)
        except ValueError:
            return None