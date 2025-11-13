#!/bin/bash

# LangBot 独立部署脚本
# 确保与知识图谱系统完全隔离

set -e

# 配置
SERVER_IP="47.108.152.16"
SERVER_USER="root"
LANGBOT_DIR="/opt/langbot"
LOG_DIR="/var/log/langbot"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}🚀 $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_step() {
    echo -e "\n${YELLOW}$1️⃣  $2${NC}"
    echo -e "${YELLOW}----------------------------------------${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 执行SSH命令
run_ssh() {
    local cmd="$1"
    local desc="$2"
    
    if [ -n "$desc" ]; then
        print_info "$desc"
    fi
    
    ssh "${SERVER_USER}@${SERVER_IP}" "$cmd"
}

# 主函数
main() {
    print_header "LangBot 独立部署脚本"
    
    # 步骤1: 验证前置条件
    print_step 1 "验证前置条件"
    
    print_info "检查SSH连接..."
    if ! ssh -o ConnectTimeout=5 "${SERVER_USER}@${SERVER_IP}" "echo 'SSH连接成功'" > /dev/null 2>&1; then
        print_error "无法连接到服务器 ${SERVER_IP}"
        exit 1
    fi
    print_success "SSH连接正常"
    
    print_info "检查Docker..."
    if ! run_ssh "docker --version" > /dev/null 2>&1; then
        print_error "Docker未安装"
        exit 1
    fi
    print_success "Docker已安装"
    
    print_info "检查现有系统..."
    run_ssh "systemctl is-active kg-api kg-frontend neo4j redis-server nginx" "检查现有服务"
    print_success "现有系统正常运行"
    
    # 步骤2: 创建目录结构
    print_step 2 "创建独立目录结构"
    
    run_ssh "mkdir -p ${LANGBOT_DIR}/config ${LANGBOT_DIR}/data ${LANGBOT_DIR}/logs ${LOG_DIR}" \
        "创建目录"
    run_ssh "chmod -R 755 ${LANGBOT_DIR} ${LOG_DIR}" \
        "设置权限"
    print_success "目录结构创建完成"
    
    # 步骤3: 创建配置文件
    print_step 3 "创建LangBot配置文件"
    
    run_ssh "cat > ${LANGBOT_DIR}/config/config.yaml << 'EOF'
server:
  host: 0.0.0.0
  port: 8080
  debug: false

dify:
  api_url: https://qmsai.transsion.com
  api_key: \${DIFY_API_KEY}
  app_type: chatbot
  timeout: 30

feishu:
  app_id: \${FEISHU_APP_ID}
  app_secret: \${FEISHU_APP_SECRET}
  webhook_token: \${WEBHOOK_TOKEN}

logging:
  level: INFO
  file: ${LOG_DIR}/langbot.log
  max_size: 100MB
  backup_count: 5

database:
  type: sqlite
  path: ${LANGBOT_DIR}/data/langbot.db
EOF" "创建配置文件"
    print_success "配置文件创建完成"
    
    # 步骤4: 创建环境变量文件
    print_step 4 "创建环境变量文件"
    
    run_ssh "cat > ${LANGBOT_DIR}/.env << 'EOF'
DIFY_API_KEY=your_dify_api_key_here
DIFY_API_URL=https://qmsai.transsion.com
FEISHU_APP_ID=your_feishu_app_id_here
FEISHU_APP_SECRET=your_feishu_app_secret_here
WEBHOOK_TOKEN=your_webhook_token_here
LANGBOT_PORT=8080
LANGBOT_HOST=0.0.0.0
LANGBOT_DEBUG=false
EOF" "创建.env文件"
    
    run_ssh "chmod 600 ${LANGBOT_DIR}/.env" "设置.env权限"
    print_success "环境变量文件创建完成"
    print_info "⚠️  请编辑 ${LANGBOT_DIR}/.env 文件，配置API Key和飞书凭证"
    
    # 步骤5: 创建Docker Compose配置
    print_step 5 "创建Docker Compose配置"
    
    run_ssh "cat > ${LANGBOT_DIR}/docker-compose.yml << 'EOF'
version: '3.8'

services:
  langbot:
    image: langbot:latest
    container_name: langbot
    ports:
      - \"8080:8080\"
    volumes:
      - ./config:/app/config
      - ./data:/data
      - ${LOG_DIR}:${LOG_DIR}
    environment:
      - DIFY_API_KEY=\${DIFY_API_KEY}
      - DIFY_API_URL=\${DIFY_API_URL}
      - FEISHU_APP_ID=\${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=\${FEISHU_APP_SECRET}
      - WEBHOOK_TOKEN=\${WEBHOOK_TOKEN}
      - LANGBOT_PORT=8080
    restart: always
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:8080/health\"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - langbot-network

networks:
  langbot-network:
    driver: bridge
EOF" "创建Docker Compose文件"
    print_success "Docker Compose配置创建完成"
    
    # 步骤6: 创建systemd服务
    print_step 6 "创建systemd服务"
    
    run_ssh "cat > /etc/systemd/system/langbot.service << 'EOF'
[Unit]
Description=LangBot IM Integration Service
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=${LANGBOT_DIR}
Environment=\"PATH=/usr/local/bin:/usr/bin:/bin\"
EnvironmentFile=${LANGBOT_DIR}/.env
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10
StandardOutput=append:${LOG_DIR}/systemd.log
StandardError=append:${LOG_DIR}/systemd-error.log

[Install]
WantedBy=multi-user.target
EOF" "创建systemd服务文件"
    
    run_ssh "systemctl daemon-reload" "重载systemd"
    print_success "systemd服务创建完成"
    
    # 步骤7: 配置Nginx反向代理
    print_step 7 "配置Nginx反向代理"
    
    run_ssh "cat > /etc/nginx/sites-available/langbot << 'EOF'
server {
    listen 80;
    server_name 47.108.152.16;
    
    location /langbot/ {
        proxy_pass http://localhost:8080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"upgrade\";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }
    
    location /webhook/feishu {
        proxy_pass http://localhost:8080/webhook/feishu;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF" "创建Nginx配置"
    
    run_ssh "ln -sf /etc/nginx/sites-available/langbot /etc/nginx/sites-enabled/" \
        "启用Nginx配置"
    run_ssh "nginx -t" "测试Nginx配置"
    run_ssh "systemctl restart nginx" "重启Nginx"
    print_success "Nginx配置完成"
    
    # 步骤8: 最终验证
    print_step 8 "最终验证"
    
    print_info "验证现有系统..."
    run_ssh "systemctl is-active kg-api kg-frontend neo4j redis-server nginx"
    print_success "现有系统仍正常运行"
    
    print_info "检查端口占用..."
    run_ssh "netstat -tlnp | grep -E ':(80|5173|8000|7474|7687|6379)'"
    print_success "端口检查完成"
    
    # 完成提示
    print_header "部署完成！"
    
    echo -e "${GREEN}✅ 所有步骤已完成${NC}\n"
    
    echo -e "${YELLOW}📋 后续步骤:${NC}"
    echo "1. 编辑环境变量文件:"
    echo "   ssh ${SERVER_USER}@${SERVER_IP}"
    echo "   nano ${LANGBOT_DIR}/.env"
    echo ""
    echo "2. 配置Dify API Key和飞书凭证"
    echo ""
    echo "3. 启动LangBot服务:"
    echo "   systemctl start langbot"
    echo ""
    echo "4. 验证服务:"
    echo "   systemctl status langbot"
    echo "   curl http://localhost:8080/health"
    echo ""
    echo -e "${YELLOW}⚠️  重要提醒:${NC}"
    echo "- 请先配置 ${LANGBOT_DIR}/.env 中的API Key"
    echo "- 确保Dify服务正常运行"
    echo "- 确保飞书机器人应用已创建"
    echo ""
}

# 执行主函数
main "$@"

