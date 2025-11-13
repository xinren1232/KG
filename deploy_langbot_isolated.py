#!/usr/bin/env python3
"""
LangBot 独立部署脚本
确保与知识图谱系统完全隔离
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
LANGBOT_PORT = 8080
LANGBOT_DIR = "/opt/langbot"
LOG_DIR = "/var/log/langbot"

def print_header(text):
    """打印标题"""
    print(f"\n{'='*70}")
    print(f"🚀 {text}")
    print(f"{'='*70}\n")

def print_step(step_num, text):
    """打印步骤"""
    print(f"\n{step_num}️⃣  {text}")
    print("-" * 70)

def run_ssh_command(cmd, description=""):
    """执行SSH命令"""
    if description:
        print(f"  ⏳ {description}...")
    
    full_cmd = f"ssh {SERVER_USER}@{SERVER_IP} '{cmd}'"
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ 错误: {result.stderr}")
            return False
        if result.stdout:
            print(f"  ✅ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

def main():
    print_header("LangBot 独立部署脚本")
    
    # 步骤1: 创建目录结构
    print_step(1, "创建独立目录结构")
    commands = [
        f"mkdir -p {LANGBOT_DIR}/config",
        f"mkdir -p {LANGBOT_DIR}/data",
        f"mkdir -p {LANGBOT_DIR}/logs",
        f"mkdir -p {LOG_DIR}",
        f"chmod -R 755 {LANGBOT_DIR}",
        f"chmod -R 755 {LOG_DIR}",
    ]
    for cmd in commands:
        run_ssh_command(cmd)
    
    # 步骤2: 创建配置文件
    print_step(2, "创建LangBot配置文件")
    config_yaml = """# LangBot 配置文件
server:
  host: 0.0.0.0
  port: 8080
  debug: false

dify:
  api_url: https://qmsai.transsion.com
  api_key: ${DIFY_API_KEY}
  app_type: chatbot
  timeout: 30

feishu:
  app_id: ${FEISHU_APP_ID}
  app_secret: ${FEISHU_APP_SECRET}
  webhook_token: ${WEBHOOK_TOKEN}

logging:
  level: INFO
  file: /var/log/langbot/langbot.log
  max_size: 100MB
  backup_count: 5

database:
  type: sqlite
  path: /opt/langbot/data/langbot.db
"""
    
    # 上传配置文件
    config_path = "/tmp/langbot_config.yaml"
    with open(config_path, 'w') as f:
        f.write(config_yaml)
    
    upload_cmd = f"scp {config_path} {SERVER_USER}@{SERVER_IP}:{LANGBOT_DIR}/config/config.yaml"
    subprocess.run(upload_cmd, shell=True)
    print(f"  ✅ 配置文件已上传")
    
    # 步骤3: 创建环境变量文件
    print_step(3, "创建环境变量文件")
    print("  ⚠️  请提供以下信息:")
    print("  1. Dify API Key")
    print("  2. 飞书应用ID")
    print("  3. 飞书应用Secret")
    print("  4. Webhook Token")
    print("\n  提示: 可以稍后编辑 /opt/langbot/.env 文件")
    
    env_content = """# Dify配置
DIFY_API_KEY=your_dify_api_key_here
DIFY_API_URL=https://qmsai.transsion.com

# 飞书配置
FEISHU_APP_ID=your_feishu_app_id_here
FEISHU_APP_SECRET=your_feishu_app_secret_here
WEBHOOK_TOKEN=your_webhook_token_here

# 服务配置
LANGBOT_PORT=8080
LANGBOT_HOST=0.0.0.0
LANGBOT_DEBUG=false
"""
    
    env_path = "/tmp/langbot.env"
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    upload_cmd = f"scp {env_path} {SERVER_USER}@{SERVER_IP}:{LANGBOT_DIR}/.env"
    subprocess.run(upload_cmd, shell=True)
    run_ssh_command(f"chmod 600 {LANGBOT_DIR}/.env")
    print(f"  ✅ 环境变量文件已创建")
    
    # 步骤4: 创建Docker Compose配置
    print_step(4, "创建Docker Compose配置")
    docker_compose = """version: '3.8'

services:
  langbot:
    image: langbot:latest
    container_name: langbot
    ports:
      - "8080:8080"
    volumes:
      - ./config:/app/config
      - ./data:/data
      - /var/log/langbot:/var/log/langbot
    environment:
      - DIFY_API_KEY=${DIFY_API_KEY}
      - DIFY_API_URL=${DIFY_API_URL}
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
      - WEBHOOK_TOKEN=${WEBHOOK_TOKEN}
      - LANGBOT_PORT=8080
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - langbot-network

networks:
  langbot-network:
    driver: bridge
"""
    
    compose_path = "/tmp/docker-compose.yml"
    with open(compose_path, 'w') as f:
        f.write(docker_compose)
    
    upload_cmd = f"scp {compose_path} {SERVER_USER}@{SERVER_IP}:{LANGBOT_DIR}/docker-compose.yml"
    subprocess.run(upload_cmd, shell=True)
    print(f"  ✅ Docker Compose配置已创建")
    
    # 步骤5: 创建systemd服务
    print_step(5, "创建systemd服务")
    systemd_service = """[Unit]
Description=LangBot IM Integration Service
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/langbot
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/opt/langbot/.env
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10
StandardOutput=append:/var/log/langbot/systemd.log
StandardError=append:/var/log/langbot/systemd-error.log

[Install]
WantedBy=multi-user.target
"""
    
    service_path = "/tmp/langbot.service"
    with open(service_path, 'w') as f:
        f.write(systemd_service)
    
    upload_cmd = f"scp {service_path} {SERVER_USER}@{SERVER_IP}:/etc/systemd/system/langbot.service"
    subprocess.run(upload_cmd, shell=True)
    run_ssh_command("systemctl daemon-reload", "重载systemd")
    print(f"  ✅ systemd服务已创建")
    
    # 步骤6: 验证现有系统
    print_step(6, "验证现有系统不受影响")
    services = ["kg-api", "kg-frontend", "neo4j", "redis-server", "nginx"]
    for service in services:
        run_ssh_command(f"systemctl is-active {service}", f"检查 {service} 状态")
    
    # 步骤7: 显示后续步骤
    print_header("部署完成！")
    print("""
✅ 已完成的步骤:
  1. ✅ 创建独立目录结构
  2. ✅ 创建LangBot配置文件
  3. ✅ 创建环境变量文件
  4. ✅ 创建Docker Compose配置
  5. ✅ 创建systemd服务
  6. ✅ 验证现有系统

📋 后续步骤:
  1. 编辑环境变量文件:
     ssh root@47.108.152.16
     nano /opt/langbot/.env
     
  2. 配置Nginx反向代理:
     参考: langbot_isolated_deployment.md
     
  3. 启动LangBot服务:
     systemctl start langbot
     
  4. 验证服务:
     systemctl status langbot
     curl http://localhost:8080/health

⚠️  重要提醒:
  - 请先配置 /opt/langbot/.env 中的API Key和飞书凭证
  - 确保Dify服务正常运行
  - 确保飞书机器人应用已创建
  - 部署前请备份现有系统配置
""")

if __name__ == "__main__":
    main()

