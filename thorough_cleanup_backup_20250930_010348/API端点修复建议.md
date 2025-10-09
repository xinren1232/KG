
# API端点修复建议

## 问题
- 前端调用 /kg/dictionary/stats 返回404
- 前端调用 /kg/graph/stats 返回404
- 数据模型不一致：Term vs Dictionary

## 修复方案
1. 确保API查询使用Dictionary标签
2. 添加缺失的API端点
3. 统一数据模型

## 修复后的查询
```cypher
// 使用Dictionary标签而不是Term
MATCH (d:Dictionary)
RETURN d.category as category, count(d) as count
ORDER BY count DESC
```
