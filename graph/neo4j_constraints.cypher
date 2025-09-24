// Neo4j 5.x schema for Quality Knowledge Graph (手机研发质量)
// Idempotent: all statements use IF NOT EXISTS and can be re-run safely

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
CREATE CONSTRAINT doc_key IF NOT EXISTS FOR (n:Doc) REQUIRE n.key IS UNIQUE;

// ---------- Helpful existence constraints ----------
CREATE CONSTRAINT symptom_name_exists IF NOT EXISTS FOR (n:Symptom) REQUIRE n.name IS NOT NULL;
CREATE CONSTRAINT rootcause_name_exists IF NOT EXISTS FOR (n:RootCause) REQUIRE n.name IS NOT NULL;
CREATE CONSTRAINT countermeasure_name_exists IF NOT EXISTS FOR (n:Countermeasure) REQUIRE n.name IS NOT NULL;

// ---------- Indexes for lookup / performance ----------
// Name-based lookups
CREATE INDEX symptom_name IF NOT EXISTS FOR (n:Symptom) ON (n.name);
CREATE INDEX rootcause_name IF NOT EXISTS FOR (n:RootCause) ON (n.name);
CREATE INDEX countermeasure_name IF NOT EXISTS FOR (n:Countermeasure) ON (n.name);

// Key-based lookups (for entities without unique constraints)
CREATE INDEX entity_key IF NOT EXISTS FOR (n:Entity) ON (n.key);

// Temporal indexes for metadata
CREATE INDEX node_created_at IF NOT EXISTS FOR (n:Entity) ON (n.created_at);
CREATE INDEX node_updated_at IF NOT EXISTS FOR (n:Entity) ON (n.updated_at);

// Source tracking indexes
CREATE INDEX node_source IF NOT EXISTS FOR (n:Entity) ON (n.source);
CREATE INDEX node_doc_id IF NOT EXISTS FOR (n:Entity) ON (n.doc_id);

// ---------- Metadata existence constraints (Neo4j 5.7+) ----------
// Uncomment if using Neo4j 5.7+ and want to enforce metadata
// CREATE CONSTRAINT node_source_exists IF NOT EXISTS FOR (n:Entity) REQUIRE n.source IS NOT NULL;
// CREATE CONSTRAINT node_created_at_exists IF NOT EXISTS FOR (n:Entity) REQUIRE n.created_at IS NOT NULL;
// CREATE CONSTRAINT rel_source_exists IF NOT EXISTS FOR ()-[r]-() REQUIRE r.source IS NOT NULL;

// ---------- Relationship indexes for performance ----------
// CREATE INDEX rel_created_at IF NOT EXISTS FOR ()-[r]-() ON (r.created_at);
// CREATE INDEX rel_source IF NOT EXISTS FOR ()-[r]-() ON (r.source);

// Wait for indexes/constraints to come online (no-op if already online)
CALL db.awaitIndexes();

