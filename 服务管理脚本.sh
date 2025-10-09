#!/bin/bash
# 知识图谱系统服务管理脚本集合

# 创建 kg-status 脚本
cat > /usr/local/bin/kg-status << 'EOF'
#!/bin/bash
echo "========================================="
echo "   知识图谱系统服务状态"
echo "========================================="
echo ""

echo "📊 systemd服务状态:"
echo "-------------------"
printf "%-15s %s\n" "Neo4j:" "$(systemctl is-active neo4j)"
printf "%-15s %s\n" "Redis:" "$(systemctl is-active redis-server)"
printf "%-15s %s\n" "API:" "$(systemctl is-active kg-api)"
printf "%-15s %s\n" "前端:" "$(systemctl is-active kg-frontend 2>/dev/null || echo 'not-configured')"
printf "%-15s %s\n" "Nginx:" "$(systemctl is-active nginx)"

echo ""
echo "🔌 端口监听状态:"
echo "-------------------"
netstat -tlnp 2>/dev/null | grep -E ':(80|5173|8000|7474|7687|6379) ' | awk '{
    port = $4; 
    gsub(/.*:/, "", port); 
    process = $7; 
    gsub(/\/.*/, "", process);
    
    if (port == "80") service = "Nginx";
    else if (port == "5173") service = "前端";
    else if (port == "8000") service = "API";
    else if (port == "7474") service = "Neo4j HTTP";
    else if (port == "7687") service = "Neo4j Bolt";
    else if (port == "6379") service = "Redis";
    else service = "未知";
    
    printf "%-15s %-10s (PID: %s)\n", service, port, process;
}'

echo ""
echo "💾 进程信息:"
echo "-------------------"
ps aux | grep -E 'java.*neo4j|redis-server|python3 main.py|vite.*5173|nginx: master' | grep -v grep | awk '{
    printf "PID: %-7s CPU: %-5s MEM: %-5s CMD: %s %s %s\n", $2, $3"%", $4"%", $11, $12, $13
}'

echo ""
echo "🏥 健康检查:"
echo "-------------------"

