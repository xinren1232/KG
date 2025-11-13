# LangBot 部署实施指南

## 📋 前置条件

### 1. Dify 配置信息
```
服务器地址: https://qmsai.transsion.com
API Key: [需要从Dify获取]
应用类型: chatbot 或 workflow
```

### 2. 飞书机器人配置
```
应用ID: [需要创建]
应用Secret: [需要创建]
Webhook URL: http://47.108.152.16:8080/webhook/feishu
```

---

## 🐳 Docker 部署方案 (推荐)

### 步骤1: 创建LangBot配置目录

```bash
# SSH连接服务器
ssh root@47.108.152.16

# 创建目录
mkdir -p /opt/langbot
cd /opt/langbot

# 创建配置文件
cat > config.yaml << 'EOF'
# LangBot 配置文件

# 服务器配置
server:
  host: 0.0.0.0
  port: 8080
  debug: false

# Dify 配置
dify:
  api_url: https://qmsai.transsion.com
  api_key: YOUR_DIFY_API_KEY
  app_type: chatbot  # 或 workflow
  timeout: 30

# 飞书配置
feishu:
  app_id: YOUR_FEISHU_APP_ID
  app_secret: YOUR_FEISHU_APP_SECRET
  webhook_token: YOUR_WEBHOOK_TOKEN

# 日志配置
logging:
  level: INFO
  file: /var/log/langbot/langbot.log

# 数据库配置 (可选)
database:
  type: sqlite
  path: /data/langbot.db
EOF
```

### 步骤2: 创建Docker Compose文件

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  langbot:
    image: langbot:latest
    container_name: langbot
    ports:
      - "8080:8080"
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./data:/data
      - /var/log/langbot:/var/log/langbot
    environment:
      - DIFY_API_URL=https://qmsai.transsion.com
      - DIFY_API_KEY=${DIFY_API_KEY}
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
    restart: always
    networks:
      - kg-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  kg-network:
    external: true
EOF
```

### 步骤3: 创建环境变量文件

```bash
cat > .env << 'EOF'
DIFY_API_KEY=your_dify_api_key_here
FEISHU_APP_ID=your_feishu_app_id_here
FEISHU_APP_SECRET=your_feishu_app_secret_here
EOF

# 设置权限
chmod 600 .env
```

### 步骤4: 启动LangBot

```bash
# 创建网络 (如果不存在)
docker network create kg-network 2>/dev/null || true

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f langbot

# 检查状态
docker-compose ps
```

---

## 🔧 Nginx 反向代理配置

### 添加LangBot到Nginx

```bash
cat > /etc/nginx/sites-available/langbot << 'EOF'
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
    }
    
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

## 🧪 测试与验证

### 1. 检查LangBot服务

```bash
# 检查容器状态
docker ps | grep langbot

# 检查日志
docker logs langbot

# 测试健康检查
curl http://localhost:8080/health
```

### 2. 测试Dify连接

```bash
# 测试API连接
curl -X POST http://localhost:8080/test-dify \
  -H "Content-Type: application/json" \
  -d '{"message": "测试消息"}'
```

### 3. 测试飞书连接

```bash
# 在飞书机器人中发送测试消息
# 应该收到来自Dify的回复
```

---

## 📊 监控与维护

### 1. 资源监控

```bash
# 实时监控
docker stats langbot

# 查看内存使用
docker inspect langbot | grep -i memory

# 查看日志大小
du -sh /var/log/langbot/
```

### 2. 日志管理

```bash
# 查看最近日志
tail -f /var/log/langbot/langbot.log

# 查看错误日志
grep ERROR /var/log/langbot/langbot.log

# 日志轮转配置
cat > /etc/logrotate.d/langbot << 'EOF'
/var/log/langbot/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF
```

### 3. 性能优化

```bash
# 如果内存不足，可以限制LangBot内存
docker update --memory 512m langbot

# 如果CPU不足，可以限制CPU
docker update --cpus 1 langbot
```

---

## 🚨 故障排查

### 问题1: LangBot无法连接Dify

```bash
# 检查网络连接
curl -v https://qmsai.transsion.com

# 检查API Key
docker exec langbot curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://qmsai.transsion.com/api/apps
```

### 问题2: 飞书机器人无法接收消息

```bash
# 检查Webhook配置
docker logs langbot | grep webhook

# 检查防火墙
sudo ufw status
sudo ufw allow 8080
```

### 问题3: 内存占用过高

```bash
# 检查进程
docker top langbot

# 重启服务
docker restart langbot

# 查看内存泄漏
docker stats --no-stream langbot
```

---

## 📋 部署检查清单

- [ ] 服务器资源充足 (内存>1.6GB)
- [ ] Dify服务正常运行
- [ ] 获取Dify API Key
- [ ] 创建飞书机器人应用
- [ ] 配置环境变量
- [ ] 启动LangBot容器
- [ ] 测试Dify连接
- [ ] 测试飞书连接
- [ ] 配置Nginx反向代理
- [ ] 设置监控告警
- [ ] 备份配置文件

---

**部署指南版本**: 1.0  
**最后更新**: 2025-11-13

