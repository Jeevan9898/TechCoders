"""
Database configuration and session management for the Multi-Agent RFP System.

This module sets up SQLAlchemy with async support for PostgreSQL,
including connection pooling, session management, and database initialization.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import structlog

from core.config import get_database_url

logger = structlog.get_logger(__name__)

# Database engine with connection pooling
database_url = get_database_url()
if database_url.startswith("sqlite"):
    # SQLite configuration
    engine = create_async_engine(
        database_url,
        echo=False,  # Set to True for SQL query logging in development
    )
else:
    # PostgreSQL configuration
    engine = create_async_engine(
        database_url,
        echo=False,  # Set to True for SQL query logging in development
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    Provides common functionality and naming conventions for all database tables.
    """
    
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )


async def get_db() -> AsyncSession:
    """
    Dependency function to get database session.
    
    Yields:
        AsyncSession: Database session for use in FastAPI dependencies
        
    Usage:
        @app.get("/items/")
        async def read_items(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function should be called during application startup to ensure
    all required tables exist in the database.
    """
    try:
        async with engine.begin() as conn:
            # Import all models to ensure they are registered with Base.metadata
            from models import rfp_models, product_models, pricing_models, audit_models
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db() -> None:
    """
    Close database connections.
    
    Should be called during application shutdown to properly close
    all database connections and clean up resources.
    """
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


# Database utilities for common operations
class DatabaseManager:
    """
    Utility class for common database operations.
    
    Provides helper methods for transactions, bulk operations,
    and database health checks.
    """
    
    @staticmethod
    async def health_check() -> bool:
        """
        Check database connectivity and health.
        
        Returns:
            bool: True if database is healthy, False otherwise
        """
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute("SELECT 1")
                return result.scalar() == 1
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return False
    
    @staticmethod
    async def execute_transaction(operations: list):
        """
        Execute multiple operations in a single transaction.
        
        Args:
            operations: List of async functions to execute in transaction
            
        Raises:
            Exception: If any operation fails, entire transaction is rolled back
        """
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    for operation in operations:
                        await operation(session)
                        
                logger.info("Transaction completed successfully")
                
            except Exception as e:
                logger.error("Transaction failed", error=str(e))
                raise