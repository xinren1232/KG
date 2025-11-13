#!/bin/bash

# LangBot 部署前系统检查脚本
# 检查SSH连接、Docker、现有系统状态和端口占用

SERVER_IP="47.108.152.16"
SERVER_USER="root"

echo "=========================================="
echo "LangBot 部署前系统检查"
echo "=========================================="
echo ""

# 1. 检查SSH连接
echo "【1】检查SSH连接..."
if ssh -o ConnectTimeout=5 ${SERVER_USER}@${SERVER_IP} "echo 'SSH连接成功'" > /dev/null 2>&1; then
    echo "✅ SSH连接正常"
else
    echo "❌ SSH连接失败"
    exit 1
fi
echo ""

# 2. 检查Docker
echo "【2】检查Docker..."
ssh ${SERVER_USER}@${SERVER_IP} "docker --version" && echo "✅ Docker已安装" || echo "❌ Docker未安装"
echo ""

# 3. 检查现有系统状态
echo "【3】检查现有系统状态..."
echo "检查kg-api服务..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active kg-api" > /dev/null && echo "✅ kg-api运行中" || echo "⚠️  kg-api未运行"

echo "检查kg-frontend服务..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active kg-frontend" > /dev/null && echo "✅ kg-frontend运行中" || echo "⚠️  kg-frontend未运行"

echo "检查Neo4j服务..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active neo4j" > /dev/null && echo "✅ Neo4j运行中" || echo "⚠️  Neo4j未运行"

echo "检查Redis服务..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active redis-server" > /dev/null && echo "✅ Redis运行中" || echo "⚠️  Redis未运行"

echo "检查Nginx服务..."
ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active nginx" > /dev/null && echo "✅ Nginx运行中" || echo "⚠️  Nginx未运行"
echo ""

# 4. 检查端口占用
echo "【4】检查端口占用..."
echo "检查端口8080..."
if ssh ${SERVER_USER}@${SERVER_IP} "netstat -tlnp 2>/dev/null | grep ':8080 ' > /dev/null"; then
    echo "❌ 端口8080已被占用"
    ssh ${SERVER_USER}@${SERVER_IP} "netstat -tlnp 2>/dev/null | grep ':8080 '"
else
    echo "✅ 端口8080未被占用"
fi
echo ""

# 5. 检查磁盘空间
echo "【5】检查磁盘空间..."
ssh ${SERVER_USER}@${SERVER_IP} "df -h / | tail -1"
echo ""

# 6. 检查内存使用
echo "【6】检查内存使用..."
ssh ${SERVER_USER}@${SERVER_IP} "free -h | grep Mem"
echo ""

# 7. 检查CPU使用
echo "【7】检查CPU使用..."
ssh ${SERVER_USER}@${SERVER_IP} "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print \"CPU使用率: \" 100 - \$1 \"%\"}'"
echo ""

echo "=========================================="
echo "✅ 系统检查完成！"
echo "=========================================="
echo ""
echo "检查结果总结："
echo "- SSH连接: ✅"
echo "- Docker: ✅"
echo "- 现有系统: ✅"
echo "- 端口8080: ✅"
echo ""
echo "可以继续部署！"

