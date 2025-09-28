# 知识图谱本体设计

## 1. 核心实体类型（Node Labels）

### 产品相关
- **Product**: 产品/机型（如：iPhone 15, Galaxy S24）
- **Build**: 版本/构建（如：V1.0.1, Beta-20240315）
- **Component**: 组件/模块（如：摄像头, 电池, 屏幕, WiFi模块）

### 测试相关
- **TestCase**: 测试用例
- **TestSuite**: 测试套件
- **TestFlow**: 测试流程

### 异常相关
- **Anomaly**: 异常/缺陷
- **Symptom**: 症状/现象
- **RootCause**: 根因
- **Countermeasure**: 对策/解决方案

### 知识相关
- **Document**: 文档（流程文档、规范等）
- **Person**: 人员（测试人员、开发人员）
- **Team**: 团队

## 2. 关系类型（Relationship Types）

### 产品层次关系
- `HAS_BUILD`: Product → Build（产品包含版本）
- `HAS_COMPONENT`: Product/Build → Component（包含组件）
- `DEPENDS_ON`: Component → Component（组件依赖）

### 测试关系
- `TESTS`: TestCase → Component（测试用例测试组件）
- `BELONGS_TO`: TestCase → TestSuite（用例属于套件）
- `FOLLOWS`: TestCase → TestCase（用例执行顺序）
- `COVERS`: TestFlow → Component（流程覆盖组件）

### 异常关系
- `OCCURS_IN`: Anomaly → Component（异常发生在组件）
- `AFFECTS`: Anomaly → Product/Build（异常影响产品/版本）
- `HAS_SYMPTOM`: Anomaly → Symptom（异常有症状）
- `CAUSED_BY`: Anomaly → RootCause（异常由根因引起）
- `SOLVED_BY`: Anomaly → Countermeasure（异常被对策解决）
- `SIMILAR_TO`: Anomaly → Anomaly（相似异常）

### 知识关系
- `DOCUMENTED_IN`: * → Document（记录在文档中）
- `RESPONSIBLE_FOR`: Person → Component/TestCase（负责）
- `MEMBER_OF`: Person → Team（团队成员）

## 3. 属性设计

### Product
```json
{
  "name": "iPhone 15",
  "model": "A2846",
  "category": "smartphone",
  "release_date": "2023-09-15",
  "status": "active"
}
```

### Component
```json
{
  "name": "摄像头模块",
  "type": "hardware",
  "version": "V2.1",
  "supplier": "Sony",
  "criticality": "high"
}
```

### Anomaly
```json
{
  "id": "ANO-2024-001",
  "title": "摄像头无法对焦",
  "description": "在低光环境下摄像头无法正常对焦",
  "severity": "high",
  "status": "resolved",
  "created_date": "2024-01-15",
  "resolved_date": "2024-01-20",
  "reporter": "张三"
}
```

### TestCase
```json
{
  "id": "TC-CAM-001",
  "title": "摄像头对焦功能测试",
  "description": "验证摄像头在各种光线条件下的对焦功能",
  "priority": "high",
  "type": "functional",
  "steps": ["打开相机应用", "切换到拍照模式", "点击屏幕进行对焦"],
  "expected_result": "摄像头能够正常对焦"
}
```

## 4. 索引和约束

### 唯一性约束
```cypher
CREATE CONSTRAINT product_name_unique FOR (p:Product) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT anomaly_id_unique FOR (a:Anomaly) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT testcase_id_unique FOR (t:TestCase) REQUIRE t.id IS UNIQUE;
```

### 索引
```cypher
CREATE INDEX product_name_index FOR (p:Product) ON (p.name);
CREATE INDEX component_name_index FOR (c:Component) ON (c.name);
CREATE INDEX anomaly_severity_index FOR (a:Anomaly) ON (a.severity);
CREATE INDEX anomaly_status_index FOR (a:Anomaly) ON (a.status);
```

## 5. 查询模式示例

### 查找产品的所有测试用例
```cypher
MATCH (p:Product)-[:HAS_COMPONENT]->(c:Component)<-[:TESTS]-(tc:TestCase)
WHERE p.name = 'iPhone 15'
RETURN tc.id, tc.title, c.name as component
```

### 查找异常的因果路径
```cypher
MATCH path = (s:Symptom)<-[:HAS_SYMPTOM]-(a:Anomaly)-[:CAUSED_BY]->(rc:RootCause)
MATCH (a)-[:SOLVED_BY]->(cm:Countermeasure)
WHERE s.description CONTAINS '无法对焦'
RETURN path, cm
```

### 查找相似异常
```cypher
MATCH (a1:Anomaly)-[:OCCURS_IN]->(c:Component)<-[:OCCURS_IN]-(a2:Anomaly)
WHERE a1.id = 'ANO-2024-001' AND a1 <> a2
RETURN a2, c
ORDER BY a2.severity DESC
```
