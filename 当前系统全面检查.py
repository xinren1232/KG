#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
当前系统全面检查 - 分析系统架构、数据模型、服务状态和设计问题
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

def check_project_structure():
    """检查项目结构"""
    print("🏗️ 项目结构分析")
    print("=" * 60)
    
    structure = {}
    
    # 检查根目录
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    root_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    print(f"📁 根目录文件: {len(root_files)}个")
    for file in sorted(root_files):
        print(f"   - {file}")
    
    print(f"\n📂 根目录子目录: {len(root_dirs)}个")
    for dir_name in sorted(root_dirs):
        dir_path = Path(dir_name)
        if dir_path.exists():
            files_count = len(list(dir_path.rglob('*')))
            print(f"   - {dir_name}/ ({files_count}个文件)")
    
    return {"root_files": root_files, "root_dirs": root_dirs}

def check_api_service():
    """检查API服务"""
    print(f"\n🔧 API服务分析")
    print("=" * 60)
    
    api_dir = Path("api")
    if not api_dir.exists():
        print("❌ API目录不存在")
        return None
    
    # 检查API文件结构
    api_files = list(api_dir.rglob('*.py'))
    print(f"📄 Python文件: {len(api_files)}个")
    
    # 检查主要文件
    main_files = ["main.py", "requirements.txt", "Dockerfile"]
    for file in main_files:
        file_path = api_dir / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    # 检查API端点
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ API服务运行正常")
            
            # 获取API信息
            try:
                health_data = response.json()
                print(f"   📊 服务状态: {health_data.get('status', 'unknown')}")
                print(f"   🔗 Neo4j连接: {health_data.get('neo4j', 'unknown')}")
            except:
                pass
        else:
            print(f"   ⚠️ API服务响应异常: {response.status_code}")
    except:
        print(f"   ❌ API服务未运行")
    
    return {"api_files": len(api_files)}

def check_frontend_service():
    """检查前端服务"""
    print(f"\n🌐 前端服务分析")
    print("=" * 60)
    
    frontend_dir = Path("apps/web")
    if not frontend_dir.exists():
        print("❌ 前端目录不存在")
        return None
    
    # 检查前端文件
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        print(f"   ✅ package.json")
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                print(f"   📦 项目名称: {package_data.get('name', 'unknown')}")
                print(f"   🔧 框架: {package_data.get('dependencies', {}).get('vue', 'unknown')}")
        except:
            pass
    else:
        print(f"   ❌ package.json")
    
    # 检查关键目录
    key_dirs = ["src", "public", "node_modules"]
    for dir_name in key_dirs:
        dir_path = frontend_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/")
    
    # 检查前端服务状态
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ 前端服务运行正常")
        else:
            print(f"   ⚠️ 前端服务响应异常: {response.status_code}")
    except:
        print(f"   ❌ 前端服务未运行")
    
    return {"frontend_exists": frontend_dir.exists()}

def check_database_service():
    """检查数据库服务"""
    print(f"\n🗄️ 数据库服务分析")
    print("=" * 60)
    
    # 检查Neo4j连接
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        with driver.session() as session:
            # 检查数据统计
            result = session.run("""
                MATCH (n) 
                RETURN labels(n) as labels, count(n) as count
                ORDER BY count DESC
            """)
            
            print(f"   ✅ Neo4j连接正常")
            print(f"   📊 数据统计:")
            
            total_nodes = 0
            for record in result:
                labels = record["labels"]
                count = record["count"]
                total_nodes += count
                if labels:
                    print(f"      - {':'.join(labels)}: {count}个")
                else:
                    print(f"      - 无标签节点: {count}个")
            
            print(f"   📈 总节点数: {total_nodes}")
            
            # 检查关系统计
            rel_result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC")
            print(f"   🔗 关系统计:")
            total_rels = 0
            for record in rel_result:
                rel_type = record["type"]
                count = record["count"]
                total_rels += count
                print(f"      - {rel_type}: {count}个")
            
            print(f"   📈 总关系数: {total_rels}")
            
        driver.close()
        return {"neo4j_connected": True, "total_nodes": total_nodes, "total_relations": total_rels}
        
    except Exception as e:
        print(f"   ❌ Neo4j连接失败: {e}")
        return {"neo4j_connected": False}

def check_configuration_files():
    """检查配置文件"""
    print(f"\n⚙️ 配置文件分析")
    print("=" * 60)
    
    config_files = [
        "docker-compose.yml",
        "docker-compose.prod.yml", 
        "Dockerfile.api",
        "config/frontend_real_data.json",
        "config/graph_visualization_data.json"
    ]
    
    config_status = {}
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ {config_file}")
            config_status[config_file] = True
        else:
            print(f"   ❌ {config_file}")
            config_status[config_file] = False
    
    return config_status

