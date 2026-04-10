-- db_exercises/schema.sql

-- 1. Metadata for entities
CREATE TABLE IF NOT EXISTS entity_metadata (
    entity_id VARCHAR PRIMARY KEY,
    category VARCHAR,
    sub_category VARCHAR
);

-- 2. Daily aggregated metrics
CREATE TABLE IF NOT EXISTS metrics_daily (
    entity_id VARCHAR,
    event_date DATE,
    visits INTEGER,
    device_type VARCHAR,
    PRIMARY KEY (entity_id, event_date, device_type)
);

-- 3. Raw behavioral logs
CREATE TABLE IF NOT EXISTS activity_logs (
    subject_id INTEGER,
    occured_at TIMESTAMP,
    entity_id VARCHAR,
    activity_type VARCHAR
);

-- 4. Attribute/Keyword performance
CREATE TABLE IF NOT EXISTS attribute_performance (
    attribute_name VARCHAR,
    entity_id VARCHAR,
    event_date DATE,
    source_type VARCHAR, 
    volume INTEGER
);