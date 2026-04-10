-- Domain metadata for categorization
CREATE TABLE IF NOT EXISTS entity_metadata (
    entity_id VARCHAR PRIMARY KEY,
    category VARCHAR,
    sub_category VARCHAR
);

-- Aggregated daily traffic
CREATE TABLE IF NOT EXISTS metrics_daily (
    entity_id VARCHAR,
    event_date DATE,
    visits INTEGER,
    device_type VARCHAR,
    PRIMARY KEY (entity_id, event_date, device_type)
);

-- Raw clickstream logs for sessionization/bot detection
CREATE TABLE IF NOT EXISTS activity_logs (
    subject_id INTEGER,
    occured_at TIMESTAMP,
    entity_id VARCHAR,
    activity_type VARCHAR
);
