# 手机研发质量知识图谱本体设计 v0.1

## 目标域
手机研发质量管理，支持：
- 流程查询：根据产品/模块查询测试用例和流程
- 历史异常：异常记录的查询和分析
- 案例指导：症状到根因到对策的路径分析
- 数据分析：质量数据的统计和趋势分析

## 核心实体（节点 Labels）

### 产品相关
- **Product**: 产品型号（如 MyPhoneX, iPhone15）
- **Build**: 版本构建（如 1.0.3, 2.1.0-beta）
- **Component**: 组件模块（如 Camera, Battery, Screen）

### 测试相关
- **TestCase**: 测试用例
- **TestStep**: 测试步骤
- **TestResult**: 测试结果

### 质量相关
- **Anomaly**: 异常记录
- **Symptom**: 症状表现
- **RootCause**: 根本原因
- **Countermeasure**: 对策措施

### 组织相关
- **Owner**: 责任人/团队
- **Supplier**: 供应商

### 文档相关
- **Doc**: 文档资料

## 关键关系

### 产品层次关系
- **HAS_BUILD**: Product → Build（产品包含版本）
- **INCLUDES**: Product → Component（产品包含组件）
- **BELONGS_TO**: Component → Product（组件属于产品）

### 测试关系
- **HAS_STEP**: TestCase → TestStep（用例包含步骤）
- **RESULT_OF**: TestResult → TestCase（结果来自用例）

### 质量关系
- **OBSERVED_IN**: Anomaly → Build（异常在版本中观察到）
- **AFFECTS**: Anomaly → Component（异常影响组件）
- **HAS_SYMPTOM**: Anomaly → Symptom（异常有症状）
- **CAUSES**: RootCause → Anomaly（根因导致异常）
- **RESOLVED_BY**: Anomaly → Countermeasure（异常被对策解决）
- **DUPLICATE_OF**: Anomaly → Anomaly（异常重复）

### 组织关系
- **SUPPLIED_BY**: Component → Supplier（组件由供应商提供）
- **OWNED_BY**: [Any] → Owner（任何实体可有责任人）

### 文档关系
- **DOCUMENTED_IN**: [Any] → Doc（任何实体可被文档记录）

## 唯一键设计

### 主键属性：key
所有核心实体使用统一的 `key` 属性作为唯一标识：
- Product: `Product:MyPhoneX`
- Build: `Build:1.0.3`
- Component: `Component:Camera`
- Anomaly: `QA-2025-0001`
- TestCase: `TC-001`

### 命名规则
- 易变字段（title, status, severity）不作主键
- key 格式：`EntityType:Identifier` 或直接使用业务ID
- 保持key的稳定性，避免因业务变更导致图谱重构

## 索引和约束

### 唯一约束
```cypher
CREATE CONSTRAINT product_key IF NOT EXISTS FOR (n:Product) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT build_key IF NOT EXISTS FOR (n:Build) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT component_key IF NOT EXISTS FOR (n:Component) REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT anomaly_key IF NOT EXISTS FOR (n:Anomaly) REQUIRE n.key IS UNIQUE;
```

### 索引
```cypher
CREATE INDEX symptom_name IF NOT EXISTS FOR (n:Symptom) ON (n.name);
CREATE INDEX rootcause_name IF NOT EXISTS FOR (n:RootCause) ON (n.name);
CREATE INDEX countermeasure_name IF NOT EXISTS FOR (n:Countermeasure) ON (n.name);
```

## 元数据字段

所有节点和关系建议包含以下元数据：
- `source`: 数据来源（如 "excel_import", "manual_input"）
- `doc_id`: 源文档ID
- `page`: 页码（如果适用）
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `created_by`: 创建人

## 实体属性定义

### Product
- key: 唯一标识
- name: 产品名称
- model: 产品型号
- category: 产品类别

### Build
- key: 唯一标识
- name: 构建名称
- version: 构建版本号
- date: 发布日期

### Component
- key: 唯一标识
- name: 组件名称
- category: 组件类别
- code: 组件编码

### Anomaly
- key: 唯一标识（如 QA-2025-0001）
- title: 异常标题
- severity: 严重程度（S1/S2/S3/S4）
- status: 状态（Open/InProgress/Resolved/Closed）

### TestCase
- key: 唯一标识（如 TC-001）
- name: 用例名称
- priority: 优先级

## 枚举字典

### 严重程度
- S1: 致命（Critical）
- S2: 严重（Major）
- S3: 一般（Minor）
- S4: 轻微（Trivial）

### 异常状态
- Open: 开放
- InProgress: 处理中
- Resolved: 已解决
- Closed: 已关闭

### 组件类别
- Hardware: 硬件
- Software: 软件
- Firmware: 固件
- Mechanical: 机械

## 版本历史
- v0.1: 初始版本，定义核心实体和关系
