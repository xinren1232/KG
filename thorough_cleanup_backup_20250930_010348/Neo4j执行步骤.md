# Neo4j图谱数据导入执行步骤

## 🎯 目标
将1124条修复后的词典数据导入Neo4j，创建Dictionary节点，按8个标准Label分类。

## 📊 数据概览
- **总数据**: 1124条
- **8个Label**: Symptom(259), Metric(190), Component(181), Process(170), TestCase(104), Tool(102), Role(63), Material(55)
- **数据质量**: 已修复格式错误，100%标准化

## 🔧 执行步骤

### 步骤1: 清理和准备
在Neo4j浏览器中执行以下命令：

```cypher
// 1. 清理现有Dictionary节点
MATCH (n:Dictionary) DETACH DELETE n;

// 2. 创建约束和索引
CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;
CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category);
CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags);
```

### 步骤2: 验证准备工作
```cypher
// 检查现有Dictionary节点（应该为0）
MATCH (n:Dictionary) RETURN count(n) as existing_nodes;

// 检查约束和索引
SHOW CONSTRAINTS;
SHOW INDEXES;
```

### 步骤3: 执行批量导入
**重要**: 打开 `更新图谱数据导入脚本.cypher` 文件，复制其中的批量导入部分到Neo4j浏览器执行。

或者分批执行（推荐）：
1. 复制第一批次（第1-50条）
2. 执行并确认成功
3. 继续下一批次
4. 重复直到所有23个批次完成

### 步骤4: 验证导入结果
```cypher
// 检查总数（应该是1124）
MATCH (d:Dictionary) RETURN count(d) as total_dictionary_nodes;

// 按分类统计（验证8个Label分布）
MATCH (d:Dictionary) 
RETURN d.category, count(d) as count 
ORDER BY count DESC;

// 显示示例数据
MATCH (d:Dictionary) 
RETURN d.term, d.category, d.aliases, d.tags 
LIMIT 10;
```

### 步骤5: 验证数据质量
```cypher
// 检查每个Label的示例
MATCH (d:Dictionary) WHERE d.category = 'Symptom'
RETURN d.term, d.description LIMIT 3;

MATCH (d:Dictionary) WHERE d.category = 'Component'
RETURN d.term, d.aliases LIMIT 3;

MATCH (d:Dictionary) WHERE d.category = 'Tool'
RETURN d.term, d.tags LIMIT 3;

// 检查是否有空字段
MATCH (d:Dictionary) 
WHERE d.term IS NULL OR d.term = '' OR d.category IS NULL OR d.category = ''
RETURN count(d) as invalid_nodes;
```

## 📊 预期结果

### 总数验证
```
total_dictionary_nodes: 1124
```

### 分类分布验证
```
Symptom: 259
Metric: 190  
Component: 181
Process: 170
TestCase: 104
Tool: 102
Role: 63
Material: 55
```

### 数据质量验证
```
invalid_nodes: 0
```

## ⚠️ 故障排除

### 如果导入失败
1. **内存不足**: 减少批次大小，每次导入25条
2. **字符编码错误**: 检查特殊字符转义
3. **约束冲突**: 确保term字段唯一性

### 如果数据不完整
1. **重新执行清理**: `MATCH (n:Dictionary) DETACH DELETE n;`
2. **检查源数据**: 确认 `api/data/dictionary.json` 完整
3. **分批导入**: 逐批次执行并验证

### 如果分类错误
1. **检查category字段**: 确保只有8个标准Label
2. **重新分类**: 如果需要，重新运行 `修复Label分类.py`

## 🎉 成功标志
- ✅ Dictionary节点总数: 1124
- ✅ 8个Label分类: 完整覆盖
- ✅ 数据质量: 无空字段
- ✅ 索引和约束: 正常创建
- ✅ 查询性能: 响应快速

## 📈 后续步骤
1. **图谱可视化**: 在Neo4j浏览器中查看节点关系图
2. **前端集成**: 确认前端能正确显示图谱数据
3. **功能测试**: 测试基于图谱的搜索和推荐功能
4. **性能优化**: 根据查询模式优化索引

---

**💡 提示**: 建议在执行前备份现有图谱数据，导入过程中可以随时在Neo4j浏览器中查看进度和结果。
