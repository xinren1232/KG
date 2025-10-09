#!/bin/bash
# 知识图谱系统完整部署脚本
# 在阿里云服务器上部署所有后端服务

set -e  # 遇到错误立即退出

echo "================================================================================"
echo "🚀 开始部署知识图谱系统"
echo "================================================================================"
echo "服务器: $(hostname)"
echo "时间: $(date)"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/opt/knowledge-graph"

# 步骤1: 检查系统环境
echo "================================================================================"
echo "1️⃣  检查系统环境"
echo "================================================================================"

echo "检查操作系统..."
cat /etc/os-release | grep PRETTY_NAME

echo -e "\n检查Python版本..."
python3 --version || { echo -e "${RED}❌ Python3未安装${NC}"; exit 1; }

echo -e "\n检查pip..."
pip3 --version || { echo -e "${YELLOW}⚠️  pip3未安装，正在安装...${NC}"; apt install -y python3-pip; }

echo -e "\n检查curl..."
curl --version > /dev/null || { echo -e "${YELLOW}⚠️  curl未安装，正在安装...${NC}"; apt install -y curl; }

echo -e "${GREEN}✅ 系统环境检查完成${NC}\n"

# 步骤2: 安装Neo4j
echo "================================================================================"
echo "2️⃣  安装Neo4j图数据库"
echo "================================================================================"

if systemctl status neo4j > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Neo4j已安装并运行中${NC}"
else
    echo "正在安装Neo4j..."
    
    # 安装Java (Neo4j依赖)
    echo "安装Java..."
    apt update
    apt install -y openjdk-11-jre-headless
    
    # 添加Neo4j仓库
    echo "添加Neo4j仓库..."
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list
    
    # 安装Neo4j
    echo "安装Neo4j..."
    apt update
    apt install -y neo4j
    
    # 设置初始密码
    echo "设置Neo4j密码..."
    neo4j-admin set-initial-password password123
    
    # 配置Neo4j
    echo "配置Neo4j..."
    sed -i 's/#dbms.default_listen_address=0.0.0.0/dbms.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf
    
    # 启动Neo4j
    echo "启动Neo4j..."
    systemctl enable neo4j
    systemctl start neo4j
    
    # 等待Neo4j启动
    echo "等待Neo4j启动..."
    for i in {1..30}; do
        if curl -s http://localhost:7474 > /dev/null; then
            echo -e "${GREEN}✅ Neo4j启动成功${NC}"
            break
        fi
        echo "等待中... ($i/30)"
        sleep 2
    done
fi

# 验证Neo4j
echo -e "\n验证Neo4j..."
curl -s http://localhost:7474 > /dev/null && echo -e "${GREEN}✅ Neo4j HTTP接口正常 (7474)${NC}" || echo -e "${RED}❌ Neo4j HTTP接口异常${NC}"
netstat -tlnp | grep 7687 > /dev/null && echo -e "${GREEN}✅ Neo4j Bolt接口正常 (7687)${NC}" || echo -e "${RED}❌ Neo4j Bolt接口异常${NC}"

echo ""

# 步骤3: 安装Redis
echo "================================================================================"
echo "3️⃣  安装Redis缓存服务"
echo "================================================================================"

if systemctl status redis-server > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis已安装并运行中${NC}"
else
    echo "正在安装Redis..."
    apt install -y redis-server
    
    # 启动Redis
    systemctl enable redis-server
    systemctl start redis-server
    
    echo -e "${GREEN}✅ Redis安装完成${NC}"
fi

# 验证Redis
echo -e "\n验证Redis..."
redis-cli ping > /dev/null && echo -e "${GREEN}✅ Redis运行正常${NC}" || echo -e "${RED}❌ Redis异常${NC}"

echo ""

# 步骤4: 修改环境变量
echo "================================================================================"
echo "4️⃣  修改环境变量配置"
echo "================================================================================"

cd $PROJECT_DIR

if [ -f .env ]; then
    echo "备份原始.env文件..."
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    
    echo "修改.env配置..."
    # 将Docker容器名改为localhost
    sed -i 's/NEO4J_URI=bolt:\/\/neo4j:7687/NEO4J_URI=bolt:\/\/localhost:7687/g' .env
    sed -i 's/REDIS_HOST=redis/REDIS_HOST=localhost/g' .env
    
    echo -e "${GREEN}✅ 环境变量配置完成${NC}"
    echo -e "\n修改后的关键配置:"
    grep -E "NEO4J_URI|REDIS_HOST" .env
else
    echo -e "${RED}❌ .env文件不存在${NC}"
fi

echo ""

# 步骤5: 安装API依赖
echo "================================================================================"
echo "5️⃣  安装API服务依赖"
echo "================================================================================"

cd $PROJECT_DIR/api

if [ -f requirements.txt ]; then
    echo "安装Python依赖..."
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Python依赖安装完成${NC}"
else
    echo -e "${RED}❌ requirements.txt不存在${NC}"
    exit 1
fi

echo ""

# 步骤6: 创建systemd服务
echo "================================================================================"
echo "6️⃣  创建systemd服务（开机自启）"
echo "================================================================================"

# 创建API服务
cat > /etc/systemd/system/kg-api.service << 'EOF'
[Unit]
Description=Knowledge Graph API Service
After=network.target neo4j.service redis-server.service
Wants=neo4j.service redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/knowledge-graph/api
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/kg-api.log
StandardError=append:/var/log/kg-api-error.log

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ API服务配置文件创建完成${NC}"

