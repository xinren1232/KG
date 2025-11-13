# LangBot 部署执行清单

## 📋 部署前准备

### 1. 信息收集 ✅

需要准备以下信息：

```
【Dify配置】
- API URL: https://qmsai.transsion.com ✅
- API Key: [需要从Dify获取]
- 应用类型: chatbot 或 workflow

【飞书机器人配置】
- 应用ID: [需要创建机器人应用]
- 应用Secret: [需要创建机器人应用]
- Webhook Token: [自定义]

【服务器配置】
- 服务器IP: 47.108.152.16 ✅
- SSH用户: root ✅
- SSH端口: 22 ✅
```

### 2. 前置检查 ✅

```bash
# 检查现有系统状态
ssh root@47.108.152.16 "systemctl status kg-api kg-frontend neo4j redis-server nginx"

# 检查端口占用
ssh root@47.108.152.16 "netstat -tlnp | grep -E ':(80|5173|8000|7474|7687|6379|8080)'"

# 检查Docker状态
ssh root@47.108.152.16 "docker --version && docker-compose --version"
```

---

## 🚀 部署执行步骤

### 第1阶段: 创建独立环境 (5分钟)

#### 步骤1.1: 创建目录结构

```bash
ssh root@47.108.152.16 << 'EOF'
mkdir -p /opt/langbot/config
mkdir -p /opt/langbot/data
mkdir -p /opt/langbot/logs
mkdir -p /var/log/langbot
chmod -R 755 /opt/langbot
chmod -R 755 /var/log/langbot
echo "✅ 目录结构创建完成"
EOF
```

**验证**: 
```bash
ssh root@47.108.152.16 "ls -la /opt/langbot/"
```

#### 步骤1.2: 创建配置文件

```bash
ssh root@47.108.152.16 << 'EOF'
cat > /opt/langbot/config/config.yaml << 'CONFIG'
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
CONFIG
echo "✅ 配置文件创建完成"
EOF
```

---

### 第2阶段: 配置环境变量 (5分钟)

#### 步骤2.1: 创建.env文件

```bash
ssh root@47.108.152.16 << 'EOF'
cat > /opt/langbot/.env << 'ENV'
# Dify配置
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
ENV
chmod 600 /opt/langbot/.env
echo "✅ 环境变量文件创建完成"
EOF
```

#### 步骤2.2: 编辑环境变量

```bash
# 连接到服务器编辑
ssh root@47.108.152.16
nano /opt/langbot/.env

# 修改以下内容:
# DIFY_API_KEY=<从Dify获取的API Key>
# FEISHU_APP_ID=<飞书应用ID>
# FEISHU_APP_SECRET=<飞书应用Secret>
# WEBHOOK_TOKEN=<自定义的Webhook Token>

# 保存并退出 (Ctrl+X, Y, Enter)
```

---

### 第3阶段: 创建Docker配置 (5分钟)

#### 步骤3.1: 创建Docker Compose文件

```bash
ssh root@47.108.152.16 << 'EOF'
cat > /opt/langbot/docker-compose.yml << 'DOCKER'
version: '3.8'

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
DOCKER
echo "✅ Docker Compose配置创建完成"
EOF
```

---

### 第4阶段: 创建systemd服务 (5分钟)

#### 步骤4.1: 创建服务文件

```bash
ssh root@47.108.152.16 << 'EOF'
cat > /etc/systemd/system/langbot.service << 'SERVICE'
[Unit]
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
SERVICE

systemctl daemon-reload
echo "✅ systemd服务创建完成"
EOF
```

---

### 第5阶段: 配置Nginx反向代理 (5分钟)

#### 步骤5.1: 创建Nginx配置

```bash
ssh root@47.108.152.16 << 'EOF'
cat > /etc/nginx/sites-available/langbot << 'NGINX'
server {
    listen 80;
    server_name 47.108.152.16;
    
    location /langbot/ {
        proxy_pass http://localhost:8080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }
    
    location /webhook/feishu {
        proxy_pass http://localhost:8080/webhook/feishu;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
NGINX

ln -s /etc/nginx/sites-available/langbot /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
echo "✅ Nginx配置完成"
EOF
```

---

### 第6阶段: 启动和验证 (10分钟)

#### 步骤6.1: 启动LangBot

```bash
ssh root@47.108.152.16 << 'EOF'
systemctl start langbot
sleep 5
systemctl status langbot
echo "✅ LangBot服务已启动"
EOF
```

#### 步骤6.2: 验证服务

```bash
# 检查端口
ssh root@47.108.152.16 "netstat -tlnp | grep 8080"

# 健康检查
ssh root@47.108.152.16 "curl http://localhost:8080/health"

# 查看日志
ssh root@47.108.152.16 "tail -20 /var/log/langbot/langbot.log"
```

#### 步骤6.3: 验证现有系统

```bash
# 检查现有服务
ssh root@47.108.152.16 << 'EOF'
echo "检查现有服务状态..."
systemctl is-active kg-api kg-frontend neo4j redis-server nginx
echo ""
echo "检查现有端口..."
netstat -tlnp | grep -E ':(80|5173|8000|7474|7687|6379)'
EOF
```

---

## ✅ 部署验证清单

- [ ] 目录结构创建成功
- [ ] 配置文件创建成功
- [ ] 环境变量文件创建并配置成功
- [ ] Docker Compose配置创建成功
- [ ] systemd服务创建成功
- [ ] Nginx配置创建成功
- [ ] LangBot服务启动成功
- [ ] 健康检查通过
- [ ] 现有系统仍正常运行
- [ ] 端口8080正常监听
- [ ] 日志文件正常生成

---

## 📊 部署后检查

### 1. 服务状态

```bash
systemctl status langbot
docker ps | grep langbot
```

### 2. 资源使用

```bash
docker stats langbot
```

### 3. 日志检查

```bash
tail -f /var/log/langbot/langbot.log
```

### 4. 功能测试

```bash
# 测试Dify连接
curl -X POST http://47.108.152.16/langbot/test-dify \
  -H "Content-Type: application/json" \
  -d '{"message": "测试"}'

# 测试飞书Webhook
curl -X POST http://47.108.152.16/webhook/feishu \
  -H "Content-Type: application/json" \
  -d '{"text": "测试消息"}'
```

---

## 🎉 部署完成

**总耗时**: 约30-40分钟

**下一步**:
1. 在飞书中配置机器人Webhook URL
2. 测试飞书消息接收
3. 监控日志和性能
4. 根据需要调整配置

---

**部署日期**: 2025-11-13  
**部署版本**: 1.0  
**隔离等级**: ⭐⭐⭐⭐⭐

