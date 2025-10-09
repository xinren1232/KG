#!/bin/bash
# 在服务器上直接修复超时问题

SERVER="root@47.108.152.16"

echo "======================================================================"
echo "修复服务器上的超时问题"
echo "======================================================================"

# 方案1: 修改前端超时配置
echo -e "\n步骤 1: 修改前端axios超时配置"
ssh $SERVER << 'ENDSSH'
cd /opt/kg

# 检查文件是否存在
if [ -f "apps/web/src/api/index.js" ]; then
    echo "找到前端API配置文件"
    # 备份原文件
    cp apps/web/src/api/index.js apps/web/src/api/index.js.backup
    # 修改超时时间从10000改为60000
    sed -i 's/timeout: 10000/timeout: 60000/g' apps/web/src/api/index.js
    echo "✓ 前端超时时间已修改为60秒"
    # 显示修改后的内容
    grep -n "timeout:" apps/web/src/api/index.js | head -5
else
    echo "✗ 前端API配置文件不存在"
fi
ENDSSH

# 方案2: 修改后端缓存逻辑
echo -e "\n步骤 2: 修改后端缓存逻辑"
ssh $SERVER << 'ENDSSH'
cd /opt/kg

# 检查文件是否存在
if [ -f "api/main.py" ]; then
    echo "找到后端API文件"
    # 备份原文件
    cp api/main.py api/main.py.backup
    
    # 修复缓存逻辑 - 将 return 改为先赋值给 result
    # 这个需要更复杂的sed命令，我们先检查是否需要修改
    if grep -q "return {" api/main.py | grep -A 15 "ok.*True" | grep -q "缓存结果"; then
        echo "需要修复缓存逻辑"
        # 这里我们使用Python脚本来修复
        python3 << 'ENDPYTHON'
import re

with open('api/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换缓存逻辑问题
# 将 return {...} 后面的缓存代码移到return之前
pattern = r'(            return \{[^}]+\})\n\n(            # 缓存结果\n            await QueryCache\.set_graph_data\(cache_key, result, depth=1, ttl=600\)\n            return result)'
replacement = r'            result = {\1[13:]}\n\n\2'

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 后端缓存逻辑已修复")
else:
    print("缓存逻辑可能已经修复或格式不同")
ENDPYTHON
    else
        echo "缓存逻辑可能已经正确"
    fi
else
    echo "✗ 后端API文件不存在"
fi
ENDSSH

# 方案3: 重启服务
echo -e "\n步骤 3: 重启服务"
ssh $SERVER << 'ENDSSH'
cd /opt/kg

echo "重启前端服务..."
docker-compose -f docker-compose.prod.yml restart web

echo "重启API服务..."
docker-compose -f docker-compose.prod.yml restart api

echo "等待服务启动..."
sleep 10

echo "检查服务状态:"
docker-compose -f docker-compose.prod.yml ps

echo -e "\n查看API日志:"
docker-compose -f docker-compose.prod.yml logs api --tail=20
ENDSSH

echo -e "\n======================================================================"
echo "修复完成！"
echo "======================================================================"
echo "请访问 http://47.108.152.16/ 测试图谱可视化功能"

