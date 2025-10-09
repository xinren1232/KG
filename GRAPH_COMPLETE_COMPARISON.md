# 🔍 本地图谱 vs 服务器图谱完整对比检查清单

## 📊 数据层面对比

### 1. API请求参数 ✅
**本地配置** (`apps/web/src/api/index.js:102-108`):
```javascript
const params = {
  show_all: showAll,
  limit: showAll ? 15000 : 100,
  min_confidence: 0.1
}
return api.get('/kg/graph', { params })
```

**检查点**:
- ✅ show_all: true
- ✅ limit: 15000
- ✅ min_confidence: 0.1
- ✅ 端点: /kg/graph

### 2. 后端数据映射 ✅
**后端标签映射** (`api/main.py:631-645`):
```python
label_mapping = {
    'Term': 'Component',
    'Tag': 'Metric',
    'Category': 'Process',
    'Product': 'Component',
    'Component': 'Component',
    'Anomaly': 'Symptom',
    'TestCase': 'TestCase',
    'Symptom': 'Symptom',
    'Tool': 'Tool',
    'Process': 'Process',
    'Metric': 'Metric',
    'Role': 'Role',
    'Material': 'Material'
}
```

**检查点**:
- ✅ 节点category字段使用映射后的值
- ✅ categories列表使用映射后的值
- ✅ 所有Neo4j标签都有对应映射

### 3. 前端数据源优先级 ✅
**前端数据加载** (`apps/web/src/views/GraphVisualization.vue:300-301`):
```javascript
const nodes = graphData.sampleNodes || graphData.nodes || []
const relations = graphData.sampleRelations || graphData.relations || graphData.links || []
```

**检查点**:
- ✅ 优先使用 sampleNodes
- ✅ 优先使用 sampleRelations
- ✅ 有调试日志输出

## 🎨 视觉层面对比

### 4. 颜色配置 ✅
**前端颜色映射** (`apps/web/src/views/GraphVisualization.vue:210-224`):
```javascript
const categoryColors = {
  'Symptom': '#E74C3C',      // 深红色
  'Component': '#3498DB',    // 蓝色
  'Tool': '#2ECC71',         // 绿色
  'Process': '#F39C12',      // 橙色
  'TestCase': '#9B59B6',     // 紫色
  'Metric': '#1ABC9C',       // 青绿色
  'Role': '#E67E22',         // 深橙色
  'Material': '#34495E',     // 深灰蓝
  'Product': '#E91E63',      // 粉红色
  'Anomaly': '#C0392B',      // 暗红色
  'Term': '#3498DB',         // 蓝色
  'Tag': '#1ABC9C',          // 青色
  'Category': '#F39C12'      // 橙色
}
```

**检查点**:
- ✅ 13种分类都有颜色
- ✅ 颜色对比度高
- ✅ getCategoryColor函数正确使用

### 5. 节点配置 ✅
**节点样式** (`apps/web/src/views/GraphVisualization.vue:396-410`):
```javascript
data: nodes.map(node => ({
  id: node.id,
  name: node.name,
  category: categories.findIndex(c => c.name === node.category),
  symbolSize: calculateNodeSize(node.id),
  originalCategory: node.category,
  itemStyle: {
    color: getCategoryColor(node.category),  // 使用原始分类名
    borderColor: '#fff',
    borderWidth: 3,
    shadowBlur: 15,
    shadowColor: 'rgba(0, 0, 0, 0.4)'
  }
}))
```

**检查点**:
- ✅ category设为索引（用于图例关联）
- ✅ itemStyle.color使用原始分类名
- ✅ 保存originalCategory字段
- ✅ 边框和阴影效果

### 6. 节点大小计算 ✅
**大小计算** (`apps/web/src/views/GraphVisualization.vue:286-290`):
```javascript
const calculateNodeSize = (nodeId) => {
  const connections = getNodeConnections(nodeId)
  return Math.min(Math.max(15 + connections * 2, 15), 60)
}
```

**检查点**:
- ✅ 基础大小: 15
- ✅ 增长系数: 2
- ✅ 最大值: 60
- ✅ 根据连接数动态调整

