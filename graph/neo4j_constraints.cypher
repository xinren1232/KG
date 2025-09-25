// Neo4j 约束和索引初始化脚本
// 为知识图谱构建助手创建必要的约束和索引

// ============================================================================
// 1. 唯一约束 (Unique Constraints)
// ============================================================================

// Product 产品唯一约束
CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT product_name_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.name IS UNIQUE;

// Build 版本唯一约束
CREATE CONSTRAINT build_id_unique IF NOT EXISTS
FOR (b:Build) REQUIRE b.id IS UNIQUE;

// Component 组件唯一约束
CREATE CONSTRAINT component_id_unique IF NOT EXISTS
FOR (c:Component) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT component_name_unique IF NOT EXISTS
FOR (c:Component) REQUIRE c.name IS UNIQUE;

// TestCase 测试用例唯一约束
CREATE CONSTRAINT testcase_id_unique IF NOT EXISTS
FOR (tc:TestCase) REQUIRE tc.id IS UNIQUE;

// TestStep 测试步骤唯一约束
CREATE CONSTRAINT teststep_id_unique IF NOT EXISTS
FOR (ts:TestStep) REQUIRE ts.id IS UNIQUE;

// TestResult 测试结果唯一约束
CREATE CONSTRAINT testresult_id_unique IF NOT EXISTS
FOR (tr:TestResult) REQUIRE tr.id IS UNIQUE;

// Anomaly 异常唯一约束
CREATE CONSTRAINT anomaly_id_unique IF NOT EXISTS
FOR (a:Anomaly) REQUIRE a.id IS UNIQUE;

// Symptom 症状唯一约束
CREATE CONSTRAINT symptom_id_unique IF NOT EXISTS
FOR (s:Symptom) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT symptom_name_unique IF NOT EXISTS
FOR (s:Symptom) REQUIRE s.name IS UNIQUE;

// RootCause 根因唯一约束
CREATE CONSTRAINT rootcause_id_unique IF NOT EXISTS
FOR (rc:RootCause) REQUIRE rc.id IS UNIQUE;

CREATE CONSTRAINT rootcause_name_unique IF NOT EXISTS
FOR (rc:RootCause) REQUIRE rc.name IS UNIQUE;

// Countermeasure 对策唯一约束
CREATE CONSTRAINT countermeasure_id_unique IF NOT EXISTS
FOR (cm:Countermeasure) REQUIRE cm.id IS UNIQUE;

// Owner 负责人唯一约束
CREATE CONSTRAINT owner_id_unique IF NOT EXISTS
FOR (o:Owner) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT owner_email_unique IF NOT EXISTS
FOR (o:Owner) REQUIRE o.email IS UNIQUE;

// Supplier 供应商唯一约束
CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
FOR (sp:Supplier) REQUIRE sp.id IS UNIQUE;

CREATE CONSTRAINT supplier_name_unique IF NOT EXISTS
FOR (sp:Supplier) REQUIRE sp.name IS UNIQUE;

// Doc 文档唯一约束
CREATE CONSTRAINT doc_id_unique IF NOT EXISTS
FOR (d:Doc) REQUIRE d.id IS UNIQUE;

// ============================================================================
// 2. 索引 (Indexes)
// ============================================================================

// Product 产品索引
CREATE INDEX product_category_index IF NOT EXISTS
FOR (p:Product) ON (p.category);

CREATE INDEX product_status_index IF NOT EXISTS
FOR (p:Product) ON (p.status);

// Build 版本索引
CREATE INDEX build_version_index IF NOT EXISTS
FOR (b:Build) ON (b.version);

CREATE INDEX build_release_date_index IF NOT EXISTS
FOR (b:Build) ON (b.release_date);

// Component 组件索引
CREATE INDEX component_type_index IF NOT EXISTS
FOR (c:Component) ON (c.type);

CREATE INDEX component_category_index IF NOT EXISTS
FOR (c:Component) ON (c.category);

// TestCase 测试用例索引
CREATE INDEX testcase_type_index IF NOT EXISTS
FOR (tc:TestCase) ON (tc.type);

CREATE INDEX testcase_priority_index IF NOT EXISTS
FOR (tc:TestCase) ON (tc.priority);

// TestResult 测试结果索引
CREATE INDEX testresult_status_index IF NOT EXISTS
FOR (tr:TestResult) ON (tr.status);

CREATE INDEX testresult_date_index IF NOT EXISTS
FOR (tr:TestResult) ON (tr.test_date);

