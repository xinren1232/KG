#!/usr/bin/env python3
"""
项目结构检查脚本
检查项目文件是否创建完整
"""

import os
from pathlib import Path

def check_project_structure():
    """检查项目结构"""
    print("🔍 检查项目结构...")
    
    # 定义期望的文件和目录结构
    expected_structure = {
        "files": [
            "README.md",
            "docker-compose.yml", 
            ".env",
            ".env.example",
            "docs/knowledge_schema.md",
            "services/api/Dockerfile",
            "services/api/requirements.txt",
            "services/api/main.py",
            "services/api/database/neo4j_client.py",
            "services/api/models/schemas.py",
            "services/api/routers/health_router.py",
            "services/api/routers/kg_router.py",
            "services/api/neo4j_init/neo4j_constraints.cypher",
            "services/api/neo4j_init/sample_data.cypher",
            "services/etl/Dockerfile",
            "services/etl/requirements.txt"
        ],
        "directories": [
            "apps/web",
            "services/api",
            "services/etl", 
            "data/raw",
            "data/processed",
            "data/neo4j",
            "docs"
        ]
    }
    
    # 检查目录
    print("\n📁 检查目录:")
    for directory in expected_structure["directories"]:
        if os.path.exists(directory):
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory}")
    
    # 检查文件
    print("\n📄 检查文件:")
    for file_path in expected_structure["files"]:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path}")
    
    print("\n📊 项目统计:")
    total_dirs = len(expected_structure["directories"])
    existing_dirs = sum(1 for d in expected_structure["directories"] if os.path.exists(d))
    
    total_files = len(expected_structure["files"])
    existing_files = sum(1 for f in expected_structure["files"] if os.path.exists(f))
    
    print(f"  目录: {existing_dirs}/{total_dirs} ({existing_dirs/total_dirs*100:.1f}%)")
    print(f"  文件: {existing_files}/{total_files} ({existing_files/total_files*100:.1f}%)")
    
    if existing_dirs == total_dirs and existing_files == total_files:
        print("\n🎉 项目结构完整！")
        return True
    else:
        print("\n⚠️  项目结构不完整，请检查缺失的文件和目录")
        return False

def show_next_steps():
    """显示下一步操作建议"""
    print("\n🚀 下一步操作建议:")
    print("1. 启动后端服务:")
    print("   docker compose up -d neo4j")
    print("   等待Neo4j启动完成后:")
    print("   docker compose up -d api")
    print()
    print("2. 初始化数据库:")
    print("   docker exec -it kg_neo4j cypher-shell -u neo4j -p password123 -f /import/neo4j_constraints.cypher")
    print("   docker exec -it kg_neo4j cypher-shell -u neo4j -p password123 -f /import/sample_data.cypher")
    print()
    print("3. 测试API:")
    print("   访问 http://localhost:8000/docs 查看API文档")
    print("   访问 http://localhost:7474 查看Neo4j控制台")
    print()
    print("4. 创建前端应用:")
    print("   cd apps/web")
    print("   npm create vue@latest . (选择Vue3 + TypeScript + Router)")
    print("   npm install")
    print("   npm run dev")

if __name__ == "__main__":
    print("=" * 60)
    print("📱 质量知识图谱助手 - 项目检查")
    print("=" * 60)
    
    is_complete = check_project_structure()
    
    if is_complete:
        show_next_steps()
    
    print("\n" + "=" * 60)