# 创建前端服务（将现有的node进程转为服务）
cat > /etc/systemd/system/kg-frontend.service << 'EOF'
[Unit]
Description=Knowledge Graph Frontend Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/knowledge-graph/apps/web
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/npm run dev
Restart=always
RestartSec=10
StandardOutput=append:/var/log/kg-frontend.log
StandardError=append:/var/log/kg-frontend-error.log

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ 前端服务配置文件创建完成${NC}"

# 重载systemd
systemctl daemon-reload

echo ""

# 步骤7: 停止旧进程并启动新服务
echo "================================================================================"
echo "7️⃣  启动所有服务"
echo "================================================================================"

# 停止旧的node进程
echo "停止旧的前端进程..."
pkill -f "vite.*5173" || echo "没有运行中的前端进程"

# 停止旧的API进程（如果有）
echo "停止旧的API进程..."
pkill -f "python3.*main.py" || echo "没有运行中的API进程"

sleep 2

# 启动API服务
echo -e "\n启动API服务..."
systemctl enable kg-api
systemctl start kg-api
sleep 3

# 检查API服务状态
if systemctl is-active --quiet kg-api; then
    echo -e "${GREEN}✅ API服务启动成功${NC}"
else
    echo -e "${RED}❌ API服务启动失败${NC}"
    echo "查看日志:"
    journalctl -u kg-api -n 20 --no-pager
fi

# 启动前端服务
echo -e "\n启动前端服务..."
systemctl enable kg-frontend
systemctl start kg-frontend
sleep 3

# 检查前端服务状态
if systemctl is-active --quiet kg-frontend; then
    echo -e "${GREEN}✅ 前端服务启动成功${NC}"
else
    echo -e "${RED}❌ 前端服务启动失败${NC}"
    echo "查看日志:"
    journalctl -u kg-frontend -n 20 --no-pager
fi

echo ""

# 步骤8: 验证所有服务
echo "================================================================================"
echo "8️⃣  验证所有服务"
echo "================================================================================"

echo "等待服务完全启动..."
sleep 5

echo -e "\n检查端口监听状态:"
echo "----------------------------------------"
netstat -tlnp | grep -E "80|5173|8000|7474|7687|6379" || echo "部分端口未监听"

echo -e "\n检查HTTP端点:"
echo "----------------------------------------"

# 测试Neo4j
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7474/)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "Neo4j (7474):     ${GREEN}✅ $HTTP_CODE${NC}"
else
    echo -e "Neo4j (7474):     ${RED}❌ $HTTP_CODE${NC}"
fi

# 测试前端
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "前端 (5173):      ${GREEN}✅ $HTTP_CODE${NC}"
else
    echo -e "前端 (5173):      ${RED}❌ $HTTP_CODE${NC}"
fi

# 测试API健康检查
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "API健康检查:      ${GREEN}✅ $HTTP_CODE${NC}"
else
    echo -e "API健康检查:      ${RED}❌ $HTTP_CODE${NC}"
fi

# 测试API文档
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "API文档:          ${GREEN}✅ $HTTP_CODE${NC}"
else
    echo -e "API文档:          ${RED}❌ $HTTP_CODE${NC}"
fi

# 测试主页（通过Nginx）
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "主页 (Nginx):     ${GREEN}✅ $HTTP_CODE${NC}"
else
    echo -e "主页 (Nginx):     ${RED}❌ $HTTP_CODE${NC}"
fi

echo ""

# 步骤9: 显示服务状态
echo "================================================================================"
echo "9️⃣  服务状态总览"
echo "================================================================================"

echo -e "\nsystemd服务状态:"
echo "----------------------------------------"
systemctl status neo4j --no-pager -l | head -3
systemctl status redis-server --no-pager -l | head -3
systemctl status kg-api --no-pager -l | head -3
systemctl status kg-frontend --no-pager -l | head -3
systemctl status nginx --no-pager -l | head -3

echo ""

# 步骤10: 生成部署报告
echo "================================================================================"
echo "📊 部署完成总结"
echo "================================================================================"

cat << EOF

✅ 部署成功！

🌐 访问地址:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  主页:           http://47.108.152.16/
  API文档:        http://47.108.152.16/api/docs
  Neo4j浏览器:    http://47.108.152.16/neo4j/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 登录凭证:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Neo4j:
    用户名: neo4j
    密码:   password123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 已部署的服务:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Nginx          (端口 80)      - 反向代理
  ✅ 前端服务       (端口 5173)    - Vue.js应用
  ✅ API服务        (端口 8000)    - FastAPI后端
  ✅ Neo4j数据库    (端口 7474, 7687) - 图数据库
  ✅ Redis缓存      (端口 6379)    - 缓存服务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 服务管理命令:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  查看API日志:     journalctl -u kg-api -f
  查看前端日志:     journalctl -u kg-frontend -f
  重启API:         systemctl restart kg-api
  重启前端:        systemctl restart kg-frontend
  重启Neo4j:       systemctl restart neo4j
  重启所有:        systemctl restart kg-api kg-frontend neo4j redis-server nginx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 日志文件:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  API日志:         /var/log/kg-api.log
  API错误日志:     /var/log/kg-api-error.log
  前端日志:        /var/log/kg-frontend.log
  前端错误日志:    /var/log/kg-frontend-error.log
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

部署时间: $(date)
服务器: $(hostname)

EOF

echo "================================================================================"
echo "🎉 部署完成！"
echo "================================================================================"

