# 质量知识图谱本体 v0.1 (手机研发质量)

本体目标覆盖：流程查询 / 历史异常 / 案例指导 / 数据分析

## 1. 实体（节点 Labels）
- Product（产品）
- Build（版本/构建）
- Component（组件/模块）
- TestCase（测试用例）
- TestStep（测试步骤）
- TestResult（测试结果）
- Anomaly（异常/缺陷）
- Symptom（症状/现象）
- RootCause（根因）
- Countermeasure（对策）
- Owner（责任人/团队）
- Supplier（供应商）
- Doc（文档）

通用元数据属性（所有节点均可用）
- key: string，节点唯一业务主键（形如 `Product:MyPhoneX`、`Build:1.0.3`、`Anomaly:QA-2025-0001`）
- name: string，可显示名称
- source: string，来源渠道（excel/pdf/doc/txt/api 等）
- doc_id: string，文档ID或文件名
- page: int，页码/段落/表格位置等
- created_at: datetime
- updated_at: datetime
- created_by: string
- status/title/severity 为易变字段，不能做主键

各节点建议属性
- Product: key, name, model, category
- Build: key, name, version, date
- Component: key, name, category, code
- TestCase: key (可用 `TestCase:<编号>`), name, priority
- TestStep: key (`TestStep:<用例编号>-<序号>`), index, description
- TestResult: key (`TestResult:<用例编号>-<Build>`), status, metrics
- Anomaly: key (`Anomaly:<跟踪号>`), title, severity, status
- Symptom: name, category
- RootCause: name, category
- Countermeasure: name, type
- Owner: key (`Owner:<部门/人员>`), name, org
- Supplier: key (`Supplier:<简称>`), name
- Doc: key (`Doc:<文件唯一ID>`), name, path

## 2. 关系（Relationship Types）
- HAS_BUILD (Product→Build)
- INCLUDES (Product/Build→Component)
- BELONGS_TO (Component/TestCase/Anomaly → Product/Build)
- HAS_STEP (TestCase→TestStep)
- RESULT_OF (TestResult→TestCase/TestStep/Build)
- OBSERVED_IN (Anomaly/Symptom → TestResult/Build)
- AFFECTS (Anomaly → Product/Component)
- HAS_SYMPTOM (Anomaly → Symptom)
- CAUSES (RootCause → Anomaly)
- RESOLVED_BY (Anomaly → Countermeasure)
- DUPLICATE_OF (Anomaly → Anomaly)
- SUPPLIED_BY (Component → Supplier)
- OWNED_BY (Product/Component/TestCase → Owner)
- DOCUMENTED_IN (任意节点 → Doc)

关系通用元数据
- source, doc_id, page, created_at, updated_at, created_by, confidence

## 3. 唯一键与索引
- 节点统一主键属性：key（唯一业务键）
- 唯一约束：Product.key, Build.key, Component.key, Anomaly.key
- 索引：Symptom.name, RootCause.name, Countermeasure.name
- 文件：`graph/neo4j_constraints.cypher`（幂等，支持重复执行）

## 4. 词表（Vocabulary）
- data/vocab/components.csv ≥ 20 条组件标准名与别名
- data/vocab/symptoms.csv ≥ 20 条症状标准名
- data/vocab/causes.csv ≥ 10 条根因类型

用法：
- 抽取阶段统一映射到词表标准名（中英文混用时兜底）
- 构图阶段按标准名生成 `key`（如 `Component:<标准名>`）

## 5. 命名策略（Key 生成）
- Product: `Product:<机型/产品线>`
- Build: `Build:<语义版本/构建号>`
- Component: `Component:<组件标准名>`
- TestCase: `TestCase:<用例编号>`
- TestStep: `TestStep:<用例编号>-<序号>`
- TestResult: `TestResult:<用例编号>-<Build>`
- Anomaly: `Anomaly:<缺陷编号>`
- Owner: `Owner:<组织或员工唯一名>`
- Supplier: `Supplier:<供应商简称>`
- Doc: `Doc:<文档ID>`

注意：
- 易变字段（title/status/severity）仅做属性，不参与 key

## 6. 构图规则建议
- 节点入库使用 `MERGE (n:Label {key: $key}) SET n += $props`，保证幂等
- 关系入库使用 `MERGE (a)-[r:TYPE]->(b) SET r += $props`，并存储 `confidence`
- 统一落库元数据：source, doc_id, page, created_at, updated_at, created_by

## 7. 性能与查询
- shortestPath / 全图查询前确保相关属性有索引/约束
- 高频查询：
  - 按 `key`/`name`/`type` 检索节点
  - 产品→版本→组件层级展开
  - 缺陷→症状/根因/对策的闭环链路

## 8. 版本化
- 本文件为 v0.1，后续变更记录字段新增/枚举变化/关系新增

