#!/bin/bash
# 修复服务器上的图谱API，使其支持Term节点

echo "🔧 修复图谱API以支持Term节点"
echo "================================"

# 备份原文件
ssh root@47.108.152.16 "cp /opt/knowledge-graph/api/main.py /opt/knowledge-graph/api/main.py.backup"

# 修改API代码，将节点类型过滤改为支持所有类型
ssh root@47.108.152.16 "cat > /tmp/fix_graph_api.py << 'EOF'
import re

# 读取文件
with open('/opt/knowledge-graph/api/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换节点类型过滤
# 原来的: allowed = \"Component|Symptom|Tool|Process|TestCase|Material|Role|Metric\"
# 改为支持所有节点类型，或者添加Term|Category|Tag

old_pattern = r'allowed = \"Component\|Symptom\|Tool\|Process\|TestCase\|Material\|Role\|Metric\"'
new_pattern = 'allowed = \"Term|Category|Tag|Component|Symptom|Tool|Process|TestCase|Material|Role|Metric\"'

content = re.sub(old_pattern, new_pattern, content)

# 保存文件
with open('/opt/knowledge-graph/api/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ API代码已更新')
EOF
"

# 执行修复脚本
ssh root@47.108.152.16 "python3 /tmp/fix_graph_api.py"

# 重启API服务
echo ""
echo "🔄 重启API服务..."
ssh root@47.108.152.16 "systemctl restart kg-api"

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 测试API
echo ""
echo "🧪 测试图谱API..."
ssh root@47.108.152.16 "curl -s 'http://localhost:8000/kg/graph?limit=20' | python3 -m json.tool | head -80"

echo ""
echo "✅ 修复完成！"

