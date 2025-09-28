// Neo4j图谱结构初始化

// 创建唯一性约束
CREATE CONSTRAINT symptom_name_unique IF NOT EXISTS FOR (n:Symptom) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT component_name_unique IF NOT EXISTS FOR (n:Component) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT process_name_unique IF NOT EXISTS FOR (n:Process) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT testcase_name_unique IF NOT EXISTS FOR (n:TestCase) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT material_name_unique IF NOT EXISTS FOR (n:Material) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT metric_name_unique IF NOT EXISTS FOR (n:Metric) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT tool_name_unique IF NOT EXISTS FOR (n:Tool) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT role_name_unique IF NOT EXISTS FOR (n:Role) REQUIRE n.name IS UNIQUE;

// 创建索引
CREATE INDEX symptom_category_index IF NOT EXISTS FOR (n:Symptom) ON (n.category);
CREATE INDEX symptom_tags_index IF NOT EXISTS FOR (n:Symptom) ON (n.tags);
CREATE INDEX component_component_type_index IF NOT EXISTS FOR (n:Component) ON (n.component_type);
CREATE INDEX component_tags_index IF NOT EXISTS FOR (n:Component) ON (n.tags);
CREATE INDEX process_process_type_index IF NOT EXISTS FOR (n:Process) ON (n.process_type);
CREATE INDEX process_phase_index IF NOT EXISTS FOR (n:Process) ON (n.phase);
CREATE INDEX process_tags_index IF NOT EXISTS FOR (n:Process) ON (n.tags);
CREATE INDEX testcase_test_type_index IF NOT EXISTS FOR (n:TestCase) ON (n.test_type);
CREATE INDEX testcase_priority_index IF NOT EXISTS FOR (n:TestCase) ON (n.priority);
CREATE INDEX testcase_tags_index IF NOT EXISTS FOR (n:TestCase) ON (n.tags);
CREATE INDEX material_material_type_index IF NOT EXISTS FOR (n:Material) ON (n.material_type);
CREATE INDEX material_tags_index IF NOT EXISTS FOR (n:Material) ON (n.tags);
CREATE INDEX metric_tags_index IF NOT EXISTS FOR (n:Metric) ON (n.tags);
CREATE INDEX tool_tool_type_index IF NOT EXISTS FOR (n:Tool) ON (n.tool_type);
CREATE INDEX tool_tags_index IF NOT EXISTS FOR (n:Tool) ON (n.tags);
CREATE INDEX role_function_index IF NOT EXISTS FOR (n:Role) ON (n.function);
CREATE INDEX role_tags_index IF NOT EXISTS FOR (n:Role) ON (n.tags);

// 关系定义(仅作参考)
// (Anomaly)-[:HAS_SYMPTOM]->(Symptom)
// (Anomaly)-[:AFFECTS]->(Component)
// (Anomaly)-[:OBSERVED_IN]->(DeviceModel)
// (Anomaly)-[:OCCURS_IN_PROCESS]->(Process)
// (Anomaly)-[:RELATED_TO_MATERIAL]->(Material)
// (Anomaly)-[:MEASURED_BY]->(Metric)
// (Anomaly)-[:RESOLVED_BY]->(Solution)
// (TestCase)-[:TESTS]->(Component)
// (TestCase)-[:USES_TOOL]->(Tool)
// (Process)-[:USES_MATERIAL]->(Material)
// (DeviceModel)-[:HAS_COMPONENT]->(Component)
// (Solution)-[:CHANGES_MATERIAL]->(Material)
// (Role)-[:OWNS_PROCESS]->(Process)
