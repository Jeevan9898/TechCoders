-- Multi-Agent RFP System Database Initialization
-- This script sets up the initial database structure and permissions

-- Create database if it doesn't exist (handled by docker-compose)
-- CREATE DATABASE rfp_system;

-- Connect to the database
\c rfp_system;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types for enums
CREATE TYPE rfp_status AS ENUM (
    'detected',
    'processing', 
    'matched',
    'priced',
    'reviewed',
    'submitted',
    'rejected'
);

CREATE TYPE rfp_priority AS ENUM (
    'low',
    'medium',
    'high',
    'urgent'
);

CREATE TYPE agent_type AS ENUM (
    'rfp_identification',
    'orchestrator',
    'technical_match',
    'pricing',
    'system',
    'human'
);

CREATE TYPE action_type AS ENUM (
    'rfp_detected',
    'rfp_classified',
    'requirements_extracted',
    'products_matched',
    'pricing_calculated',
    'workflow_started',
    'workflow_completed',
    'human_review',
    'approval_granted',
    'submission_sent',
    'error_occurred'
);

CREATE TYPE event_severity AS ENUM (
    'debug',
    'info',
    'warning',
    'error',
    'critical'
);

-- Grant permissions to the application user
GRANT ALL PRIVILEGES ON DATABASE rfp_system TO rfp_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rfp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rfp_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO rfp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO rfp_user;

-- Create indexes for better performance (will be created by Alembic migrations)
-- These are just examples of what will be created

-- Performance optimization settings
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET track_activity_query_size = 2048;
ALTER SYSTEM SET pg_stat_statements.track = 'all';

-- Reload configuration
SELECT pg_reload_conf();