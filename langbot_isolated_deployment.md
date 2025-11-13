# LangBot 独立部署方案 (与知识图谱系统隔离)

## 🎯 部署目标

- ✅ 完全独立的LangBot服务
- ✅ 不影响现有知识图谱系统
- ✅ 独立的端口、进程、日志
- ✅ 独立的systemd服务管理
- ✅ 独立的Nginx反向代理配置

---

## 📊 当前系统占用情况

### 现有服务
| 服务 | 端口 | 进程 | 状态 |
|------|------|------|------|
| **Nginx** | 80 | systemd | ✅ 运行 |
| **前端** | 5173 | nohup | ✅ 运行 |
| **API** | 8000 | systemd | ✅ 运行 |
| **Neo4j HTTP** | 7474 | systemd | ✅ 运行 |
| **Neo4j Bolt** | 7687 | systemd | ✅ 运行 |
| **Redis** | 6379 | systemd | ✅ 运行 |

### LangBot 独立配置
| 资源 | 分配 | 说明 |
|------|------|------|
| **端口** | 8080 | 独立端口，不与现有冲突 |
| **进程管理** | systemd | langbot.service |
| **日志** | /var/log/langbot/ | 独立日志目录 |
| **数据** | /opt/langbot/ | 独立数据目录 |
| **内存限制** | 512MB | Docker容器限制 |
| **CPU限制** | 1核 | Docker容器限制 |

---

## 🚀 部署步骤

### 步骤1: 创建独立目录结构

```bash
# 创建LangBot专用目录
mkdir -p /opt/langbot
mkdir -p /opt/langbot/config
mkdir -p /opt/langbot/data
mkdir -p /opt/langbot/logs
mkdir -p /var/log/langbot

# 设置权限
chmod -R 755 /opt/langbot
chmod -R 755 /var/log/langbot
```

### 步骤2: 配置LangBot

```bash
# 创建配置文件
cat > /opt/langbot/config/config.yaml << 'EOF'
# LangBot 配置文件

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
EOF
```

### 步骤3: 创建环境变量文件

```bash
cat > /opt/langbot/.env << 'EOF'
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
EOF

# 设置权限
chmod 600 /opt/langbot/.env
```

### 步骤4: 创建Docker Compose配置

```bash
cat > /opt/langbot/docker-compose.yml << 'EOF'
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
EOF
```

### 步骤5: 创建systemd服务

```bash
cat > /etc/systemd/system/langbot.service << 'EOF'
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
EOF

# 重载systemd
systemctl daemon-reload
```

### 步骤6: 配置Nginx反向代理

```bash
cat > /etc/nginx/sites-available/langbot << 'EOF'
server {
    listen 80;
    server_name 47.108.152.16;
    
    # LangBot API路由
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
    
    # 飞书Webhook路由
    location /webhook/feishu {
        proxy_pass http://localhost:8080/webhook/feishu;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/langbot /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启Nginx
systemctl restart nginx
```

---

## ✅ 启动和验证

### 启动LangBot

```bash
# 启动服务
systemctl start langbot

# 查看状态
systemctl status langbot

# 查看日志
tail -f /var/log/langbot/langbot.log
```

### 验证服务

```bash
# 检查端口
netstat -tlnp | grep 8080

# 健康检查
curl http://localhost:8080/health

# 测试Dify连接
curl -X POST http://localhost:8080/test-dify \
  -H "Content-Type: application/json" \
  -d '{"message": "测试"}'
```

---

## 🔒 隔离验证

### 确保不影响现有系统

```bash
# 1. 检查现有服务状态
systemctl status kg-api kg-frontend neo4j redis-server

# 2. 检查现有端口
netstat -tlnp | grep -E ':(80|5173|8000|7474|7687|6379)'

# 3. 检查现有进程
ps aux | grep -E 'node|python|java' | grep -v grep

# 4. 测试现有API
curl http://localhost:8000/health
```

---

## 📊 资源监控

```bash
# 监控LangBot容器
docker stats langbot

# 查看内存使用
docker inspect langbot | grep -i memory

# 查看日志大小
du -sh /var/log/langbot/
```

---

## 🚨 故障排查

### LangBot无法启动

```bash
# 查看systemd日志
journalctl -u langbot -n 50

# 查看Docker日志
docker logs langbot

# 检查配置文件
cat /opt/langbot/config/config.yaml
```

### 无法连接Dify

```bash
# 测试网络连接
curl -v https://qmsai.transsion.com

# 检查API Key
docker exec langbot curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://qmsai.transsion.com/api/apps
```

---

## 📋 部署检查清单

- [ ] 创建独立目录结构
- [ ] 配置环境变量
- [ ] 创建Docker Compose配置
- [ ] 创建systemd服务
- [ ] 配置Nginx反向代理
- [ ] 启动LangBot服务
- [ ] 验证服务状态
- [ ] 测试Dify连接
- [ ] 测试飞书连接
- [ ] 验证现有系统不受影响

---

**部署方案版本**: 1.0  
**隔离等级**: ⭐⭐⭐⭐⭐ (完全隔离)

