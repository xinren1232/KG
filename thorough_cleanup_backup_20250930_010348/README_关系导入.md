# 关系导入与建议（使用说明）

## 模板文件位置
- data/relations/templates/
  - testcases_measures_metrics.csv  (TestCase)-[:MEASURES]->(Metric)
  - testcases_uses_tools.csv        (TestCase)-[:USES_TOOL]->(Tool)
  - testcases_covers_components.csv (TestCase)-[:COVERS_COMPONENT]->(Component)
  - process_uses_tools_v2.csv       (Process)-[:USES_TOOL]->(Tool)
  - process_consumes_materials_v2.csv (Process)-[:CONSUMES]->(Material)
  - component_has_symptom.csv       (Component)-[:HAS_SYMPTOM]->(Symptom)

CSV 列：
- source_term,target_term,confidence,source,note
- source_term/target_term 均为词典 term 字段的值；
- confidence 可空，0~1；source/note 可填“规范/文件/工艺卡/门禁规则”等。

## 一键导入
- 实际写入：
```
python import_relations_from_csv.py
```
- 仅统计（不写库）：
```
python import_relations_from_csv.py --dry-run
```

> 脚本会跳过不存在的节点；重复关系用 MERGE 幂等创建；会写入 r.confidence / r.source / r.note / r.updated_at。

## 自动候选建议
根据 Tag 与 Module 共现，生成候选关系 CSV（便于人工审核）：
```
python suggest_relations.py
```
输出到：data/relations/suggestions/
- 同模板列结构，可直接复制到 templates 对应文件再导入

## 验证统计
```
python validate_relations.py
```
- 输出各关系类型计数与 Top 连接点，方便观察导入效果

## 注意
- 所有节点均为 (:Dictionary:具体类别) 组合，唯一键为 Dictionary.term；
- 建议：先跑 suggest_relations.py 生成候选，人工筛选后再导入；
- 如需回滚本轮新增边，可在 Neo4j 浏览器执行：
```
MATCH ()-[r:MEASURES|USES_TOOL|COVERS_COMPONENT|CONSUMES|HAS_SYMPTOM]->() DELETE r;
```

