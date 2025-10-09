# 🔧 API调用问题修复指南

## 📋 问题描述

错误信息: `apiClient.getGovernanceData is not a function`

## ✅ 已修复的问题

### 1. API导入方式修复
**修改文件**: `apps/web/src/views/DataGovernanceNew.vue`

**修复前**:
```javascript
import apiClient from '@/api'
// ...
const response = await apiClient.getGovernanceData()
```

**修复后**:
```javascript
import api from '@/api'
// ...
const response = await api.getGovernanceData()
```

### 2. 确认API方法存在
**文件**: `apps/web/src/api/index.js`
```javascript
// 获取数据治理信息
getGovernanceData() {
  return api.get('/kg/governance-data')
},
```

## 🚀 完整解决步骤

### 步骤1: 确保API服务运行
```bash
# 启动API服务
python api/main.py
```

### 步骤2: 确保前端服务运行
```bash
# 启动前端服务
cd apps/web
npm run dev
```

### 步骤3: 清除浏览器缓存
- 按 `Ctrl+Shift+R` (Windows) 或 `Cmd+Shift+R` (Mac)
- 或者按 `F12` 打开开发者工具，右键刷新按钮选择"清空缓存并硬性重新加载"

### 步骤4: 验证修复
访问: http://localhost:5173/governance

## 🔍 问题排查

### 如果仍然出现错误，请检查:

1. **API服务状态**
   - 访问: http://localhost:8000/docs
   - 检查: http://localhost:8000/kg/governance-data

2. **前端服务状态**
   - 访问: http://localhost:5173
   - 检查控制台错误信息 (F12)

3. **Neo4j数据库连接**
   - 确保Neo4j运行在端口7687
   - 检查认证信息: neo4j/password123

## 📊 API端点测试

### 手动测试API端点
```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试数据治理端点
curl http://localhost:8000/kg/governance-data

# 测试图谱数据端点
curl http://localhost:8000/kg/graph-data
```

### 预期响应格式
```json
{
  "ok": true,
  "success": true,
  "data": {
    "data_overview": {
      "total_entries": 1124,
      "quality_score": 92.5,
      ...
    },
    "quality_metrics": [...],
    "issues": [...]
  },
  "message": "获取实时数据治理信息成功"
}
```

## 🎯 验证成功标志

修复成功后，数据治理页面应该显示:
- ✅ 数据概览卡片 (1124条术语)
- ✅ 质量指标表格 (6个指标)
- ✅ 分类分布图表 (8个分类)
- ✅ 问题列表和建议
- ✅ 治理规则状态

## 🌐 相关链接

- **数据治理页面**: http://localhost:5173/governance
- **API文档**: http://localhost:8000/docs
- **主页**: http://localhost:5173
- **图谱可视化**: http://localhost:5173/graph-viz

## 🔧 常见问题解决

### 问题1: API服务未启动
**症状**: 连接被拒绝
**解决**: `python api/main.py`

### 问题2: 前端服务未启动
**症状**: 页面无法访问
**解决**: `cd apps/web && npm run dev`

### 问题3: Neo4j连接失败
**症状**: API返回配置文件数据
**解决**: 启动Neo4j服务，检查端口7687

### 问题4: 浏览器缓存问题
**症状**: 修改后仍显示旧错误
**解决**: 强制刷新 `Ctrl+Shift+R`

## 📈 系统状态检查

### 服务状态检查清单
- [ ] Neo4j数据库运行 (端口7687)
- [ ] API服务运行 (端口8000)
- [ ] 前端服务运行 (端口5173)
- [ ] 浏览器缓存已清除
- [ ] 控制台无错误信息

### 功能验证清单
- [ ] 数据治理页面正常加载
- [ ] 概览卡片显示正确数据
- [ ] 质量指标表格正常
- [ ] 分类分布图表显示
- [ ] 问题列表正常展示

## 🎉 修复完成

如果所有步骤都正确执行，您应该能够:
1. 正常访问数据治理页面
2. 看到基于真实数据的质量指标
3. 查看1124条硬件质量术语的统计
4. 使用所有数据治理功能

修复完成后，系统将提供完整的硬件质量数据治理解决方案！
