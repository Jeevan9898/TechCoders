"""
Database initialization script for the Multi-Agent RFP System.

This script creates sample data for development and testing purposes,
including RFPs, products, and system configuration.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal, init_db
from models.rfp_models import RFPDocument, Requirement, RFPStatusEnum, RFPPriorityEnum
from models.product_models import Product, ProductMatch
from models.pricing_models import PricingCalculation
from models.audit_models import AuditLog, ActionTypeEnum, AgentTypeEnum, EventSeverityEnum


async def create_sample_products():
    """Create sample products for the catalog."""
    products = [
        {
            "sku": "SW-001",
            "name": "Enterprise Software Platform",
            "description": "Comprehensive enterprise software solution with CRM, ERP, and analytics capabilities",
            "category": "software",
            "subcategory": "enterprise",
            "specifications": {
                "deployment": "cloud",
                "users": "unlimited",
                "storage": "1TB included",
                "integrations": ["salesforce", "sap", "oracle"],
                "security": ["sso", "2fa", "encryption"]
            },
            "base_price": 50000.0,
            "availability": True,
            "vendor_name": "TechCorp Solutions",
            "certifications": ["ISO27001", "SOC2", "GDPR"],
            "search_keywords": "enterprise software platform crm erp analytics business management"
        },
        {
            "sku": "HW-001", 
            "name": "High-Performance Server Cluster",
            "description": "Scalable server infrastructure with redundancy and high availability",
            "category": "hardware",
            "subcategory": "servers",
            "specifications": {
                "cpu": "Intel Xeon Gold 6248R",
                "ram": "256GB DDR4",
                "storage": "10TB NVMe SSD",
                "network": "10Gbps Ethernet",
                "redundancy": "N+1 power, RAID 10"
            },
            "base_price": 75000.0,
            "availability": True,
            "vendor_name": "ServerTech Inc",
            "certifications": ["Energy Star", "FCC", "CE"],
            "search_keywords": "server cluster infrastructure hardware high performance computing"
        },
        {
            "sku": "SV-001",
            "name": "IT Consulting Services",
            "description": "Expert IT consulting for digital transformation and system integration",
            "category": "service",
            "subcategory": "consulting",
            "specifications": {
                "expertise": ["cloud migration", "system integration", "security audit"],
                "team_size": "5-10 consultants",
                "duration": "3-12 months",
                "methodology": "agile",
                "deliverables": ["assessment", "roadmap", "implementation"]
            },
            "base_price": 150000.0,
            "pricing_model": "per_project",
            "availability": True,
            "vendor_name": "ConsultPro LLC",
            "certifications": ["PMP", "CISSP", "AWS Certified"],
            "search_keywords": "consulting services digital transformation system integration"
        },
        {
            "sku": "SW-002",
            "name": "Cybersecurity Suite",
            "description": "Comprehensive cybersecurity solution with threat detection and response",
            "category": "software",
            "subcategory": "security",
            "specifications": {
                "features": ["endpoint protection", "network monitoring", "incident response"],
                "deployment": "hybrid",
                "compliance": ["NIST", "ISO27001", "PCI DSS"],
                "ai_powered": True,
                "24x7_monitoring": True
            },
            "base_price": 25000.0,
            "availability": True,
            "vendor_name": "SecureShield Corp",
            "certifications": ["Common Criteria", "FIPS 140-2"],
            "search_keywords": "cybersecurity security suite threat detection endpoint protection"
        },
        {
            "sku": "TR-001",
            "name": "Technical Training Program",
            "description": "Comprehensive technical training for IT staff and end users",
            "category": "training",
            "subcategory": "technical",
            "specifications": {
                "format": ["online", "in-person", "hybrid"],
                "duration": "40 hours",
                "participants": "up to 50",
                "materials": ["videos", "labs", "certification"],
                "languages": ["english", "spanish"]
            },
            "base_price": 15000.0,
            "pricing_model": "per_program",
            "availability": True,
            "vendor_name": "TechEd Solutions",
            "certifications": ["Accredited Training Provider"],
            "search_keywords": "training technical education certification staff development"
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for product_data in products:
            product = Product(**product_data)
            db.add(product)
        
        await db.commit()
        print(f"Created {len(products)} sample products")


async def create_sample_rfps():
    """Create sample RFPs for testing."""
    rfps = [
        {
            "title": "Enterprise Software Modernization Initiative",
            "description": "Seeking comprehensive software platform to modernize legacy systems and improve operational efficiency. Must include CRM, ERP, and analytics capabilities with cloud deployment options.",
            "source_url": "https://example-gov.com/rfp/2024/enterprise-modernization",
            "source_name": "Government Technology Portal",
            "due_date": datetime.utcnow() + timedelta(days=45),
            "project_value": 500000.0,
            "status": RFPStatusEnum.DETECTED,
            "priority": RFPPriorityEnum.HIGH,
            "priority_score": 0.85,
            "classification_confidence": 0.92,
            "relevance_score": 0.88,
            "raw_content": "Enterprise software modernization legacy systems CRM ERP analytics cloud deployment operational efficiency digital transformation",
            "detected_at": datetime.utcnow() - timedelta(hours=2)
        },
        {
            "title": "High-Performance Computing Infrastructure",
            "description": "Request for proposals to provide scalable server infrastructure with high availability and redundancy for research computing workloads.",
            "source_url": "https://example-research.edu/procurement/hpc-infrastructure",
            "source_name": "Research University Procurement",
            "due_date": datetime.utcnow() + timedelta(days=30),
            "project_value": 750000.0,
            "status": RFPStatusEnum.PROCESSING,
            "priority": RFPPriorityEnum.URGENT,
            "priority_score": 0.95,
            "classification_confidence": 0.89,
            "relevance_score": 0.91,
            "raw_content": "high performance computing HPC server infrastructure scalable redundancy availability research workloads cluster",
            "detected_at": datetime.utcnow() - timedelta(hours=6)
        },
        {
            "title": "Cybersecurity Assessment and Implementation",
            "description": "Comprehensive cybersecurity solution needed including threat detection, endpoint protection, and 24/7 monitoring services for critical infrastructure protection.",
            "source_url": "https://example-city.gov/rfp/cybersecurity-2024",
            "source_name": "City Government Portal",
            "due_date": datetime.utcnow() + timedelta(days=60),
            "project_value": 300000.0,
            "status": RFPStatusEnum.MATCHED,
            "priority": RFPPriorityEnum.HIGH,
            "priority_score": 0.78,
            "classification_confidence": 0.85,
            "relevance_score": 0.82,
            "raw_content": "cybersecurity threat detection endpoint protection monitoring services critical infrastructure security assessment",
            "detected_at": datetime.utcnow() - timedelta(days=1)
        },
        {
            "title": "IT Staff Training and Certification Program",
            "description": "Seeking training provider for comprehensive technical education program covering cloud technologies, cybersecurity, and modern development practices.",
            "source_url": "https://example-corp.com/procurement/training-2024",
            "source_name": "Corporate Procurement Portal",
            "due_date": datetime.utcnow() + timedelta(days=90),
            "project_value": 150000.0,
            "status": RFPStatusEnum.PRICED,
            "priority": RFPPriorityEnum.MEDIUM,
            "priority_score": 0.65,
            "classification_confidence": 0.78,
            "relevance_score": 0.72,
            "raw_content": "training certification technical education cloud technologies cybersecurity development practices staff development",
            "detected_at": datetime.utcnow() - timedelta(days=2)
        }
    ]
    
    async with AsyncSessionLocal() as db:
        rfp_ids = []
        for rfp_data in rfps:
            rfp = RFPDocument(**rfp_data)
            db.add(rfp)
            await db.flush()  # Get the ID
            rfp_ids.append(str(rfp.id))
        
        await db.commit()
        print(f"Created {len(rfps)} sample RFPs")
        return rfp_ids


async def create_sample_requirements(rfp_ids):
    """Create sample requirements for RFPs."""
    requirements_data = [
        # Requirements for Enterprise Software RFP
        {
            "rfp_id": rfp_ids[0],
            "text": "The system must provide comprehensive CRM functionality including lead management, opportunity tracking, and customer communication history.",
            "category": "functional",
            "mandatory": True,
            "extracted_specs": {"module": "crm", "features": ["lead_management", "opportunity_tracking", "communication_history"]},
            "confidence_score": 0.92
        },
        {
            "rfp_id": rfp_ids[0],
            "text": "Cloud deployment with 99.9% uptime SLA and automatic scaling capabilities required.",
            "category": "technical",
            "mandatory": True,
            "extracted_specs": {"deployment": "cloud", "sla": "99.9%", "scaling": "automatic"},
            "confidence_score": 0.88
        },
        # Requirements for HPC Infrastructure RFP
        {
            "rfp_id": rfp_ids[1],
            "text": "Minimum 256GB RAM per node with Intel Xeon processors and high-speed interconnect.",
            "category": "hardware",
            "mandatory": True,
            "extracted_specs": {"ram": "256GB", "cpu": "Intel Xeon", "interconnect": "high_speed"},
            "confidence_score": 0.95
        },
        {
            "rfp_id": rfp_ids[1],
            "text": "N+1 redundancy for power and cooling systems with 24/7 monitoring capabilities.",
            "category": "reliability",
            "mandatory": True,
            "extracted_specs": {"redundancy": "N+1", "monitoring": "24x7"},
            "confidence_score": 0.90
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for req_data in requirements_data:
            requirement = Requirement(**req_data)
            db.add(requirement)
        
        await db.commit()
        print(f"Created {len(requirements_data)} sample requirements")


async def create_sample_audit_logs():
    """Create sample audit logs."""
    logs = [
        {
            "event_type": ActionTypeEnum.RFP_DETECTED,
            "event_category": "rfp_monitoring",
            "event_description": "New RFP detected from Government Technology Portal",
            "severity": EventSeverityEnum.INFO,
            "source_agent": AgentTypeEnum.RFP_IDENTIFICATION,
            "event_data": {"source": "gov_portal", "classification_score": 0.85},
            "execution_time_ms": 1250.0
        },
        {
            "event_type": ActionTypeEnum.WORKFLOW_STARTED,
            "event_category": "orchestration",
            "event_description": "RFP processing workflow initiated",
            "severity": EventSeverityEnum.INFO,
            "source_agent": AgentTypeEnum.ORCHESTRATOR,
            "event_data": {"workflow_id": "wf_001", "priority": "high"},
            "execution_time_ms": 450.0
        },
        {
            "event_type": ActionTypeEnum.REQUIREMENTS_EXTRACTED,
            "event_category": "nlp_processing",
            "event_description": "Technical requirements extracted from RFP document",
            "severity": EventSeverityEnum.INFO,
            "source_agent": AgentTypeEnum.TECHNICAL_MATCH,
            "event_data": {"requirements_count": 8, "confidence_avg": 0.87},
            "execution_time_ms": 3200.0
        },
        {
            "event_type": ActionTypeEnum.PRICING_CALCULATED,
            "event_category": "pricing_analysis",
            "event_description": "Pricing strategy calculated with market analysis",
            "severity": EventSeverityEnum.INFO,
            "source_agent": AgentTypeEnum.PRICING,
            "event_data": {"total_price": 485000, "margin": 0.15, "win_probability": 0.72},
            "execution_time_ms": 2800.0
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for log_data in logs:
            audit_log = AuditLog(**log_data)
            db.add(audit_log)
        
        await db.commit()
        print(f"Created {len(logs)} sample audit logs")


async def main():
    """Initialize database with sample data."""
    print("Initializing Multi-Agent RFP System database...")
    
    # Initialize database tables
    await init_db()
    print("Database tables created")
    
    # Create sample data
    await create_sample_products()
    rfp_ids = await create_sample_rfps()
    await create_sample_requirements(rfp_ids)
    await create_sample_audit_logs()
    
    print("Database initialization completed successfully!")
    print("\nSample data created:")
    print("- 5 Products in catalog")
    print("- 4 RFPs with different statuses")
    print("- Requirements extracted from RFPs")
    print("- Audit logs for system monitoring")
    print("\nYou can now start the application and explore the dashboard!")


if __name__ == "__main__":
    asyncio.run(main())