// Anomaly 异常索引
CREATE INDEX anomaly_severity_index IF NOT EXISTS
FOR (a:Anomaly) ON (a.severity);

CREATE INDEX anomaly_status_index IF NOT EXISTS
FOR (a:Anomaly) ON (a.status);

CREATE INDEX anomaly_date_index IF NOT EXISTS
FOR (a:Anomaly) ON (a.occurrence_date);

// Symptom 症状索引
CREATE INDEX symptom_category_index IF NOT EXISTS
FOR (s:Symptom) ON (s.category);

CREATE INDEX symptom_severity_index IF NOT EXISTS
FOR (s:Symptom) ON (s.severity);

// RootCause 根因索引
CREATE INDEX rootcause_category_index IF NOT EXISTS
FOR (rc:RootCause) ON (rc.category);

CREATE INDEX rootcause_priority_index IF NOT EXISTS
FOR (rc:RootCause) ON (rc.priority);

// Countermeasure 对策索引
CREATE INDEX countermeasure_type_index IF NOT EXISTS
FOR (cm:Countermeasure) ON (cm.type);

CREATE INDEX countermeasure_status_index IF NOT EXISTS
FOR (cm:Countermeasure) ON (cm.status);

// Owner 负责人索引
CREATE INDEX owner_department_index IF NOT EXISTS
FOR (o:Owner) ON (o.department);

CREATE INDEX owner_role_index IF NOT EXISTS
FOR (o:Owner) ON (o.role);

// Supplier 供应商索引
CREATE INDEX supplier_type_index IF NOT EXISTS
FOR (sp:Supplier) ON (sp.type);

CREATE INDEX supplier_status_index IF NOT EXISTS
FOR (sp:Supplier) ON (sp.status);

// Doc 文档索引
CREATE INDEX doc_type_index IF NOT EXISTS
FOR (d:Doc) ON (d.type);

CREATE INDEX doc_created_date_index IF NOT EXISTS
FOR (d:Doc) ON (d.created_date);

// ============================================================================
// 3. 复合索引 (Composite Indexes)
// ============================================================================

// 产品-版本复合索引
CREATE INDEX product_build_index IF NOT EXISTS
FOR (b:Build) ON (b.product_id, b.version);

// 组件-类型复合索引
CREATE INDEX component_type_category_index IF NOT EXISTS
FOR (c:Component) ON (c.type, c.category);

// 异常-严重程度-状态复合索引
CREATE INDEX anomaly_severity_status_index IF NOT EXISTS
FOR (a:Anomaly) ON (a.severity, a.status);

// 测试结果-状态-日期复合索引
CREATE INDEX testresult_status_date_index IF NOT EXISTS
FOR (tr:TestResult) ON (tr.status, tr.test_date);

// ============================================================================
// 4. 全文索引 (Full-text Indexes)
// ============================================================================

// 产品描述全文索引
CREATE FULLTEXT INDEX product_description_fulltext IF NOT EXISTS
FOR (p:Product) ON EACH [p.description, p.name];

// 组件描述全文索引
CREATE FULLTEXT INDEX component_description_fulltext IF NOT EXISTS
FOR (c:Component) ON EACH [c.description, c.name];

// 症状描述全文索引
CREATE FULLTEXT INDEX symptom_description_fulltext IF NOT EXISTS
FOR (s:Symptom) ON EACH [s.description, s.name];

// 根因描述全文索引
CREATE FULLTEXT INDEX rootcause_description_fulltext IF NOT EXISTS
FOR (rc:RootCause) ON EACH [rc.description, rc.name];

// 对策描述全文索引
CREATE FULLTEXT INDEX countermeasure_description_fulltext IF NOT EXISTS
FOR (cm:Countermeasure) ON EACH [cm.description, cm.name];

// 文档内容全文索引
CREATE FULLTEXT INDEX doc_content_fulltext IF NOT EXISTS
FOR (d:Doc) ON EACH [d.title, d.content, d.summary];

// ============================================================================
// 5. 验证约束和索引
// ============================================================================

// 显示所有约束
SHOW CONSTRAINTS;

// 显示所有索引
SHOW INDEXES;

// ============================================================================
// 6. 初始化完成标记
// ============================================================================

// 创建一个标记节点表示初始化完成
MERGE (init:SystemInit {type: 'constraints_and_indexes', version: '1.0', created_at: datetime()})
SET init.updated_at = datetime();

// 输出完成信息
RETURN 'Neo4j constraints and indexes initialization completed successfully' AS status;