# API健康检查
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API服务: 正常 (http://localhost:8000)"
else
    echo "❌ API服务: 异常"
fi

# 前端健康检查
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "✅ 前端服务: 正常 (http://localhost:5173)"
else
    echo "❌ 前端服务: 异常"
fi

# Neo4j健康检查
if curl -s http://localhost:7474/ > /dev/null 2>&1; then
    echo "✅ Neo4j: 正常 (http://localhost:7474)"
else
    echo "❌ Neo4j: 异常"
fi

# Redis健康检查
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: 正常 (localhost:6379)"
else
    echo "❌ Redis: 异常"
fi

# Nginx健康检查
if curl -s http://localhost/ > /dev/null 2>&1; then
    echo "✅ Nginx: 正常 (http://localhost)"
else
    echo "❌ Nginx: 异常"
fi

echo ""
echo "========================================="
EOF

chmod +x /usr/local/bin/kg-status

# 创建 kg-start 脚本
cat > /usr/local/bin/kg-start << 'EOF'
#!/bin/bash
echo "▶️  启动所有知识图谱服务..."
echo ""

echo "1️⃣  启动Redis..."
systemctl start redis-server
sleep 2

echo "2️⃣  启动Neo4j..."
systemctl start neo4j
echo "   等待Neo4j完全启动..."
sleep 8

echo "3️⃣  启动API服务..."
systemctl start kg-api
sleep 3

echo "4️⃣  启动前端服务..."
if systemctl list-unit-files | grep -q kg-frontend.service; then
    systemctl start kg-frontend
else
    echo "   ⚠️  前端服务未配置systemd，使用nohup启动..."
    pkill -f 'vite.*5173'
    cd /opt/knowledge-graph/apps/web
    nohup npm run dev > /var/log/kg-frontend.log 2>&1 &
fi
sleep 3

echo "5️⃣  重启Nginx..."
systemctl restart nginx

echo ""
echo "✅ 所有服务启动完成！"
echo ""
/usr/local/bin/kg-status
EOF

chmod +x /usr/local/bin/kg-start

# 创建 kg-stop 脚本
cat > /usr/local/bin/kg-stop << 'EOF'
#!/bin/bash
echo "⏹️  停止所有知识图谱服务..."
echo ""

echo "1️⃣  停止前端服务..."
if systemctl list-unit-files | grep -q kg-frontend.service; then
    systemctl stop kg-frontend
else
    pkill -f 'vite.*5173'
fi

echo "2️⃣  停止API服务..."
systemctl stop kg-api

echo "3️⃣  停止Neo4j..."
systemctl stop neo4j

echo "4️⃣  停止Redis..."
systemctl stop redis-server

echo ""
echo "✅ 所有服务已停止"
EOF

chmod +x /usr/local/bin/kg-stop

# 创建 kg-restart 脚本
cat > /usr/local/bin/kg-restart << 'EOF'
#!/bin/bash
echo "🔄 重启所有知识图谱服务..."
echo ""

/usr/local/bin/kg-stop
sleep 3
/usr/local/bin/kg-start
EOF

chmod +x /usr/local/bin/kg-restart

# 创建 kg-health 脚本
cat > /usr/local/bin/kg-health << 'EOF'
#!/bin/bash
echo "🏥 知识图谱系统健康检查"
echo "========================================="
echo ""

# 检查API
echo -n "API服务 (8000): "
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 正常"
else
    echo "❌ 异常"
fi

# 检查前端
echo -n "前端服务 (5173): "
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo "✅ 正常"
else
    echo "❌ 异常"
fi

# 检查Neo4j
echo -n "Neo4j (7474): "
if curl -s http://localhost:7474/ > /dev/null 2>&1; then
    echo "✅ 正常"
else
    echo "❌ 异常"
fi

# 检查Redis
echo -n "Redis (6379): "
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ 正常"
else
    echo "❌ 异常"
fi

# 检查Nginx
echo -n "Nginx (80): "
if curl -s http://localhost/ > /dev/null 2>&1; then
    echo "✅ 正常"
else
    echo "❌ 异常"
fi

echo ""
echo "📈 API详细状态:"
echo "-------------------"
curl -s http://localhost:8000/health 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "无法获取API状态"

echo ""
echo "========================================="
EOF

chmod +x /usr/local/bin/kg-health

# 创建 kg-logs 脚本
cat > /usr/local/bin/kg-logs << 'EOF'
#!/bin/bash
SERVICE=${1:-all}

case $SERVICE in
    api)
        echo "📋 API服务日志:"
        tail -f /var/log/kg-api.log
        ;;
    frontend)
        echo "📋 前端服务日志:"
        tail -f /var/log/kg-frontend.log
        ;;
    neo4j)
        echo "📋 Neo4j日志:"
        tail -f /var/log/neo4j/neo4j.log
        ;;
    redis)
        echo "📋 Redis日志:"
        tail -f /var/log/redis/redis-server.log
        ;;
    nginx)
        echo "📋 Nginx访问日志:"
        tail -f /var/log/nginx/access.log
        ;;
    error)
        echo "📋 所有错误日志:"
        tail -f /var/log/kg-api-error.log /var/log/kg-frontend-error.log /var/log/nginx/error.log
        ;;
    all)
        echo "📋 所有服务日志 (最近50行):"
        echo ""
        echo "=== API ==="
        tail -20 /var/log/kg-api.log 2>/dev/null || echo "无日志"
        echo ""
        echo "=== 前端 ==="
        tail -20 /var/log/kg-frontend.log 2>/dev/null || echo "无日志"
        echo ""
        echo "=== Neo4j ==="
        tail -10 /var/log/neo4j/neo4j.log 2>/dev/null || echo "无日志"
        ;;
    *)
        echo "用法: kg-logs [api|frontend|neo4j|redis|nginx|error|all]"
        echo ""
        echo "示例:"
        echo "  kg-logs api       - 查看API日志"
        echo "  kg-logs frontend  - 查看前端日志"
        echo "  kg-logs error     - 查看所有错误日志"
        echo "  kg-logs all       - 查看所有日志摘要"
        ;;
esac
EOF

chmod +x /usr/local/bin/kg-logs

echo "✅ 所有服务管理脚本已创建！"
echo ""
echo "可用命令:"
echo "  kg-status   - 查看所有服务状态"
echo "  kg-start    - 启动所有服务"
echo "  kg-stop     - 停止所有服务"
echo "  kg-restart  - 重启所有服务"
echo "  kg-health   - 健康检查"
echo "  kg-logs     - 查看日志"

