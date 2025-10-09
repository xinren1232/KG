#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署配置助手
帮助用户配置SSH部署参数
"""

import json
import os
import sys
from pathlib import Path

def get_user_input(prompt, default="", required=True):
    """获取用户输入"""
    if default:
        full_prompt = f"{prompt} (默认: {default}): "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("❌ 此项为必填项，请输入有效值")

def validate_ssh_connection(host, port, username, password, key_file):
    """验证SSH连接"""
    try:
        import paramiko
        
        print(f"🔍 测试SSH连接到 {username}@{host}:{port}...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connect_params = {
            "hostname": host,
            "port": port,
            "username": username,
            "timeout": 10
        }
        
        if key_file and os.path.exists(key_file):
            connect_params["key_filename"] = key_file
            print(f"   使用SSH密钥: {key_file}")
        elif password:
            connect_params["password"] = password
            print("   使用密码认证")
        else:
            print("❌ 未配置认证方式")
            return False
        
        ssh.connect(**connect_params)
        
        # 测试执行命令
        stdin, stdout, stderr = ssh.exec_command("echo 'SSH连接测试成功'")
        result = stdout.read().decode().strip()
        
        ssh.close()
        
        if result == "SSH连接测试成功":
            print("✅ SSH连接测试成功！")
            return True
        else:
            print("❌ SSH连接测试失败")
            return False
            
    except ImportError:
        print("⚠️ 未安装paramiko库，跳过连接测试")
        print("   请运行: pip install paramiko")
        return True
    except Exception as e:
        print(f"❌ SSH连接失败: {e}")
        return False

def configure_deployment():
    """配置部署参数"""
    print("🚀 知识图谱系统部署配置助手")
    print("=" * 50)
    
    # 加载现有配置
    config_file = "deploy_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        print("❌ 配置文件不存在")
        return False
    
    print("\n📋 请配置服务器连接信息:")
    
    # 服务器基本信息
    print("\n1. 服务器基本信息")
    config["server"]["host"] = get_user_input(
        "服务器IP地址或域名", 
        config["server"]["host"] if config["server"]["host"] != "your-server-ip" else ""
    )
    
    config["server"]["port"] = int(get_user_input(
        "SSH端口", 
        str(config["server"]["port"])
    ))
    
    config["server"]["username"] = get_user_input(
        "SSH用户名", 
        config["server"]["username"] if config["server"]["username"] != "your-username" else ""
    )
    
    # 认证方式选择
    print("\n2. SSH认证方式")
    print("   1) SSH密钥认证 (推荐)")
    print("   2) 密码认证")
    
    auth_choice = get_user_input("请选择认证方式 (1/2)", "1")
    
    if auth_choice == "1":
        # SSH密钥认证
        default_key_paths = [
            os.path.expanduser("~/.ssh/id_rsa"),
            os.path.expanduser("~/.ssh/id_ed25519"),
            "C:\\Users\\{}/.ssh/id_rsa".format(os.getenv("USERNAME", ""))
        ]
        
        suggested_key = ""
        for key_path in default_key_paths:
            if os.path.exists(key_path):
                suggested_key = key_path
                break
        
        config["server"]["key_file"] = get_user_input(
            "SSH私钥文件路径", 
            suggested_key
        )
        config["server"]["password"] = ""
        
        # 验证密钥文件
        if not os.path.exists(config["server"]["key_file"]):
            print(f"⚠️ 警告: 密钥文件不存在: {config['server']['key_file']}")
            create_key = get_user_input("是否生成新的SSH密钥? (y/n)", "n", False)
            if create_key.lower() == 'y':
                print("💡 请运行以下命令生成SSH密钥:")
                print(f"   ssh-keygen -t rsa -b 4096 -f {config['server']['key_file']}")
                print("   然后将公钥上传到服务器:")
                print(f"   ssh-copy-id -i {config['server']['key_file']}.pub {config['server']['username']}@{config['server']['host']}")
    else:
        # 密码认证
        import getpass
        config["server"]["password"] = getpass.getpass("SSH密码: ")
        config["server"]["key_file"] = ""
    
    # 部署路径配置
    print("\n3. 部署路径配置")
    config["deployment"]["remote_path"] = get_user_input(
        "远程部署路径", 
        config["deployment"]["remote_path"]
    )
    
    config["deployment"]["backup_path"] = get_user_input(
        "备份路径", 
        config["deployment"]["backup_path"]
    )
    
    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 配置已保存到: {config_file}")
    
    # 测试连接
    print("\n🔍 测试SSH连接...")
    connection_ok = validate_ssh_connection(
        config["server"]["host"],
        config["server"]["port"],
        config["server"]["username"],
        config["server"]["password"],
        config["server"]["key_file"]
    )
    
    if connection_ok:
        print("\n🎉 配置完成！可以开始部署了")
        return True
    else:
        print("\n❌ SSH连接测试失败，请检查配置")
        return False

def show_deployment_summary():
    """显示部署摘要"""
    config_file = "deploy_config.json"
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("\n📋 部署配置摘要:")
    print(f"   服务器: {config['server']['host']}:{config['server']['port']}")
    print(f"   用户: {config['server']['username']}")
    print(f"   认证: {'SSH密钥' if config['server']['key_file'] else '密码'}")
    print(f"   部署路径: {config['deployment']['remote_path']}")
    print(f"   备份路径: {config['deployment']['backup_path']}")
    
    print(f"\n🌐 部署后访问地址:")
    host = config['server']['host']
    print(f"   • Neo4j浏览器:    http://{host}:7474")
    print(f"   • API服务:        http://{host}:8000")
    print(f"   • API文档:        http://{host}:8000/docs")
    print(f"   • 健康检查:       http://{host}:8000/health")
    print(f"   • Prometheus:     http://{host}:9090")
    print(f"   • Grafana:        http://{host}:3000")

def main():
    """主函数"""
    print("🚀 知识图谱系统部署配置助手")
    print("=" * 50)
    
    # 检查是否已配置
    config_file = "deploy_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if (config["server"]["host"] != "your-server-ip" and 
            config["server"]["username"] != "your-username"):
            print("✅ 检测到已有配置")
            show_deployment_summary()
            
            reconfigure = get_user_input("\n是否重新配置? (y/n)", "n", False)
            if reconfigure.lower() != 'y':
                print("\n💡 使用现有配置，可以直接执行部署:")
                print("   python ssh_deploy.py")
                return True
    
    # 配置部署参数
    if configure_deployment():
        show_deployment_summary()
        
        print("\n🚀 下一步操作:")
        print("   1. 确认服务器配置正确")
        print("   2. 执行部署命令: python ssh_deploy.py")
        print("   3. 等待部署完成")
        print("   4. 访问服务地址验证部署")
        
        # 询问是否立即部署
        deploy_now = get_user_input("\n是否立即开始部署? (y/n)", "y", False)
        if deploy_now.lower() == 'y':
            print("\n🚀 开始执行部署...")
            os.system("python ssh_deploy.py")
        
        return True
    else:
        print("\n❌ 配置失败，请检查服务器信息")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消配置")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 配置过程中发生错误: {e}")
        sys.exit(1)
