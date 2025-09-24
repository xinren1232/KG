// 创建唯一性约束
CREATE CONSTRAINT product_name_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT anomaly_id_unique IF NOT EXISTS FOR (a:Anomaly) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT testcase_id_unique IF NOT EXISTS FOR (t:TestCase) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT component_name_unique IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS UNIQUE;

// 创建索引
CREATE INDEX product_name_index IF NOT EXISTS FOR (p:Product) ON (p.name);
CREATE INDEX component_name_index IF NOT EXISTS FOR (c:Component) ON (c.name);
CREATE INDEX anomaly_severity_index IF NOT EXISTS FOR (a:Anomaly) ON (a.severity);
CREATE INDEX anomaly_status_index IF NOT EXISTS FOR (a:Anomaly) ON (a.status);
CREATE INDEX testcase_priority_index IF NOT EXISTS FOR (t:TestCase) ON (t.priority);
CREATE INDEX symptom_description_index IF NOT EXISTS FOR (s:Symptom) ON (s.description);
