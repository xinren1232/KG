// Neo4j 5.x schema for Quality Knowledge Graph (手机研发质量)
// Idempotent: all statements use IF NOT EXISTS and can be re-run safely
// Based on ontology v0.1 design requirements

// ---------- Uniqueness constraints (keys) ----------
// Core business entities
CREATE CONSTRAINT product_key IF NOT EXISTS FOR (n:Product) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT build_key IF NOT EXISTS FOR (n:Build) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT component_key IF NOT EXISTS FOR (n:Component) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT anomaly_key IF NOT EXISTS FOR (n:Anomaly) REQUIRE n.key IS UNIQUE;

// Test entities
CREATE CONSTRAINT testcase_key IF NOT EXISTS FOR (n:TestCase) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT teststep_key IF NOT EXISTS FOR (n:TestStep) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT testresult_key IF NOT EXISTS FOR (n:TestResult) REQUIRE n.key IS UNIQUE;

// Organizational entities
CREATE CONSTRAINT owner_key IF NOT EXISTS FOR (n:Owner) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT supplier_key IF NOT EXISTS FOR (n:Supplier) REQUIRE n.key IS UNIQUE;

// Document entities
CREATE CONSTRAINT doc_key IF NOT EXISTS FOR (n:Doc) REQUIRE n.key IS UNIQUE;

// ---------- Existence constraints ----------
// Ensure critical fields are not null
CREATE CONSTRAINT symptom_name_exists IF NOT EXISTS FOR (n:Symptom) REQUIRE n.name IS NOT NULL;
CREATE CONSTRAINT rootcause_name_exists IF NOT EXISTS FOR (n:RootCause) REQUIRE n.name IS NOT NULL;
CREATE CONSTRAINT countermeasure_name_exists IF NOT EXISTS FOR (n:Countermeasure) REQUIRE n.name IS NOT NULL;

// ---------- Indexes for performance ----------
// Name-based lookups (for symptoms, causes, countermeasures)
CREATE INDEX symptom_name IF NOT EXISTS FOR (n:Symptom) ON (n.name);
CREATE INDEX rootcause_name IF NOT EXISTS FOR (n:RootCause) ON (n.name);
CREATE INDEX countermeasure_name IF NOT EXISTS FOR (n:Countermeasure) ON (n.name);

// Composite indexes for common query patterns
CREATE INDEX anomaly_severity_status IF NOT EXISTS FOR (n:Anomaly) ON (n.severity, n.status);
CREATE INDEX component_category IF NOT EXISTS FOR (n:Component) ON (n.category);
CREATE INDEX testcase_priority IF NOT EXISTS FOR (n:TestCase) ON (n.priority);

// Time-based indexes
CREATE INDEX anomaly_created_at IF NOT EXISTS FOR (n:Anomaly) ON (n.created_at);
CREATE INDEX build_date IF NOT EXISTS FOR (n:Build) ON (n.date);

// Full-text search indexes
CREATE FULLTEXT INDEX anomaly_fulltext IF NOT EXISTS FOR (n:Anomaly) ON EACH [n.title, n.description];
CREATE FULLTEXT INDEX symptom_fulltext IF NOT EXISTS FOR (n:Symptom) ON EACH [n.name, n.description];

// ---------- Verification queries ----------
// Use these to verify schema is correctly applied:
// SHOW CONSTRAINTS;
// SHOW INDEXES;
// CALL db.schema.visualization();
