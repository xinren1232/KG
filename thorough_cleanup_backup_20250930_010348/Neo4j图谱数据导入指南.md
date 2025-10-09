# Neo4j图谱数据导入指南

## 🎯 导入目标
将1124条修复后的词典数据导入Neo4j图谱，创建Dictionary节点。

## 📊 数据概览
- **总数据量**: 1124条词典数据
- **8个Label分类**: Symptom, Component, Tool, Process, TestCase, Metric, Material, Role
- **数据格式**: 已修复aliases和tags字段格式错误

## 🔧 导入步骤

### 1. 启动Neo4j服务
```bash
# 确保Neo4j服务正在运行
neo4j start
# 或者通过Neo4j Desktop启动
```

### 2. 访问Neo4j浏览器
打开浏览器访问: http://localhost:7474

### 3. 执行导入脚本
1. 在Neo4j浏览器中打开 `更新图谱数据导入脚本.cypher`
2. 复制脚本内容到查询框
3. 执行脚本（建议分批执行）

### 4. 验证导入结果
执行以下查询验证导入：

```cypher
// 检查总数
MATCH (d:Dictionary) RETURN count(d) as total;

// 按分类统计
MATCH (d:Dictionary) 
RETURN d.category, count(d) as count 
ORDER BY count DESC;

// 查看示例数据
MATCH (d:Dictionary) 
RETURN d.term, d.category, d.aliases, d.tags 
LIMIT 10;
```

## 📊 预期结果
- **Dictionary节点总数**: 1124个
- **分类分布**:
  - Symptom (症状): 259个
  - Metric (性能指标): 190个
  - Component (组件): 181个
  - Process (流程): 170个
  - TestCase (测试用例): 104个
  - Tool (工具): 102个
  - Role (角色): 63个
  - Material (物料): 55个

## ⚠️ 注意事项
1. **清理现有数据**: 脚本会先删除现有Dictionary节点
2. **批量导入**: 数据分批导入，避免内存问题
3. **字符转义**: 已处理特殊字符转义
4. **索引创建**: 自动创建必要的索引和约束

## 🔧 故障排除

### 如果导入失败
1. 检查Neo4j服务状态
2. 确认内存配置充足
3. 分批执行脚本（每次50条）
4. 检查日志错误信息

### 如果数据不完整
1. 重新执行清理和导入脚本
2. 检查源数据文件完整性
3. 验证字符编码问题

## 📈 后续步骤
1. 验证Dictionary节点创建成功
2. 建立节点间关系（如果需要）
3. 创建图谱可视化
4. 测试图谱查询功能
