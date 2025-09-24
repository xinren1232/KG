# 📱 知识图谱构建助手

> 基于先进NLP技术和知识图谱技术的智能文档解析与知识构建系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue 3](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-red.svg)](https://fastapi.tiangolo.com/)

## 🎯 项目简介

知识图谱构建助手是一个专业的企业级系统，专注于从非结构化文档中智能抽取知识并构建领域知识图谱。系统支持多种文档格式，提供完整的数据治理体系，帮助企业实现知识资产的数字化管理。

### ✨ 核心特性

- 🔍 **智能文档解析** - 支持Excel、PDF、Word、CSV、TXT等多种格式
- 🧠 **知识自动抽取** - 基于NLP技术的实体和关系抽取
- 🕸️ **知识图谱构建** - 自动化图谱构建和推理分析
- 📚 **词典标准化管理** - 支持别名映射和分类管理
- 🏛️ **数据治理体系** - 完整的质量监控和持续优化
- 🎨 **现代化界面** - 基于Vue3的响应式用户界面

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/xinren1232/KG.git
cd KG
```

2. **安装Python依赖**
```bash
pip install fastapi uvicorn pydantic pandas openpyxl python-docx PyPDF2 spacy networkx
```

3. **安装前端依赖**
```bash
cd apps/web
npm install
```

4. **启动后端服务**
```bash
cd ../../
python api/simple_api.py
```

5. **启动前端应用**
```bash
cd apps/web
npm run dev
```

6. **访问应用**
- 前端应用: http://localhost:5175
- API文档: http://127.0.0.1:8000/docs

## 📖 使用指南

### 1. 文档解析
- 上传Excel、PDF、Word等文档
- 系统自动识别文档结构
- 智能抽取实体和关系
- 实时查看抽取结果

### 2. 知识图谱
- 可视化浏览图谱结构
- 交互式节点探索
- 多种查询方式支持
- 图谱统计分析

### 3. 词典管理
- 标准化词典维护
- 别名映射管理
- 分类筛选和搜索
- 批量导入导出

### 4. 数据治理
- 数据质量监控
- 治理规则管理
- 改进建议生成
- 持续优化支持

## 🏗️ 系统架构

```
📱 知识图谱构建助手
├── 🌐 API服务层 (FastAPI)
│   ├── 文档上传与解析
│   ├── 知识抽取与构建
│   ├── 图谱查询与管理
│   └── 词典与治理接口
├── 🖥️ 前端应用层 (Vue3)
│   ├── 文档解析界面
│   ├── 图谱可视化
│   ├── 词典管理
│   └── 数据治理
├── 🧠 智能处理层
│   ├── NLP实体抽取
│   ├── 关系推理
│   ├── 数据标准化
│   └── 质量评估
└── 🏛️ 数据治理层
    ├── 异常标签管理
    ├── 组件词典维护
    ├── 供应商档案
    └── 质量监控
```

## 📁 项目结构

```
KG/
├── api/                          # 后端API服务
├── apps/web/                     # 前端Vue应用
├── services/                     # 核心服务模块
│   ├── nlp/                     # NLP处理服务
│   ├── governance/              # 数据治理服务
│   └── reasoning/               # 推理引擎
├── graph/                       # 图谱本体设计
├── data/                        # 数据存储目录
├── docs/                        # 项目文档
├── PROGRESS.md                  # 建设进度
└── README.md                    # 项目说明
```

## 🔧 开发指南

### API开发
- 基于FastAPI框架
- 遵循RESTful设计原则
- 统一的错误处理机制
- 完整的API文档

### 前端开发
- Vue3 + Composition API
- Element Plus UI组件库
- Vite构建工具
- 响应式设计

### 数据处理
- pandas数据处理
- spaCy NLP处理
- NetworkX图算法
- 多格式文档解析

## 🧪 测试

```bash
# 运行系统状态检查
python system_status_check.py

# 前端开发服务器
cd apps/web
npm run dev

# API服务测试
python api/simple_api.py
```

## 📊 性能指标

- **文档处理**: 支持10MB以下文档快速解析
- **实体抽取**: 准确率>90%，支持13种实体类型
- **图谱构建**: 支持万级节点的知识图谱
- **查询响应**: 毫秒级API响应时间
- **并发支持**: 支持多用户同时使用

## 🤝 贡献

我们欢迎所有形式的贡献！

### 贡献方式
- 🐛 报告Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- 🐛 Issues: [GitHub Issues](https://github.com/xinren1232/KG/issues)
- 📖 文档: [项目Wiki](https://github.com/xinren1232/KG/wiki)

## 🙏 致谢

感谢以下开源项目的支持：
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Element Plus](https://element-plus.org/) - Vue3 UI组件库
- [spaCy](https://spacy.io/) - 工业级NLP库
- [NetworkX](https://networkx.org/) - Python图分析库

---

**⭐ 如果这个项目对你有帮助，请给我们一个Star！**

**📋 详细的建设进度和技术文档请查看 [PROGRESS.md](PROGRESS.md)**
