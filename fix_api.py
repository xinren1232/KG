#!/usr/bin/env python3
import shutil

# 备份
shutil.copy('/opt/knowledge-graph/api/main.py', '/opt/knowledge-graph/api/main.py.backup')

# 读取文件
with open('/opt/knowledge-graph/api/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换
old_text = 'allowed = "Component|Symptom|Tool|Process|TestCase|Material|Role|Metric"'
new_text = 'allowed = "Term|Category|Tag|Component|Symptom|Tool|Process|TestCase|Material|Role|Metric"'

if old_text in content:
    content = content.replace(old_text, new_text)
    print('✅ 找到并替换了节点类型过滤')
else:
    print('⚠️ 未找到目标文本，尝试查找类似文本...')
    # 查找包含allowed的行
    for i, line in enumerate(content.split('\n'), 1):
        if 'allowed =' in line and 'Component' in line:
            print(f'第{i}行: {line}')

# 保存
with open('/opt/knowledge-graph/api/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ 文件已更新')

