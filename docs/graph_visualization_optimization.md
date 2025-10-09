# 图谱可视化样式优化报告

## 问题分析

从用户提供的图片可以看出，原始图谱存在以下问题：

1. **节点密度过高** - 显示了过多节点（可能是全部1124个），导致图谱过于密集
2. **节点大小过小** - 所有节点都显示得很小，难以区分和点击
3. **布局参数不合适** - 节点间距太小，重叠严重
4. **颜色对比度不足** - 原始配色方案对比度较低，不够清晰
5. **标签显示不清** - 节点标签太小或不显示

## 优化方案

### 1. 数据显示策略优化

```javascript
// 优先使用样本数据，限制显示节点数量
const nodes = graphData.sampleNodes || graphData.nodes || []
const relations = graphData.sampleRelations || graphData.relations || graphData.links || []

// 限制节点数量以提高性能和可视化效果
const maxNodes = 100
const displayNodes = nodes.slice(0, maxNodes)
const nodeIds = new Set(displayNodes.map(n => n.id))
const displayRelations = relations.filter(rel => 
  nodeIds.has(rel.source) && nodeIds.has(rel.target)
)
```

### 2. 节点大小和样式优化

```javascript
// 增大节点基础大小，提高可见性
const calculateNodeSize = (nodeId) => {
  const connections = getNodeConnections(nodeId)
  return Math.min(Math.max(20 + connections * 3, 20), 100)
}

// 增强节点样式
itemStyle: {
  color: getCategoryColor(node.category),
  borderColor: '#fff',
  borderWidth: 3,           // 增加边框宽度
  shadowBlur: 15,           // 增加阴影
  shadowColor: 'rgba(0, 0, 0, 0.4)'
}
```

### 3. 颜色方案优化

采用高对比度配色方案，提高可读性：

```javascript
const categoryColors = {
  'Symptom': '#E74C3C',      // 深红色 - 症状/问题
  'Component': '#3498DB',    // 蓝色 - 组件
  'Tool': '#2ECC71',         // 绿色 - 工具
  'Process': '#F39C12',      // 橙色 - 流程
  'TestCase': '#9B59B6',     // 紫色 - 测试用例
  'Metric': '#1ABC9C',       // 青绿色 - 指标
  'Role': '#E67E22',         // 深橙色 - 角色
  'Material': '#34495E',     // 深灰蓝 - 材料
  'Product': '#E91E63',      // 粉红色 - 产品
  'Anomaly': '#C0392B'       // 暗红色 - 异常
}
```

### 4. 布局参数优化

```javascript
force: {
  repulsion: 1000,       // 增加斥力，让节点分散更清晰
  gravity: 0.05,         // 降低重力，让布局更自然
  edgeLength: [80, 200], // 增加边长范围，让节点间距更大
  layoutAnimation: true,
  friction: 0.4          // 降低摩擦力，让布局更动态
}
```

### 5. 标签显示优化

```javascript
label: {
  show: true,
  fontSize: 12,
  fontWeight: 'bold',
  color: '#333',
  formatter: function(params) {
    // 显示所有节点的标签，但限制长度
    return params.data.name.length > 8
      ? params.data.name.substring(0, 8) + '...'
      : params.data.name
  }
}
```

### 6. 工具提示优化

增强交互体验，提供更丰富的信息展示：

```javascript
tooltip: {
  trigger: 'item',
  backgroundColor: 'rgba(255, 255, 255, 0.98)',
  borderColor: '#ddd',
  borderWidth: 1,
  borderRadius: 8,
  padding: 12,
  extraCssText: 'box-shadow: 0 4px 12px rgba(0,0,0,0.15);',
  // 详细的格式化函数...
}
```

### 7. 连接线样式优化

```javascript
lineStyle: {
  color: '#999',
  width: 2,              // 增加线条宽度
  curveness: 0.2,        // 增加曲率
  opacity: 0.7           // 提高透明度
}
```

## 实施结果

经过优化后，图谱可视化效果应该有以下改进：

1. **节点清晰可见** - 限制显示数量，增大节点尺寸
2. **颜色对比鲜明** - 采用高对比度配色方案
3. **布局合理** - 节点间距适中，不会过于密集
4. **交互友好** - 增强的工具提示和标签显示
5. **性能优化** - 限制节点数量，提高渲染性能

## 后续建议

1. **分层显示** - 可以考虑实现分层显示功能，用户可以选择显示不同层级的节点
2. **过滤功能** - 完善分类和标签过滤功能
3. **搜索高亮** - 实现搜索结果高亮显示
4. **布局算法** - 可以尝试其他布局算法，如层次布局或圆形布局
5. **响应式设计** - 优化移动端显示效果
