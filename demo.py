#!/usr/bin/env python3
"""
项目演示脚本
展示当前已完成的功能
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """打印横幅"""
    print("=" * 70)
    print("📱 质量知识图谱助手 - 项目演示")
    print("=" * 70)
    print()

def check_project_status():
    """检查项目状态"""
    print("🔍 检查项目状态...")
    
    # 检查关键文件
    key_files = [
        "README.md",
        "services/api/main_simple.py",
        "apps/web/package.json",
        "apps/web/src/App.vue",
        "data/raw/测试用例样本数据.xlsx",
        "data/raw/异常数据样本.xlsx"
    ]
    
    missing_files = []
    for file_path in key_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少关键文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ 项目文件完整")
    return True

def show_project_structure():
    """显示项目结构"""
    print("\n📁 项目结构:")
    print("""
KG/
├── 📄 README.md                    # 项目说明
├── 🐳 docker-compose.yml           # 容器配置
├── ⚙️  .env                        # 环境变量
├── 📚 docs/                        # 文档
│   └── knowledge_schema.md         # 知识图谱设计
├── 🔧 services/                    # 后端服务
│   ├── api/                        # FastAPI服务
│   │   ├── main.py                 # 完整版API
│   │   ├── main_simple.py          # 简化版API ✨
│   │   ├── database/               # 数据库客户端
│   │   ├── models/                 # 数据模型
│   │   └── routers/                # API路由
│   └── etl/                        # ETL数据处理
│       └── excel_processor.py      # Excel导入器
├── 🌐 apps/                        # 前端应用
│   └── web/                        # Vue3应用 ✨
│       ├── src/
│       │   ├── App.vue             # 主应用
│       │   ├── views/              # 页面组件
│       │   └── api/                # API调用
│       └── package.json            # 依赖配置
└── 📊 data/                        # 数据文件
    └── raw/                        # 示例数据 ✨
        ├── 测试用例样本数据.xlsx
        └── 异常数据样本.xlsx
    """)

def show_features():
    """显示功能特性"""
    print("\n🎯 已实现的功能:")
    print("""
1. 📋 测试流程查询
   - 根据产品和组件查询测试用例
   - 支持优先级和类型筛选
   - 详细的测试步骤和期望结果

2. 🔍 异常指导分析
   - 输入症状描述，获取相关异常
   - 展示完整的因果路径：症状→根因→对策
   - 智能的异常匹配和建议

3. 🕸️ 知识图谱可视化
   - 交互式图谱探索
   - 多种布局算法
   - 节点详情和关系查看

4. 📊 系统监控面板
   - 实时系统状态检查
   - 数据统计和健康监控
   - 快速功能导航
    """)

def show_tech_stack():
    """显示技术栈"""
    print("\n🛠️ 技术栈:")
    print("""
后端:
  • FastAPI - 现代Python Web框架
  • Neo4j - 图数据库（可选）
  • Pydantic - 数据验证和序列化
  • pandas - 数据处理

前端:
  • Vue 3 - 渐进式JavaScript框架
  • Element Plus - Vue组件库
  • Cytoscape.js - 图可视化
  • Axios - HTTP客户端

数据:
  • Excel - 数据导入格式
  • JSON - API数据交换
  • Cypher - 图查询语言
    """)

def show_demo_instructions():
    """显示演示说明"""
    print("\n🚀 演示说明:")
    print("""
当前可以演示的功能（无需Neo4j）:

1. 启动简化版API:
   cd services/api
   python -m uvicorn main_simple:app --reload --port 8000

2. 查看API文档:
   http://localhost:8000/docs

3. 启动前端应用（如果有Node.js）:
   cd apps/web
   npm install
   npm run dev
   http://localhost:5173

4. 测试功能:
   - 产品和组件查询
   - 测试用例检索
   - 异常症状分析
   - 图谱数据可视化

注意: 当前使用模拟数据，完整功能需要Neo4j数据库
    """)

def show_next_steps():
    """显示后续步骤"""
    print("\n📋 后续开发计划:")
    print("""
阶段1 - 基础完善:
  ✅ 项目架构搭建
  ✅ API服务开发
  ✅ 前端界面实现
  ✅ 基础功能验证

阶段2 - 数据集成:
  🔄 Neo4j数据库集成
  🔄 Excel数据导入优化
  🔄 真实数据测试

阶段3 - 智能增强:
  ⏳ LLM三元组抽取
  ⏳ 相似异常检索
  ⏳ 智能问答功能

阶段4 - 生产部署:
  ⏳ 容器化部署
  ⏳ 权限管理
  ⏳ 性能优化
    """)

def main():
    """主函数"""
    print_banner()
    
    if not check_project_status():
        print("\n❌ 项目状态检查失败，请确保在正确的目录运行")
        return
    
    show_project_structure()
    show_features()
    show_tech_stack()
    show_demo_instructions()
    show_next_steps()
    
    print("\n" + "=" * 70)
    print("🎉 项目演示完成！")
    print("📖 详细信息请查看: README.md 和 项目进展总结.md")
    print("🔗 API文档: http://localhost:8000/docs (启动API后)")
    print("🌐 前端应用: http://localhost:5173 (启动前端后)")
    print("=" * 70)

if __name__ == "__main__":
    main()
