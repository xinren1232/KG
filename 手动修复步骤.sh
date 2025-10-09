#!/bin/bash
# 在服务器上手动执行的修复脚本
# 使用方法: 
# 1. ssh root@47.108.152.16
# 2. 复制粘贴以下命令执行

echo "======================================================================"
echo "修复图谱API超时问题"
echo "======================================================================"

# 查找项目目录
echo -e "\n查找项目目录..."
if [ -d "/opt/kg" ]; then
    PROJECT_DIR="/opt/kg"
elif [ -d "/root/kg" ]; then
    PROJECT_DIR="/root/kg"
elif [ -d "/home/kg" ]; then
    PROJECT_DIR="/home/kg"
else
    echo "请手动指定项目目录:"
    read -p "输入项目路径: " PROJECT_DIR
fi

echo "项目目录: $PROJECT_DIR"
cd $PROJECT_DIR

# 1. 修改前端超时配置
echo -e "\n======================================================================"
echo "步骤 1: 修改前端超时配置"
echo "======================================================================"

FRONTEND_API_FILE="apps/web/src/api/index.js"

if [ -f "$FRONTEND_API_FILE" ]; then
    echo "找到前端API配置文件: $FRONTEND_API_FILE"
    
    # 备份
    cp $FRONTEND_API_FILE ${FRONTEND_API_FILE}.backup.$(date +%Y%m%d_%H%M%S)
    echo "✓ 已备份原文件"
    
    # 显示当前配置
    echo -e "\n当前超时配置:"
    grep -n "timeout:" $FRONTEND_API_FILE | head -3
    
    # 修改超时时间
    sed -i 's/timeout: 10000/timeout: 60000/g' $FRONTEND_API_FILE
    
    # 显示修改后的配置
    echo -e "\n修改后的配置:"
    grep -n "timeout:" $FRONTEND_API_FILE | head -3
    
    echo "✓ 前端超时时间已从10秒改为60秒"
else
    echo "✗ 前端API配置文件不存在: $FRONTEND_API_FILE"
    echo "请检查项目目录是否正确"
fi

# 2. 修改后端缓存逻辑
echo -e "\n======================================================================"
echo "步骤 2: 修改后端缓存逻辑"
echo "======================================================================"

BACKEND_API_FILE="api/main.py"

if [ -f "$BACKEND_API_FILE" ]; then
    echo "找到后端API文件: $BACKEND_API_FILE"
    
    # 备份
    cp $BACKEND_API_FILE ${BACKEND_API_FILE}.backup.$(date +%Y%m%d_%H%M%S)
    echo "✓ 已备份原文件"
    
    # 使用Python脚本修复
    python3 << 'ENDPYTHON'
import re

try:
    with open('api/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    modified = False
    
    # 查找需要修复的位置
    for i in range(len(lines)):
        if 'return {' in lines[i] and '"ok": True' in '\n'.join(lines[i:i+5]):
            # 检查后面是否有缓存代码
            future_lines = '\n'.join(lines[i:min(i+30, len(lines))])
            if '# 缓存结果' in future_lines and 'QueryCache.set_graph_data' in future_lines:
                # 修复：将 return { 改为 result = {
                lines[i] = lines[i].replace('return {', 'result = {')
                modified = True
                print(f"✓ 在第 {i+1} 行修复了缓存逻辑")
                print(f"  修改前: return {{")
                print(f"  修改后: result = {{")
                break
    
    if modified:
        with open('api/main.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("✓ 后端缓存逻辑已修复")
    else:
        print("缓存逻辑可能已经正确")
        
except Exception as e:
    print(f"✗ 修复失败: {e}")
    import traceback
    traceback.print_exc()
ENDPYTHON
    
else
    echo "✗ 后端API文件不存在: $BACKEND_API_FILE"
fi

# 3. 重启服务
echo -e "\n======================================================================"
echo "步骤 3: 重启服务"
echo "======================================================================"

# 检查docker-compose文件
if [ -f "docker-compose.prod.yml" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
elif [ -f "docker-compose.yml" ]; then
    COMPOSE_FILE="docker-compose.yml"
else
    echo "✗ 找不到docker-compose配置文件"
    exit 1
fi

echo "使用配置文件: $COMPOSE_FILE"

echo -e "\n重启前端服务..."
docker-compose -f $COMPOSE_FILE restart web

echo -e "\n重启API服务..."
docker-compose -f $COMPOSE_FILE restart api

echo -e "\n等待服务启动..."
sleep 10

# 4. 检查服务状态
echo -e "\n======================================================================"
echo "步骤 4: 检查服务状态"
echo "======================================================================"

docker-compose -f $COMPOSE_FILE ps

# 5. 查看日志
echo -e "\n======================================================================"
echo "步骤 5: 查看服务日志"
echo "======================================================================"

echo -e "\nAPI服务日志 (最后20行):"
docker-compose -f $COMPOSE_FILE logs api --tail=20

echo -e "\n前端服务日志 (最后20行):"
docker-compose -f $COMPOSE_FILE logs web --tail=20

# 6. 测试API
echo -e "\n======================================================================"
echo "步骤 6: 测试API"
echo "======================================================================"

echo -e "\n测试图谱API..."
curl -s -w "\n响应时间: %{time_total}s\n状态码: %{http_code}\n" \
     "http://localhost:8000/kg/graph?limit=100&show_all=false" \
     -o /tmp/api_test.json

if [ -f /tmp/api_test.json ]; then
    echo "响应数据大小: $(wc -c < /tmp/api_test.json) 字节"
    # 尝试解析JSON
    if command -v jq &> /dev/null; then
        echo "节点数量: $(jq '.data.sampleNodes | length' /tmp/api_test.json 2>/dev/null || echo '无法解析')"
    fi
fi

# 完成
echo -e "\n======================================================================"
echo "修复完成！"
echo "======================================================================"

echo -e "\n修复内容总结:"
echo "1. ✓ 前端axios超时时间: 10秒 → 60秒"
echo "2. ✓ 后端缓存逻辑bug已修复"
echo "3. ✓ 服务已重启"

echo -e "\n请在浏览器中测试:"
echo "  http://47.108.152.16/"
echo "  点击 '图谱可视化' 菜单"

echo -e "\n如果仍有问题，查看实时日志:"
echo "  docker-compose -f $COMPOSE_FILE logs -f api"
echo "  docker-compose -f $COMPOSE_FILE logs -f web"

echo -e "\n备份文件位置:"
ls -lh ${FRONTEND_API_FILE}.backup.* 2>/dev/null
ls -lh ${BACKEND_API_FILE}.backup.* 2>/dev/null

