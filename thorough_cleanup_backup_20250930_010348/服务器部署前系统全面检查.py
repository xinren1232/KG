#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器部署前系统全面检查和优化建议
包括数据保存形式、架构设计、性能优化等
"""

import os
import json
import psutil
import requests
from pathlib import Path
from datetime import datetime
from neo4j import GraphDatabase

def check_data_storage_optimization():
    """检查数据存储优化需求"""
    print("📊 数据存储优化检查")
    print("=" * 50)
    
    # 1. 检查当前数据文件大小和分布
    data_files = {
        "Neo4j数据": "neo4j_standalone/data" if Path("neo4j_standalone/data").exists() else "N/A",
        "词典数据": "data/dictionary.json",
        "上传文件": "api/uploads",
        "缓存数据": "api/cache",
        "备份数据": "data_backup",
        "导出数据": "exports"
    }
    
    total_size = 0
    print("📁 当前数据文件分布:")
    
    for name, path in data_files.items():
        if path != "N/A" and Path(path).exists():
            if Path(path).is_file():
                size = Path(path).stat().st_size
                size_mb = size / (1024 * 1024)
                print(f"   {name}: {size_mb:.2f} MB ({path})")
                total_size += size
            elif Path(path).is_dir():
                dir_size = sum(f.stat().st_size for f in Path(path).rglob('*') if f.is_file())
                size_mb = dir_size / (1024 * 1024)
                print(f"   {name}: {size_mb:.2f} MB ({path}/)")
                total_size += dir_size
        else:
            print(f"   {name}: 不存在 ({path})")
    
    total_mb = total_size / (1024 * 1024)
    print(f"\n📊 总数据大小: {total_mb:.2f} MB")
    
    # 2. 数据存储优化建议
    print("\n💡 数据存储优化建议:")
    
    if total_mb > 100:
        print("   🔴 数据量较大，建议优化:")
        print("     - 实施数据压缩")
        print("     - 分离热数据和冷数据")
        print("     - 考虑对象存储(S3/OSS)")
    elif total_mb > 50:
        print("   🟡 数据量中等，建议:")
        print("     - 定期清理临时文件")
        print("     - 实施数据归档策略")
    else:
        print("   🟢 数据量适中，当前存储方式可行")
    
    return total_mb

def check_database_optimization():
    """检查数据库优化需求"""
    print("\n🗄️ 数据库优化检查")
    print("=" * 50)
    
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        
        with driver.session() as session:
            # 1. 检查数据库大小和性能
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            
            print(f"📊 数据库规模:")
            print(f"   节点数量: {node_count:,}")
            print(f"   关系数量: {rel_count:,}")
            
            # 2. 检查索引使用情况
            indexes = session.run("SHOW INDEXES").data()
            print(f"\n🔍 索引状态:")
            print(f"   索引数量: {len(indexes)}")
            
            for idx in indexes[:5]:  # 显示前5个索引
                name = idx.get('name', 'N/A')
                state = idx.get('state', 'N/A')
                print(f"   - {name}: {state}")
            
            # 3. 检查约束
            constraints = session.run("SHOW CONSTRAINTS").data()
            print(f"\n🔒 约束状态:")
            print(f"   约束数量: {len(constraints)}")
            
            # 4. 性能优化建议
            print(f"\n💡 数据库优化建议:")
            
            if node_count > 10000:
                print("   🔴 大规模数据，建议:")
                print("     - 添加必要的索引")
                print("     - 实施查询优化")
                print("     - 考虑数据分片")
                print("     - 增加内存配置")
            elif node_count > 1000:
                print("   🟡 中等规模，建议:")
                print("     - 优化常用查询")
                print("     - 添加关键索引")
            else:
                print("   🟢 小规模数据，当前配置足够")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def check_system_architecture():
    """检查系统架构优化需求"""
    print("\n🏗️ 系统架构检查")
    print("=" * 50)
    
    # 1. 检查当前架构组件
    components = {
        "前端服务": {"port": 5173, "type": "Vue.js + Vite"},
        "API服务": {"port": 8000, "type": "FastAPI"},
        "数据库": {"port": 7687, "type": "Neo4j"},
        "Web界面": {"port": 7474, "type": "Neo4j Browser"}
    }
    
    print("🔧 当前架构组件:")
    running_services = 0
    
    for name, config in components.items():
        port = config["port"]
        service_type = config["type"]
        
        # 检查端口是否开放
        port_open = False
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                port_open = True
                break
        
        status = "✅ 运行中" if port_open else "❌ 未运行"
        print(f"   {name} ({service_type}): {status} (:{port})")
        
        if port_open:
            running_services += 1
    
    # 2. 架构优化建议
    print(f"\n💡 架构优化建议:")
    
    print("   📦 容器化部署:")
    print("     - 使用Docker容器化所有服务")
    print("     - 编写docker-compose.yml")
    print("     - 实现一键部署")
    
    print("   🔄 负载均衡:")
    print("     - 使用Nginx反向代理")
    print("     - 实现API负载均衡")
    print("     - 静态资源CDN")
    
    print("   🔒 安全加固:")
    print("     - HTTPS证书配置")
    print("     - API认证和授权")
    print("     - 数据库访问控制")
    
    return running_services == len(components)

def check_performance_optimization():
    """检查性能优化需求"""
    print("\n⚡ 性能优化检查")
    print("=" * 50)
    
    # 1. 检查系统资源使用
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('.')
    
    print("💻 系统资源使用:")
    print(f"   CPU使用率: {cpu_percent:.1f}%")
    print(f"   内存使用: {memory.percent:.1f}% ({memory.used//1024//1024} MB / {memory.total//1024//1024} MB)")
    print(f"   磁盘使用: {disk.percent:.1f}% ({disk.used//1024//1024//1024} GB / {disk.total//1024//1024//1024} GB)")
    
    # 2. 检查API响应时间
    print("\n🌐 API性能测试:")
    
    api_endpoints = [
        "/health",
        "/kg/real-stats",
        "/kg/stats"
    ]
    
    for endpoint in api_endpoints:
        try:
            start_time = datetime.now()
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds() * 1000
            status = "✅" if response.status_code == 200 else "❌"
            
            print(f"   {endpoint}: {status} {response_time:.0f}ms")
            
        except Exception as e:
            print(f"   {endpoint}: ❌ 超时/错误")
    
    # 3. 性能优化建议
    print(f"\n💡 性能优化建议:")
    
    if cpu_percent > 80:
        print("   🔴 CPU使用率高，建议:")
        print("     - 优化算法复杂度")
        print("     - 实施异步处理")
        print("     - 增加CPU核心")
    
    if memory.percent > 80:
        print("   🔴 内存使用率高，建议:")
        print("     - 实施内存缓存优化")
        print("     - 减少内存泄漏")
        print("     - 增加内存容量")
    
    if disk.percent > 80:
        print("   🔴 磁盘使用率高，建议:")
        print("     - 清理临时文件")
        print("     - 实施数据归档")
        print("     - 扩展存储空间")
    
    print("   ⚡ 通用性能优化:")
    print("     - 实施Redis缓存")
    print("     - 数据库连接池")
    print("     - 异步任务队列")
    print("     - 静态资源压缩")

def generate_deployment_recommendations():
    """生成部署建议"""
    print("\n🚀 服务器部署建议")
    print("=" * 50)
    
    print("📋 部署前准备清单:")
    
    print("\n1. 🗄️ 数据迁移策略:")
    print("   ✅ 导出Neo4j数据库")
    print("   ✅ 备份词典和配置文件")
    print("   ✅ 准备数据恢复脚本")
    
    print("\n2. 🔧 环境配置:")
    print("   ✅ 生产环境配置文件")
    print("   ✅ 环境变量管理")
    print("   ✅ 日志配置优化")
    
    print("\n3. 🔒 安全配置:")
    print("   ✅ 防火墙规则")
    print("   ✅ SSL证书")
    print("   ✅ 数据库密码")
    print("   ✅ API密钥管理")
    
    print("\n4. 📦 容器化:")
    print("   ✅ Dockerfile编写")
    print("   ✅ docker-compose配置")
    print("   ✅ 镜像构建测试")
    
    print("\n5. 🔄 CI/CD:")
    print("   ✅ 自动化部署脚本")
    print("   ✅ 健康检查")
    print("   ✅ 回滚策略")
    
    print("\n6. 📊 监控告警:")
    print("   ✅ 系统监控")
    print("   ✅ 应用监控")
    print("   ✅ 日志聚合")

def create_optimization_scripts():
    """创建优化脚本"""
    print("\n📝 生成优化脚本")
    print("=" * 50)
    
    # 1. 数据备份脚本
    backup_script = '''#!/bin/bash
# 数据备份脚本

echo "🔄 开始数据备份..."

# 创建备份目录
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# 备份Neo4j数据
echo "📊 备份Neo4j数据..."
neo4j-admin dump --database=neo4j --to=$BACKUP_DIR/neo4j_backup.dump

# 备份应用数据
echo "📁 备份应用数据..."
cp -r data/ $BACKUP_DIR/
cp -r config/ $BACKUP_DIR/
cp docker-compose.yml $BACKUP_DIR/

echo "✅ 备份完成: $BACKUP_DIR"
'''
    
    with open("backup_data.sh", "w") as f:
        f.write(backup_script)
    
    # 2. 性能优化配置
    neo4j_config = '''# Neo4j性能优化配置
# 内存设置
server.memory.heap.initial_size=2g
server.memory.heap.max_size=4g
server.memory.pagecache.size=2g

# 连接设置
server.bolt.thread_pool_min_size=5
server.bolt.thread_pool_max_size=400

# 查询优化
cypher.default_language_version=5
cypher.hints_error=true
'''
    
    with open("neo4j_production.conf", "w") as f:
        f.write(neo4j_config)
    
    print("💾 已生成优化脚本:")
    print("   - backup_data.sh (数据备份)")
    print("   - neo4j_production.conf (Neo4j优化配置)")

def main():
    """主函数"""
    print("🔍 服务器部署前系统全面检查")
    print("=" * 60)
    print(f"🕒 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 数据存储检查
    data_size = check_data_storage_optimization()
    
    # 2. 数据库优化检查
    db_ok = check_database_optimization()
    
    # 3. 系统架构检查
    arch_ok = check_system_architecture()
    
    # 4. 性能优化检查
    check_performance_optimization()
    
    # 5. 部署建议
    generate_deployment_recommendations()
    
    # 6. 生成优化脚本
    create_optimization_scripts()
    
    # 7. 总结报告
    print("\n📋 检查总结")
    print("=" * 50)
    
    print(f"📊 数据规模: {data_size:.1f} MB")
    print(f"🗄️ 数据库状态: {'✅ 正常' if db_ok else '❌ 需要优化'}")
    print(f"🏗️ 架构状态: {'✅ 完整' if arch_ok else '❌ 不完整'}")
    
    print(f"\n🎯 部署就绪度评估:")
    
    ready_score = 0
    if data_size < 100: ready_score += 25
    if db_ok: ready_score += 25
    if arch_ok: ready_score += 25
    ready_score += 25  # 基础分
    
    if ready_score >= 90:
        print("   🟢 高度就绪 - 可以开始部署")
    elif ready_score >= 70:
        print("   🟡 基本就绪 - 建议先优化")
    else:
        print("   🔴 需要优化 - 建议完善后部署")
    
    print(f"\n📈 就绪度得分: {ready_score}/100")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断检查")
    except Exception as e:
        print(f"\n❌ 检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
