#!/bin/bash

# 质量知识图谱系统 - 构建和部署脚本
# 用于阿里云服务器部署

set -e

echo "========================================="
echo "质量知识图谱系统 - 构建和部署"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 步骤1: 构建前端
echo -e "\n${YELLOW}步骤1: 构建前端应用${NC}"
cd apps/web

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 构建前端
echo "构建前端..."
npm run build

# 检查构建结果
if [ ! -d "dist" ]; then
    echo -e "${RED}错误: 前端构建失败，dist目录不存在${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 前端构建成功${NC}"

# 返回项目根目录
cd ../..

# 步骤2: 复制构建文件到项目根目录
echo -e "\n${YELLOW}步骤2: 准备部署文件${NC}"
if [ -d "dist" ]; then
    rm -rf dist
fi
cp -r apps/web/dist ./dist
echo -e "${GREEN}✓ 构建文件已复制到 ./dist${NC}"

# 步骤3: 使用HTTP配置替换nginx配置
echo -e "\n${YELLOW}步骤3: 更新Nginx配置${NC}"
if [ -f "nginx/nginx.http.conf" ]; then
    cp nginx/nginx.http.conf nginx/nginx.conf
    echo -e "${GREEN}✓ Nginx配置已更新为HTTP模式${NC}"
else
    echo -e "${YELLOW}警告: nginx.http.conf不存在，跳过配置更新${NC}"
fi

# 步骤4: 停止现有容器
echo -e "\n${YELLOW}步骤4: 停止现有容器${NC}"
docker-compose -f docker-compose.prod.yml down
echo -e "${GREEN}✓ 容器已停止${NC}"

# 步骤5: 重新构建并启动容器
echo -e "\n${YELLOW}步骤5: 启动服务${NC}"
docker-compose -f docker-compose.prod.yml up -d --build

# 步骤6: 等待服务启动
echo -e "\n${YELLOW}步骤6: 等待服务启动${NC}"
sleep 10

# 步骤7: 检查服务状态
echo -e "\n${YELLOW}步骤7: 检查服务状态${NC}"
docker-compose -f docker-compose.prod.yml ps

# 步骤8: 检查nginx日志
echo -e "\n${YELLOW}步骤8: 检查Nginx日志${NC}"
docker-compose -f docker-compose.prod.yml logs nginx --tail=20

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "\n访问地址: ${GREEN}http://47.108.152.16/${NC}"
echo -e "API地址: ${GREEN}http://47.108.152.16/api/${NC}"
echo -e "健康检查: ${GREEN}http://47.108.152.16/health${NC}"
echo -e "\n查看日志命令:"
echo -e "  docker-compose -f docker-compose.prod.yml logs -f nginx"
echo -e "  docker-compose -f docker-compose.prod.yml logs -f api"
echo ""

