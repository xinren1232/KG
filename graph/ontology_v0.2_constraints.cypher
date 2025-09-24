// 📱 质量知识图谱本体设计 v0.2 - Neo4j约束和索引
// 基于来料异常数据的专业本体设计

// ============================================================================
// 1. 删除现有约束（如果存在）
// ============================================================================

// 删除旧的约束
DROP CONSTRAINT entity_key_unique IF EXISTS;
DROP CONSTRAINT factory_key_unique IF EXISTS;
DROP CONSTRAINT project_key_unique IF EXISTS;
DROP CONSTRAINT material_key_unique IF EXISTS;
DROP CONSTRAINT anomaly_key_unique IF EXISTS;
DROP CONSTRAINT symptom_key_unique IF EXISTS;
DROP CONSTRAINT rootcause_key_unique IF EXISTS;
DROP CONSTRAINT countermeasure_key_unique IF EXISTS;
DROP CONSTRAINT owner_key_unique IF EXISTS;
DROP CONSTRAINT supplier_key_unique IF EXISTS;
DROP CONSTRAINT doc_key_unique IF EXISTS;

// ============================================================================
// 2. 创建实体类型约束和索引
// ============================================================================

// Factory (工厂) - 发生地点
CREATE CONSTRAINT factory_key_unique FOR (f:Factory) REQUIRE f.key IS UNIQUE;
CREATE INDEX factory_name_index FOR (f:Factory) ON (f.name);
CREATE INDEX factory_location_index FOR (f:Factory) ON (f.location);

// Project (项目) - 质量项目
CREATE CONSTRAINT project_key_unique FOR (p:Project) REQUIRE p.key IS UNIQUE;
CREATE INDEX project_name_index FOR (p:Project) ON (p.name);
CREATE INDEX project_phase_index FOR (p:Project) ON (p.phase);

// Material (物料) - 来料物料
CREATE CONSTRAINT material_key_unique FOR (m:Material) REQUIRE m.key IS UNIQUE;
CREATE INDEX material_code_index FOR (m:Material) ON (m.code);
CREATE INDEX material_desc_index FOR (m:Material) ON (m.desc);
CREATE INDEX material_category_index FOR (m:Material) ON (m.category);

// Anomaly (异常) - 具体不良事件
CREATE CONSTRAINT anomaly_key_unique FOR (a:Anomaly) REQUIRE a.key IS UNIQUE;
CREATE INDEX anomaly_title_index FOR (a:Anomaly) ON (a.title);
CREATE INDEX anomaly_date_index FOR (a:Anomaly) ON (a.date);
CREATE INDEX anomaly_severity_index FOR (a:Anomaly) ON (a.severity);
CREATE INDEX anomaly_defect_rate_index FOR (a:Anomaly) ON (a.defect_rate);

// Symptom (症状) - 从描述抽取的不良现象
CREATE CONSTRAINT symptom_key_unique FOR (s:Symptom) REQUIRE s.key IS UNIQUE;
CREATE INDEX symptom_name_index FOR (s:Symptom) ON (s.name);
CREATE INDEX symptom_category_index FOR (s:Symptom) ON (s.category);

// RootCause (根因) - 归纳的不良原因
CREATE CONSTRAINT rootcause_key_unique FOR (rc:RootCause) REQUIRE rc.key IS UNIQUE;
CREATE INDEX rootcause_name_index FOR (rc:RootCause) ON (rc.name);
CREATE INDEX rootcause_detail_index FOR (rc:RootCause) ON (rc.detail);

// Countermeasure (对策) - 对应措施
CREATE CONSTRAINT countermeasure_key_unique FOR (cm:Countermeasure) REQUIRE cm.key IS UNIQUE;
CREATE INDEX countermeasure_name_index FOR (cm:Countermeasure) ON (cm.name);
CREATE INDEX countermeasure_type_index FOR (cm:Countermeasure) ON (cm.type);

// Owner (责任人) - 处理责任人
CREATE CONSTRAINT owner_key_unique FOR (o:Owner) REQUIRE o.key IS UNIQUE;
CREATE INDEX owner_name_index FOR (o:Owner) ON (o.name);
CREATE INDEX owner_role_index FOR (o:Owner) ON (o.role);

// Supplier (供应商) - 物料来源
CREATE CONSTRAINT supplier_key_unique FOR (sp:Supplier) REQUIRE sp.key IS UNIQUE;
CREATE INDEX supplier_name_index FOR (sp:Supplier) ON (sp.name);
CREATE INDEX supplier_contact_index FOR (sp:Supplier) ON (sp.contact);

// Doc (文档) - 数据溯源文件
CREATE CONSTRAINT doc_key_unique FOR (d:Doc) REQUIRE d.key IS UNIQUE;
CREATE INDEX doc_title_index FOR (d:Doc) ON (d.title);
CREATE INDEX doc_type_index FOR (d:Doc) ON (d.type);
CREATE INDEX doc_date_index FOR (d:Doc) ON (d.date);

// ============================================================================
// 3. 创建通用属性索引
// ============================================================================

// 通用时间戳索引
CREATE INDEX entity_created_at_index FOR (n) ON (n.created_at);
CREATE INDEX entity_updated_at_index FOR (n) ON (n.updated_at);
CREATE INDEX entity_source_index FOR (n) ON (n.source);

// ============================================================================
// 4. 创建示例数据（基于真实Excel样例）
// ============================================================================

// 创建工厂
MERGE (f:Factory {key: 'Factory:泰衡诺工厂'})
SET f.name = '泰衡诺工厂',
    f.location = '中国',
    f.created_at = datetime(),
    f.source = 'ontology_v0.2_init';

