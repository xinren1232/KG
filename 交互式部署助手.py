#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式SSH部署助手
帮助用户配置和完成部署
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """显示横幅"""
    print("🚀 知识图谱系统 - 交互式SSH部署助手")
    print("=" * 60)
    print("本工具将帮助您配置服务器信息并完成自动化部署")
    print("=" * 60)

def check_prerequisites():
    """检查前置条件"""
    print("\n🔍 检查部署前置条件...")
    
    issues = []
    
    # 检查SSH客户端
    try:
        result = subprocess.run(['ssh', '-V'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ SSH客户端已安装")
        else:
            issues.append("SSH客户端未正确安装")
    except FileNotFoundError:
        issues.append("SSH客户端未安装，请安装OpenSSH或Git Bash")
    
    # 检查Python依赖
    try:
        import paramiko
        print("   ✅ paramiko库已安装")
    except ImportError:
        issues.append("paramiko库未安装，请运行: pip install paramiko")
    
    # 检查部署脚本
    if os.path.exists("ssh_deploy.py"):
        print("   ✅ SSH部署脚本存在")
    else:
        issues.append("ssh_deploy.py文件缺失")
    
    # 检查Docker配置
    if os.path.exists("docker-compose.yml"):
        print("   ✅ Docker Compose配置存在")
    else:
        issues.append("docker-compose.yml文件缺失")
    
    if issues:
        print("\n❌ 发现以下问题:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("   ✅ 所有前置条件满足")
        return True

def get_user_input(prompt, default="", required=True):
    """获取用户输入"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        else:
            print("   ❌ 此项为必填项，请输入有效值")

def get_yes_no(prompt, default=True):
    """获取是/否输入"""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        if not response:
            return default
        elif response in ['y', 'yes', '是']:
            return True
        elif response in ['n', 'no', '否']:
            return False
        else:
            print("   请输入 y/yes/是 或 n/no/否")

def configure_server():
    """配置服务器信息"""
    print("\n📋 配置服务器连接信息")
    print("-" * 40)
    
    config = {
        "server": {
            "host": "",
            "port": 22,
            "username": "",
            "password": "",
            "key_file": "",
            "timeout": 30
        },
        "deployment": {
            "remote_path": "/opt/knowledge-graph",
            "backup_path": "/opt/kg-backups",
            "docker_compose_file": "docker-compose.yml",
            "monitoring_compose_file": "docker-compose.monitoring.yml",
            "services": ["neo4j", "redis", "api", "web", "prometheus", "grafana"]
        }
    }
    
    # 服务器地址
    config["server"]["host"] = get_user_input("请输入服务器IP地址或域名")
    
    # SSH端口
    port_input = get_user_input("请输入SSH端口", "22", False)
    if port_input:
        try:
            config["server"]["port"] = int(port_input)
        except ValueError:
            print("   ⚠️ 端口格式错误，使用默认端口22")
            config["server"]["port"] = 22
    
    # SSH用户名
    config["server"]["username"] = get_user_input("请输入SSH用户名")
    
    # 认证方式选择
    print("\n🔑 选择SSH认证方式:")
    print("   1. SSH密钥认证 (推荐)")
    print("   2. 密码认证")
    
    auth_choice = get_user_input("请选择认证方式 (1/2)", "1")
    
    if auth_choice == "1":
        # SSH密钥路径
        default_key_paths = [
            os.path.expanduser("~/.ssh/id_rsa"),
            os.path.expanduser("~/.ssh/id_ed25519"),
            "C:\\Users\\{}\\.ssh\\id_rsa".format(os.getenv('USERNAME', 'user'))
        ]
        
        suggested_key = None
        for key_path in default_key_paths:
            if os.path.exists(key_path):
                suggested_key = key_path
                break
        
        if suggested_key:
            use_suggested = get_yes_no(f"找到SSH密钥文件: {suggested_key}，是否使用?")
            if use_suggested:
                config["server"]["key_file"] = suggested_key
            else:
                config["server"]["key_file"] = get_user_input("请输入SSH密钥文件路径")
        else:
            config["server"]["key_file"] = get_user_input("请输入SSH密钥文件路径")
        
        # 验证密钥文件
        if config["server"]["key_file"] and not os.path.exists(config["server"]["key_file"]):
            print(f"   ⚠️ 警告: 密钥文件不存在: {config['server']['key_file']}")
            if not get_yes_no("是否继续?", False):
                return None
    else:
        # 密码认证
        import getpass
        config["server"]["password"] = getpass.getpass("请输入SSH密码: ")
    
    # 部署路径配置
    print("\n📁 配置部署路径:")
    remote_path = get_user_input("远程部署路径", "/opt/knowledge-graph", False)
    if remote_path:
        config["deployment"]["remote_path"] = remote_path
    
    backup_path = get_user_input("备份路径", "/opt/kg-backups", False)
    if backup_path:
        config["deployment"]["backup_path"] = backup_path
    
    return config

def save_config(config):
    """保存配置"""
    try:
        # 加载现有配置文件以保留其他设置
        if os.path.exists("deploy_config.json"):
            with open("deploy_config.json", 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # 更新服务器和部署配置
            existing_config["server"] = config["server"]
            existing_config["deployment"] = config["deployment"]
            config = existing_config
        
        # 保存配置
        with open("deploy_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("   ✅ 配置已保存到 deploy_config.json")
        return True
    except Exception as e:
        print(f"   ❌ 保存配置失败: {e}")
        return False

def test_ssh_connection(config):
    """测试SSH连接"""
    print("\n🔍 测试SSH连接...")
    
    try:
        import paramiko
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connect_params = {
            "hostname": config["server"]["host"],
            "port": config["server"]["port"],
            "username": config["server"]["username"],
            "timeout": config["server"]["timeout"]
        }
        
        # 认证方式
        if config["server"].get("key_file") and os.path.exists(config["server"]["key_file"]):
            connect_params["key_filename"] = config["server"]["key_file"]
        elif config["server"].get("password"):
            connect_params["password"] = config["server"]["password"]
        else:
            print("   ❌ 未配置有效的认证方式")
            return False
        
        ssh.connect(**connect_params)
        
        # 执行测试命令
        stdin, stdout, stderr = ssh.exec_command("echo 'SSH连接测试成功'")
        output = stdout.read().decode('utf-8').strip()
        
        ssh.close()
        
        if "SSH连接测试成功" in output:
            print("   ✅ SSH连接测试成功")
            return True
        else:
            print("   ❌ SSH连接测试失败")
            return False
            
    except Exception as e:
        print(f"   ❌ SSH连接失败: {e}")
        return False

def show_deployment_summary(config):
    """显示部署摘要"""
    print("\n📋 部署配置摘要:")
    print("-" * 40)
    print(f"   服务器地址: {config['server']['host']}:{config['server']['port']}")
    print(f"   SSH用户名: {config['server']['username']}")
    
    if config["server"].get("key_file"):
        print(f"   认证方式: SSH密钥 ({config['server']['key_file']})")
    else:
        print("   认证方式: 密码认证")
    
    print(f"   部署路径: {config['deployment']['remote_path']}")
    print(f"   备份路径: {config['deployment']['backup_path']}")
    
    print("\n🌐 部署后访问地址:")
    host = config['server']['host']
    print(f"   • Neo4j浏览器:  http://{host}:7474")
    print(f"   • API服务:      http://{host}:8000")
    print(f"   • API文档:      http://{host}:8000/docs")
    print(f"   • Prometheus:   http://{host}:9090")
    print(f"   • Grafana:      http://{host}:3000")

def execute_deployment():
    """执行部署"""
    print("\n🚀 开始执行自动化部署...")
    print("-" * 40)
    
    try:
        # 执行部署脚本
        process = subprocess.Popen(
            [sys.executable, "ssh_deploy.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时显示输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        
        if return_code == 0:
            print("\n🎉 部署成功完成！")
            return True
        else:
            print(f"\n❌ 部署失败，退出码: {return_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 部署过程中发生错误: {e}")
        return False

def show_post_deployment_info(config):
    """显示部署后信息"""
    print("\n🎉 部署完成！")
    print("=" * 60)
    
    host = config['server']['host']
    
    print("🌐 服务访问地址:")
    print(f"   • Neo4j浏览器:  http://{host}:7474")
    print(f"     用户名: neo4j, 密码: password123")
    print(f"   • API服务:      http://{host}:8000")
    print(f"   • API文档:      http://{host}:8000/docs")
    print(f"   • 健康检查:     http://{host}:8000/health")
    print(f"   • Prometheus:   http://{host}:9090")
    print(f"   • Grafana:      http://{host}:3000")
    print(f"     用户名: admin, 密码: admin123")
    
    print("\n🔧 远程管理命令:")
    print(f"   • SSH登录:      ssh {config['server']['username']}@{host}")
    print("   • 查看日志:     docker-compose logs -f")
    print("   • 重启服务:     docker-compose restart")
    print("   • 停止服务:     docker-compose down")
    
    print("\n📁 服务器路径:")
    print(f"   • 项目目录:     {config['deployment']['remote_path']}")
    print(f"   • 备份目录:     {config['deployment']['backup_path']}")
    
    print("\n💡 下一步建议:")
    print("   1. 访问Neo4j浏览器验证数据库连接")
    print("   2. 访问API文档测试接口功能")
    print("   3. 访问Grafana查看系统监控")
    print("   4. 上传测试数据验证系统功能")

def main():
    """主函数"""
    print_banner()
    
    # 检查前置条件
    if not check_prerequisites():
        print("\n❌ 前置条件检查失败，请解决上述问题后重试")
        return False
    
    print("\n✅ 前置条件检查通过")
    
    # 配置服务器信息
    config = configure_server()
    if not config:
        print("\n❌ 配置过程被取消")
        return False
    
    # 保存配置
    if not save_config(config):
        print("\n❌ 配置保存失败")
        return False
    
    # 测试SSH连接
    if not test_ssh_connection(config):
        print("\n❌ SSH连接测试失败，请检查配置")
        retry = get_yes_no("是否重新配置?", True)
        if retry:
            return main()  # 重新开始
        else:
            return False
    
    # 显示部署摘要
    show_deployment_summary(config)
    
    # 确认部署
    if not get_yes_no("\n确认开始部署?", True):
        print("部署已取消")
        return False
    
    # 执行部署
    if execute_deployment():
        show_post_deployment_info(config)
        return True
    else:
        print("\n❌ 部署失败，请检查错误信息")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 恭喜！知识图谱系统部署成功！")
        else:
            print("\n😞 部署未完成，请解决问题后重试")
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生未预期的错误: {e}")
    
    input("\n按回车键退出...")
