#!/bin/bash
# 检查服务器目录结构

SERVER="root@47.108.152.16"

echo "======================================================================"
echo "检查服务器目录结构"
echo "======================================================================"

echo -e "\n检查 /opt/kg 目录:"
ssh $SERVER "ls -la /opt/kg/ 2>&1 | head -20"

echo -e "\n检查 apps 目录:"
ssh $SERVER "ls -la /opt/kg/apps/ 2>&1"

echo -e "\n检查 api 目录:"
ssh $SERVER "ls -la /opt/kg/api/ 2>&1 | head -20"

echo -e "\n检查 Docker 容器状态:"
ssh $SERVER "cd /opt/kg && docker-compose -f docker-compose.prod.yml ps"

echo -e "\n检查前端容器内部结构:"
ssh $SERVER "docker exec kg-web-1 ls -la /app/src/api/ 2>&1"

echo -e "\n======================================================================"
echo "检查完成"
echo "======================================================================"

