#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH部署演示脚本
展示部署配置和流程
"""

import json
import os
from pathlib import Path

def show_deployment_demo():
    """展示部署演示"""
    print("🚀 知识图谱系统 SSH 部署演示")
    print("=" * 60)
    
    # 检查部署文件
    deployment_files = {
        "ssh_deploy.py": "Python自动化部署脚本",
        "ssh_deploy.sh": "Shell脚本部署 (Linux/macOS)",
        "ssh_deploy.bat": "批处理部署 (Windows)",
        "deploy_config.json": "部署配置文件",
        "SSH部署指南.md": "详细部署指南"
    }
    
    print("📁 部署文件检查:")
    for file_name, description in deployment_files.items():
        if os.path.exists(file_name):
            print(f"   ✅ {file_name} - {description}")
        else:
            print(f"   ❌ {file_name} - {description} (缺失)")
    
    print("\n📋 部署配置示例:")
    
    # 显示配置示例
    config_example = {
        "server": {
            "host": "192.168.1.100",
            "port": 22,
            "username": "ubuntu",
            "password": "",
            "key_file": "C:\\Users\\用户名\\.ssh\\id_rsa",
            "timeout": 30
        },
        "deployment": {
            "remote_path": "/opt/knowledge-graph",
            "backup_path": "/opt/kg-backups",
            "services": ["neo4j", "redis", "api", "web", "prometheus", "grafana"]
        }
    }
    
    print(json.dumps(config_example, indent=2, ensure_ascii=False))
    
    print("\n🔧 部署命令示例:")
    print("\n1. Python自动化部署:")
    print("   # 编辑 deploy_config.json 配置文件")
    print("   python ssh_deploy.py")
    
    print("\n2. Shell脚本部署 (Linux/macOS):")
    print("   chmod +x ssh_deploy.sh")
    print("   ./ssh_deploy.sh --host 192.168.1.100 --user ubuntu --key ~/.ssh/id_rsa")
    
    print("\n3. Windows批处理部署:")
    print("   ssh_deploy.bat --host 192.168.1.100 --user ubuntu --key C:\\Users\\用户名\\.ssh\\id_rsa")
    
    print("\n📊 部署流程:")
    deployment_steps = [
        "🔍 测试SSH连接",
        "📦 创建部署包",
        "📤 上传到服务器",
        "💾 备份现有部署",
        "🔧 安装系统依赖",
        "🚀 部署主服务",
        "⚡ 优化数据库",
        "📊 部署监控",
        "🔍 验证部署",
        "📋 显示访问信息"
    ]
    
    for i, step in enumerate(deployment_steps, 1):
        print(f"   {i:2d}. {step}")
    
    print("\n🌐 部署后访问地址:")
    services = [
        ("Neo4j浏览器", "http://服务器IP:7474"),
        ("API服务", "http://服务器IP:8000"),
        ("API文档", "http://服务器IP:8000/docs"),
        ("健康检查", "http://服务器IP:8000/health"),
        ("Prometheus", "http://服务器IP:9090"),
        ("Grafana", "http://服务器IP:3000")
    ]
    
    for service_name, url in services:
        print(f"   • {service_name:12s}: {url}")
    
    print("\n🔑 认证信息:")
    print("   • Neo4j:    用户名: neo4j, 密码: password123")
    print("   • Grafana:  用户名: admin, 密码: admin123")
    
    print("\n📋 服务器要求:")
    requirements = [
        "操作系统: Ubuntu 18.04+, CentOS 7+, Debian 9+",
        "内存: 最少4GB，推荐8GB+",
        "磁盘: 最少20GB可用空间",
        "网络: 开放端口 22, 7474, 8000, 9090, 3000",
        "权限: SSH访问权限, sudo权限"
    ]
    
    for requirement in requirements:
        print(f"   • {requirement}")
    
    print("\n🛠️ 本地环境要求:")
    local_requirements = [
        "SSH客户端 (OpenSSH或Git Bash)",
        "Python 3.7+ (使用Python部署脚本)",
        "paramiko库 (pip install paramiko)"
    ]
    
    for requirement in local_requirements:
        print(f"   • {requirement}")
    
    print("\n🔧 快速开始:")
    print("   1. 编辑 deploy_config.json 配置服务器信息")
    print("   2. 确保SSH连接正常: ssh username@server_ip")
    print("   3. 运行部署脚本: python ssh_deploy.py")
    print("   4. 等待部署完成，访问服务地址")
    
    print("\n📚 详细文档:")
    print("   查看 SSH部署指南.md 获取完整部署说明")
    
    print("\n" + "=" * 60)
    print("🎉 SSH部署工具已准备就绪！")

def check_deployment_readiness():
    """检查部署就绪状态"""
    print("\n🔍 部署就绪状态检查:")
    
    checks = []
    
    # 检查部署脚本
    if os.path.exists("ssh_deploy.py"):
        checks.append(("✅", "Python部署脚本"))
    else:
        checks.append(("❌", "Python部署脚本"))
    
    # 检查配置文件
    if os.path.exists("deploy_config.json"):
        checks.append(("✅", "部署配置文件"))
        
        # 检查配置内容
        try:
            with open("deploy_config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
                if config["server"]["host"] and config["server"]["host"] != "your-server-ip":
                    checks.append(("✅", "服务器地址已配置"))
                else:
                    checks.append(("⚠️", "服务器地址需要配置"))
                
                if config["server"]["username"] and config["server"]["username"] != "your-username":
                    checks.append(("✅", "SSH用户名已配置"))
                else:
                    checks.append(("⚠️", "SSH用户名需要配置"))
        except:
            checks.append(("❌", "配置文件格式错误"))
    else:
        checks.append(("❌", "部署配置文件"))
    
    # 检查Docker配置
    if os.path.exists("docker-compose.yml"):
        checks.append(("✅", "Docker Compose配置"))
    else:
        checks.append(("❌", "Docker Compose配置"))
    
    # 检查监控配置
    if os.path.exists("docker-compose.monitoring.yml"):
        checks.append(("✅", "监控服务配置"))
    else:
        checks.append(("❌", "监控服务配置"))
    
    # 检查API代码
    if os.path.exists("api/main.py"):
        checks.append(("✅", "API服务代码"))
    else:
        checks.append(("❌", "API服务代码"))
    
    # 检查前端代码
    if os.path.exists("apps/web"):
        checks.append(("✅", "前端应用代码"))
    else:
        checks.append(("❌", "前端应用代码"))
    
    # 检查优化脚本
    if os.path.exists("scripts/optimize_neo4j.py"):
        checks.append(("✅", "数据库优化脚本"))
    else:
        checks.append(("❌", "数据库优化脚本"))
    
    # 显示检查结果
    for status, item in checks:
        print(f"   {status} {item}")
    
    # 计算就绪度
    ready_count = sum(1 for status, _ in checks if status == "✅")
    total_count = len(checks)
    readiness = (ready_count / total_count) * 100
    
    print(f"\n📊 部署就绪度: {ready_count}/{total_count} ({readiness:.1f}%)")
    
    if readiness >= 90:
        print("🎉 系统已准备好进行SSH部署！")
    elif readiness >= 70:
        print("⚠️ 系统基本就绪，建议完善配置后部署")
    else:
        print("❌ 系统未就绪，请检查缺失的组件")
    
    return readiness >= 70

def main():
    """主函数"""
    show_deployment_demo()
    
    if check_deployment_readiness():
        print("\n💡 下一步操作:")
        print("   1. 编辑 deploy_config.json 配置服务器信息")
        print("   2. 测试SSH连接: ssh username@server_ip")
        print("   3. 执行部署: python ssh_deploy.py")
    else:
        print("\n💡 需要完成的准备工作:")
        print("   1. 确保所有必要文件存在")
        print("   2. 配置服务器连接信息")
        print("   3. 准备SSH认证 (密钥或密码)")

if __name__ == "__main__":
    main()
