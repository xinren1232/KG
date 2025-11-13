#!/bin/bash

# LangBot 配置脚本
# 帮助用户配置环境变量

SERVER_IP="47.108.152.16"
SERVER_USER="root"
ENV_FILE="/opt/langbot/.env"

echo "=========================================="
echo "LangBot 环境变量配置向导"
echo "=========================================="
echo ""

# 检查SSH连接
echo "检查SSH连接..."
if ! ssh -o ConnectTimeout=5 ${SERVER_USER}@${SERVER_IP} "test -f ${ENV_FILE}" > /dev/null 2>&1; then
    echo "❌ SSH连接失败或.env文件不存在"
    exit 1
fi
echo "✅ SSH连接正常"
echo ""

# 收集信息
echo "请输入以下信息:"
echo ""

read -p "【1】Dify API Key: " DIFY_API_KEY
if [ -z "$DIFY_API_KEY" ]; then
    echo "❌ Dify API Key不能为空"
    exit 1
fi

read -p "【2】飞书应用ID: " FEISHU_APP_ID
if [ -z "$FEISHU_APP_ID" ]; then
    echo "❌ 飞书应用ID不能为空"
    exit 1
fi

read -p "【3】飞书应用Secret: " FEISHU_APP_SECRET
if [ -z "$FEISHU_APP_SECRET" ]; then
    echo "❌ 飞书应用Secret不能为空"
    exit 1
fi

read -p "【4】Webhook Token (默认: langbot_webhook_token): " WEBHOOK_TOKEN
WEBHOOK_TOKEN=${WEBHOOK_TOKEN:-"langbot_webhook_token"}

echo ""
echo "=========================================="
echo "配置信息总结"
echo "=========================================="
echo "Dify API Key: ${DIFY_API_KEY:0:10}***"
echo "飞书应用ID: $FEISHU_APP_ID"
echo "飞书应用Secret: ${FEISHU_APP_SECRET:0:10}***"
echo "Webhook Token: $WEBHOOK_TOKEN"
echo ""

read -p "确认配置? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "❌ 已取消"
    exit 1
fi

# 更新.env文件
echo ""
echo "正在更新.env文件..."

ssh ${SERVER_USER}@${SERVER_IP} "cat > ${ENV_FILE} << 'EOF'
DIFY_API_KEY=$DIFY_API_KEY
DIFY_API_URL=https://qmsai.transsion.com
FEISHU_APP_ID=$FEISHU_APP_ID
FEISHU_APP_SECRET=$FEISHU_APP_SECRET
WEBHOOK_TOKEN=$WEBHOOK_TOKEN
LANGBOT_PORT=8080
LANGBOT_HOST=0.0.0.0
LANGBOT_DEBUG=false
LOG_LEVEL=INFO
EOF"

if [ $? -eq 0 ]; then
    echo "✅ .env文件已更新"
else
    echo "❌ .env文件更新失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 配置完成！"
echo "=========================================="
echo ""
echo "下一步: 执行部署脚本"
echo "  bash execute_langbot_deployment.sh"