def check_data_integrity():
    """检查数据完整性"""
    print(f"\n📊 数据完整性分析")
    print("=" * 60)
    
    data_dirs = ["data", "ontology", "exports"]
    data_status = {}
    
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            files = list(Path(data_dir).rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            print(f"   ✅ {data_dir}/: {file_count}个文件")
            data_status[data_dir] = file_count
        else:
            print(f"   ❌ {data_dir}/: 不存在")
            data_status[data_dir] = 0
    
    return data_status

def check_deployment_readiness():
    """检查部署就绪状态"""
    print(f"\n🚀 部署就绪状态分析")
    print("=" * 60)
    
    deployment_items = [
        ("Docker Compose开发", "docker-compose.yml"),
        ("Docker Compose生产", "docker-compose.prod.yml"),
        ("API Dockerfile", "Dockerfile.api"),
        ("Nginx配置", "nginx/nginx.conf"),
        ("部署脚本", "部署脚本.sh"),
        ("服务管理脚本", "全面重启所有服务.py"),
        ("状态检查脚本", "服务状态检查.py")
    ]
    
    deployment_score = 0
    for item_name, file_path in deployment_items:
        if os.path.exists(file_path):
            print(f"   ✅ {item_name}")
            deployment_score += 1
        else:
            print(f"   ❌ {item_name}")
    
    readiness_percentage = (deployment_score / len(deployment_items)) * 100
    print(f"\n   📊 部署就绪度: {readiness_percentage:.1f}% ({deployment_score}/{len(deployment_items)})")
    
    return {"readiness_score": deployment_score, "readiness_percentage": readiness_percentage}

def analyze_system_design():
    """分析系统设计"""
    print(f"\n🎯 系统设计分析")
    print("=" * 60)
    
    design_aspects = {
        "架构模式": "微服务架构 (API + Frontend + Database)",
        "前端技术": "Vue.js + Vite",
        "后端技术": "FastAPI + Python",
        "数据库": "Neo4j图数据库",
        "容器化": "Docker + Docker Compose",
        "反向代理": "Nginx",
        "部署方式": "容器化部署"
    }
    
    for aspect, description in design_aspects.items():
        print(f"   🔧 {aspect}: {description}")
    
    return design_aspects

def generate_system_report():
    """生成系统报告"""
    print(f"\n📋 生成系统全面检查报告")
    print("=" * 80)
    
    report = {
        "检查时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "项目结构": check_project_structure(),
        "API服务": check_api_service(),
        "前端服务": check_frontend_service(),
        "数据库服务": check_database_service(),
        "配置文件": check_configuration_files(),
        "数据完整性": check_data_integrity(),
        "部署就绪": check_deployment_readiness(),
        "系统设计": analyze_system_design()
    }
    
    # 保存报告
    report_file = f"系统全面检查报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 系统检查完成!")
    print(f"📄 报告已保存: {report_file}")
    
    return report

def main():
    """主函数"""
    print("🔍 知识图谱系统全面检查")
    print("=" * 80)
    print(f"🕒 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        report = generate_system_report()
        
        # 总结
        print(f"\n🎯 检查总结")
        print("=" * 80)
        
        # 服务状态总结
        api_ok = report.get("API服务", {}).get("api_files", 0) > 0
        frontend_ok = report.get("前端服务", {}).get("frontend_exists", False)
        db_ok = report.get("数据库服务", {}).get("neo4j_connected", False)
        
        print(f"🔧 核心服务状态:")
        print(f"   - API服务: {'✅ 正常' if api_ok else '❌ 异常'}")
        print(f"   - 前端服务: {'✅ 正常' if frontend_ok else '❌ 异常'}")
        print(f"   - 数据库服务: {'✅ 正常' if db_ok else '❌ 异常'}")
        
        # 部署就绪度
        readiness = report.get("部署就绪", {}).get("readiness_percentage", 0)
        print(f"\n🚀 部署就绪度: {readiness:.1f}%")
        
        if readiness >= 80:
            print("   🟢 系统部署就绪")
        elif readiness >= 60:
            print("   🟡 系统基本就绪，需要完善")
        else:
            print("   🔴 系统需要进一步配置")
        
        # 数据状态
        if db_ok:
            nodes = report.get("数据库服务", {}).get("total_nodes", 0)
            relations = report.get("数据库服务", {}).get("total_relations", 0)
            print(f"\n📊 数据状态:")
            print(f"   - 节点数量: {nodes:,}")
            print(f"   - 关系数量: {relations:,}")
        
    except Exception as e:
        print(f"❌ 检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