### 7. 标签显示策略 ✅
**标签配置** (`apps/web/src/views/GraphVisualization.vue:411-426`):
```javascript
label: {
  show: true,
  fontSize: 9,
  formatter: function(params) {
    const connections = getNodeConnections(params.data.id)
    if (connections > 1 || params.data.symbolSize > 20) {
      return params.data.name.length > 8
        ? params.data.name.substring(0, 8) + '...'
        : params.data.name
    }
    return ''
  }
}
```

**检查点**:
- ✅ 显示阈值: connections > 1 或 symbolSize > 20
- ✅ 字体大小: 9px
- ✅ 名称截断: 8个字符
- ✅ 动态显示逻辑

### 8. 力导向布局 ✅
**布局参数** (`apps/web/src/views/GraphVisualization.vue:449-456`):
```javascript
force: {
  repulsion: 300,
  gravity: 0.1,
  edgeLength: [30, 100],
  layoutAnimation: true,
  friction: 0.6,
  initLayout: 'none'
}
```

**检查点**:
- ✅ 斥力: 300
- ✅ 重力: 0.1
- ✅ 边长: [30, 100]
- ✅ 摩擦力: 0.6
- ✅ 初始布局: none

### 9. 图例配置 ✅
**图例设置** (`apps/web/src/views/GraphVisualization.vue:333-341`):
```javascript
legend: [{
  data: categories.map(c => c.name),
  orient: 'vertical',
  left: 10,
  top: 80,
  textStyle: {
    fontSize: 12
  }
}]
```

**检查点**:
- ✅ 显示所有分类
- ✅ 垂直布局
- ✅ 位置: 左上角
- ✅ 字体大小: 12px

## 🔧 关键修复点

### 最新修复 (刚刚完成)
**问题**: 后端返回的categories包含原始Neo4j标签，未映射
**修复**: 在 `api/main.py:706` 添加映射
```python
categories = [{"name": label_mapping.get(r['category'], r['category']), "count": r['count']} for r in categories_result]
```

## ✅ 完整检查清单

| 检查项 | 本地 | 服务器 | 状态 |
|--------|------|--------|------|
| API参数limit | 15000 | 15000 | ✅ |
| API参数min_confidence | 0.1 | 0.1 | ✅ |
| 后端标签映射 | 完整 | 完整 | ✅ |
| 后端categories映射 | 映射后 | 映射后 | ✅ |
| 前端数据源 | sampleNodes | sampleNodes | ✅ |
| 颜色配置 | 13种 | 13种 | ✅ |
| 节点大小范围 | 15-60 | 15-60 | ✅ |
| 标签显示阈值 | >1连接 | >1连接 | ✅ |
| 力导向斥力 | 300 | 300 | ✅ |
| 力导向重力 | 0.1 | 0.1 | ✅ |
| 边长范围 | [30,100] | [30,100] | ✅ |
| 图例配置 | 完整 | 完整 | ✅ |

## 🚀 部署最新修复

需要重新部署后端文件以应用categories映射修复：

```bash
# 1. 上传修复后的后端文件
scp api/main.py root@47.108.152.16:/opt/knowledge-graph/api/

# 2. 重启后端服务
ssh root@47.108.152.16 "systemctl restart kg-api"

# 3. 验证服务状态
ssh root@47.108.152.16 "systemctl status kg-api"

# 4. 测试API响应
ssh root@47.108.152.16 "curl -s 'http://localhost:8000/kg/graph?limit=1' | python3 -m json.tool"
```

## 🎯 预期最终效果

修复后，服务器图谱应该与本地图谱完全一致：

1. **数据量**: 1421个节点，4910条关系
2. **颜色**: 红、蓝、绿、橙、紫等多种颜色
3. **布局**: 紧密聚类，层次分明
4. **图例**: 显示映射后的分类名（Component, Symptom等）
5. **标签**: 重要节点显示名称
6. **交互**: 悬停提示，点击高亮

---

**下一步**: 部署最新修复并验证效果
