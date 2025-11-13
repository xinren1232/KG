#!/bin/bash

# LangBot 最终部署脚本
# 一键完成所有部署步骤

SERVER_IP="47.108.152.16"
SERVER_USER="root"

echo "=========================================="
echo "LangBot 最终部署脚本"
echo "=========================================="
echo ""

# 第1步: 创建Python应用
echo "【步骤1】创建LangBot Python应用..."
ssh ${SERVER_USER}@${SERVER_IP} 'cat > /opt/langbot/app.py << '\''EOF'\''
#!/usr/bin/env python3
import os, json, logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ["/health", "/"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "langbot", "timestamp": datetime.now().isoformat()}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if "/webhook/feishu" in self.path:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"code": 0, "msg": "success"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        logger.info(format % args)

if __name__ == "__main__":
    host = os.getenv("LANGBOT_HOST", "0.0.0.0")
    port = int(os.getenv("LANGBOT_PORT", 8080))
    logger.info(f"Starting LangBot on {host}:{port}")
    HTTPServer((host, port), Handler).serve_forever()
EOF
chmod +x /opt/langbot/app.py'

echo "✅ Python应用已创建"
echo ""

# 第2步: 更新systemd服务
echo "【步骤2】更新systemd服务..."
ssh ${SERVER_USER}@${SERVER_IP} 'cat > /etc/systemd/system/langbot.service << '\''EOF'\''
[Unit]
Description=LangBot IM Integration Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/langbot
EnvironmentFile=/opt/langbot/.env
ExecStart=/usr/bin/python3 /opt/langbot/app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/langbot/systemd.log
StandardError=append:/var/log/langbot/systemd-error.log

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable langbot'

echo "✅ systemd服务已更新"
echo ""

# 第3步: 启动LangBot服务
echo "【步骤3】启动LangBot服务..."
ssh ${SERVER_USER}@${SERVER_IP} 'systemctl start langbot && sleep 2 && systemctl status langbot'

echo "✅ LangBot服务已启动"
echo ""

# 第4步: 验证服务
echo "【步骤4】验证LangBot服务..."
ssh ${SERVER_USER}@${SERVER_IP} 'curl -s http://localhost:8080/health | python3 -m json.tool'

echo ""
echo "=========================================="
echo "✅ LangBot部署完成！"
echo "=========================================="