// 创建项目
MERGE (p:Project {key: 'Project:BG6'})
SET p.name = 'BG6',
    p.phase = '量产',
    p.owner = '项目经理',
    p.created_at = datetime(),
    p.source = 'ontology_v0.2_init';

// 创建物料
MERGE (m:Material {key: 'Material:37300344'})
SET m.code = '37300344',
    m.desc = '复合板电池盖组件',
    m.category = '电池组件',
    m.class = '结构件',
    m.subclass = '盖板',
    m.created_at = datetime(),
    m.source = 'ontology_v0.2_init';

// 创建异常
MERGE (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
SET a.title = '复合板电池盖组件裂纹异常',
    a.defects_number = 50,
    a.defect_rate = 0.05,
    a.date = date('2024-12-31'),
    a.position = '压合工序',
    a.severity = 'S2',
    a.created_at = datetime(),
    a.source = 'ontology_v0.2_init';

// 创建症状
MERGE (s:Symptom {key: 'Symptom:裂纹'})
SET s.name = '裂纹',
    s.category = '外观缺陷',
    s.created_at = datetime(),
    s.source = 'ontology_v0.2_init';

// 创建根因
MERGE (rc:RootCause {key: 'RootCause:压合压力不均导致裂纹'})
SET rc.name = '压合压力不均导致裂纹',
    rc.detail = '治具设计不当，压合过程中压力分布不均匀，导致局部应力集中产生裂纹',
    rc.probability = 0.8,
    rc.created_at = datetime(),
    rc.source = 'ontology_v0.2_init';

// 创建对策
MERGE (cm:Countermeasure {key: 'Countermeasure:更换治具+铁氟龙包裹'})
SET cm.name = '更换治具+铁氟龙包裹',
    cm.type = '技术措施',
    cm.effectiveness = 0.9,
    cm.created_at = datetime(),
    cm.source = 'ontology_v0.2_init';

// 创建责任人
MERGE (o:Owner {key: 'Owner:杨圣杰'})
SET o.name = '杨圣杰',
    o.role = '质量工程师',
    o.created_at = datetime(),
    o.source = 'ontology_v0.2_init';

// 创建供应商
MERGE (sp:Supplier {key: 'Supplier:XX精密制造有限公司'})
SET sp.name = 'XX精密制造有限公司',
    sp.contact = 'supplier@example.com',
    sp.created_at = datetime(),
    sp.source = 'ontology_v0.2_init';

// 创建文档
MERGE (d:Doc {key: 'Doc:来料异常分析报告_20241231'})
SET d.title = '来料异常分析报告_20241231',
    d.path = '/docs/来料异常分析报告_20241231.xlsx',
    d.type = 'Excel',
    d.date = date('2024-12-31'),
    d.created_at = datetime(),
    d.source = 'ontology_v0.2_init';

// ============================================================================
// 5. 创建关系（基于本体设计）
// ============================================================================

// HAPPENED_IN: 异常发生工厂
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (f:Factory {key: 'Factory:泰衡诺工厂'})
MERGE (a)-[:HAPPENED_IN]->(f);

// RELATED_TO: 异常归属项目
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (p:Project {key: 'Project:BG6'})
MERGE (a)-[:RELATED_TO]->(p);

// INVOLVES: 涉及物料
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (m:Material {key: 'Material:37300344'})
MERGE (a)-[:INVOLVES]->(m);

// HAS_SYMPTOM: 异常对应现象
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (s:Symptom {key: 'Symptom:裂纹'})
MERGE (a)-[:HAS_SYMPTOM]->(s);

// HAS_ROOTCAUSE: 异常对应根因
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (rc:RootCause {key: 'RootCause:压合压力不均导致裂纹'})
MERGE (a)-[:HAS_ROOTCAUSE]->(rc);

// RESOLVED_BY: 根因被措施解决
MATCH (rc:RootCause {key: 'RootCause:压合压力不均导致裂纹'})
MATCH (cm:Countermeasure {key: 'Countermeasure:更换治具+铁氟龙包裹'})
MERGE (rc)-[:RESOLVED_BY]->(cm);

// OWNED_BY: 异常责任人
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (o:Owner {key: 'Owner:杨圣杰'})
MERGE (a)-[:OWNED_BY]->(o);

// SUPPLIED_BY: 供应商与物料关系
MATCH (m:Material {key: 'Material:37300344'})
MATCH (sp:Supplier {key: 'Supplier:XX精密制造有限公司'})
MERGE (m)-[:SUPPLIED_BY]->(sp);

// DOCUMENTED_IN: 异常记录来源
MATCH (a:Anomaly {key: 'Anomaly:A-20241231-37300344'})
MATCH (d:Doc {key: 'Doc:来料异常分析报告_20241231'})
MERGE (a)-[:DOCUMENTED_IN]->(d);

// ============================================================================
// 6. 验证数据完整性
// ============================================================================

// 检查节点数量
MATCH (n) RETURN labels(n)[0] as EntityType, count(n) as Count ORDER BY EntityType;

// 检查关系数量
MATCH ()-[r]->() RETURN type(r) as RelationType, count(r) as Count ORDER BY RelationType;

// 检查示例路径：症状 → 异常 → 根因 → 对策
MATCH path = (s:Symptom {name: '裂纹'})-[:HAS_SYMPTOM]-(a:Anomaly)-[:HAS_ROOTCAUSE]->(rc:RootCause)-[:RESOLVED_BY]->(cm:Countermeasure)
RETURN path LIMIT 1;
