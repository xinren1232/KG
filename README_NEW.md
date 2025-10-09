# 📚 质量知识图谱助手

> 专为手机研发质量部门设计的智能化知识管理平台，集成词典管理、知识图谱、文档解析和智能问答功能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0+-red.svg)](https://fastapi.tiangolo.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.23+-blue.svg)](https://neo4j.com/)

## 🎯 项目简介

质量知识图谱助手是一个专业的知识管理系统，专为手机研发质量部门设计。系统通过图数据库技术构建完整的质量知识体系，提供智能化的词典管理、知识图谱可视化、文档解析和智能问答功能，帮助团队建立标准化的质量管理流程。

### 📊 系统概览

- **数据规模**: 1,333个术语节点 + 17,412个关系
- **服务状态**: 生产环境运行 (http://47.108.152.16)
- **系统版本**: v1.3.0
- **技术架构**: 微服务架构 (前后端分离)
- **系统评级**: A级 (87/100分)

### ✨ 核心特性

#### 📚 词典管理系统
- **标准化术语管理** - 1,333个专业术语，8大分类体系
- **智能别名映射** - 1,746个别名，支持多种表达方式
- **标签体系** - 131个标准化标签，精确分类
- **批量导入导出** - 支持Excel、CSV格式数据交换
- **质量检查** - 自动去重、格式验证、完整性检查

#### 🕸️ 知识图谱系统
- **图数据库** - 基于Neo4j 5.23的高性能图存储
- **关系网络** - 17,412个复杂关系，多维度关联
- **可视化展示** - 交互式图谱，支持缩放、拖拽、搜索
- **路径查询** - 智能关系推理和路径发现
- **实时更新** - 动态数据同步和图谱刷新

#### 📄 文档解析引擎
- **多格式支持** - Excel、PDF、Word、CSV、TXT
- **智能抽取** - NLP技术自动识别实体和关系
- **结构化处理** - 表格、文本、字段自动解析
- **质量评估** - 完整性、准确性等质量指标
- **批量处理** - 支持大规模文档批量解析

#### 🤖 智能问答系统
- **自然语言** - 支持中文问答和多轮对话
- **上下文理解** - 智能理解用户意图
- **知识推理** - 基于图谱的智能推荐
- **置信度评估** - 答案可信度量化评分

## 🏗️ 技术架构

### 微服务架构
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   前端服务   │◄──►│   API服务   │◄──►│  数据库服务  │
│  Vue.js 3.x │    │  FastAPI    │    │   Neo4j     │
│ Element Plus│    │   Python    │    │   5.23      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 技术栈

#### 前端技术栈
- **Vue.js 3.x** - 渐进式JavaScript框架
- **Element Plus 2.4.4** - Vue 3企业级组件库
- **Vite 5.4.20** - 现代化构建工具
- **Vue Router 4.2.5** - 路由管理
- **Pinia 2.1.7** - 状态管理
- **Axios 1.6.2** - HTTP客户端

#### 可视化组件
- **Cytoscape 3.26.0** - 图谱可视化
- **ECharts 5.4.3** - 图表组件
- **D3.js 7.8.5** - 数据可视化
- **Vue-ECharts 6.6.1** - Vue ECharts集成

#### 后端技术栈
- **FastAPI 2.0.0** - Python Web框架
- **Neo4j 5.23** - 图数据库
- **Redis 7** - 缓存数据库
- **Docker Compose** - 容器编排
- **Nginx** - 反向代理

### 数据模型

#### 词典条目结构
```python
@dataclass
class DictionaryEntry:
    term: str                    # 主术语 (必填)
    aliases: List[str]           # 别名列表 (推荐)
    category: str                # 8大类别 (必填)
    tags: List[str]              # 70标签体系 (推荐)
    definition: str              # 定义/备注 (推荐)
    source: str = "manual"       # 数据来源
    created_at: str = None       # 创建时间
    updated_at: str = None       # 更新时间
    version: int = 1             # 版本号
```

#### 8大核心分类
1. **Symptom** (症状) - 280个术语
2. **TestCase** (测试用例) - 244个术语
3. **Metric** (指标) - 197个术语
4. **Component** (组件) - 194个术语
5. **Process** (流程) - 186个术语
6. **Tool** (工具) - 109个术语
7. **Role** (角色) - 63个术语
8. **Material** (材料) - 55个术语

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- Neo4j 5.23+
- Docker & Docker Compose

### 一键启动（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/xinren1232/KG.git
cd KG

# 2. 启动所有服务
docker-compose up -d

# 3. 访问系统
# 前端界面: http://localhost
# API文档: http://localhost/api/docs
# Neo4j浏览器: http://localhost:7474
```

### 手动部署

#### 后端服务
```bash
# 1. 安装依赖
cd api
pip install -r requirements.txt

# 2. 启动Neo4j
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.23

# 3. 启动API服务
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 前端服务
```bash
# 1. 安装依赖
cd apps/web
npm install

# 2. 构建项目
npm run build

# 3. 启动服务
npm run preview
```

## 📖 使用指南

### 词典管理
1. **访问词典管理页面** - http://localhost/dictionary
2. **搜索术语** - 支持按名称、描述、分类搜索
3. **添加新术语** - 点击"添加词典"按钮
4. **批量导入** - 支持Excel、CSV格式文件
5. **数据导出** - 导出为Excel或CSV格式

### 知识图谱
1. **访问图谱页面** - http://localhost/graph
2. **图谱探索** - 点击节点查看详情，拖拽移动
3. **关系查询** - 搜索特定实体的关系网络
4. **布局切换** - 支持多种图谱布局算法

### 文档解析
1. **访问解析页面** - http://localhost/extraction
2. **上传文档** - 支持多种格式文件
3. **查看结果** - 实时显示解析进度和结果
4. **数据导出** - 将解析结果导出为结构化数据

### 系统管理
1. **访问管理页面** - http://localhost/system
2. **查看统计** - 系统数据统计和健康状态
3. **Schema管理** - 词典和图谱结构管理
4. **版本管理** - 系统版本和更新记录

## 📊 API文档

### 核心API端点

#### 词典管理
```
GET  /kg/dictionary/entries     - 获取词典条目
POST /kg/dictionary/entries     - 创建词典条目
PUT  /kg/dictionary/entries/{id} - 更新词典条目
DELETE /kg/dictionary/entries/{id} - 删除词典条目
GET  /kg/dictionary/stats       - 获取统计信息
GET  /kg/dictionary/categories  - 获取分类信息
```

#### 知识图谱
```
GET /kg/graph              - 获取图谱数据
GET /kg/stats              - 获取图谱统计
GET /kg/entities           - 获取实体统计
GET /kg/relations          - 获取关系统计
```

#### 文档解析
```
POST /documents/upload     - 上传文档
GET  /documents/{id}       - 获取解析结果
POST /documents/extract    - 批量解析
```

### 响应格式
```json
{
  "success": true,
  "data": {
    "entries": [...],
    "total": 1333,
    "page": 1,
    "page_size": 50,
    "total_pages": 27
  }
}
```

## 🔧 配置说明

### 环境变量
```bash
# Neo4j配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# API配置
API_HOST=0.0.0.0
API_PORT=8000
APP_VERSION=v1.3.0

# 前端配置
VITE_API_BASE_URL=http://localhost:8000
```

### Docker配置
```yaml
# docker-compose.yml
version: '3.8'
services:
  neo4j:
    image: neo4j:5.23
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
  
  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - neo4j
  
  web:
    build: ./apps/web
    ports:
      - "80:80"
    depends_on:
      - api
```

## 📈 系统监控

### 健康检查
- **API健康**: http://localhost:8000/health
- **数据库连接**: http://localhost:8000/kg/stats
- **前端状态**: http://localhost/

### 性能指标
- **响应时间**: < 200ms (API调用)
- **数据加载**: < 2s (1000条记录)
- **图谱渲染**: < 3s (500个节点)
- **内存使用**: < 2GB (完整系统)

## 🤝 贡献指南

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 代码规范
- **Python**: 遵循 PEP 8 规范
- **JavaScript**: 使用 ESLint + Prettier
- **Vue**: 遵循 Vue 3 Composition API 规范
- **提交信息**: 使用 Conventional Commits 格式

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- **项目地址**: https://github.com/xinren1232/KG
- **在线演示**: http://47.108.152.16
- **问题反馈**: https://github.com/xinren1232/KG/issues

## 🙏 致谢

感谢以下开源项目的支持：
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Python Web框架
- [Neo4j](https://neo4j.com/) - 图数据库
- [Element Plus](https://element-plus.org/) - Vue 3组件库
- [ECharts](https://echarts.apache.org/) - 数据可视化库

---

**最后更新**: 2025-10-09  
**系统版本**: v1.3.0  
**文档版本**: v2.0
