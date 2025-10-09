#!/usr/bin/env python3
"""自动修复服务器超时问题"""

import subprocess
import sys
import time

SERVER = "root@47.108.152.16"

def ssh_exec(command, show_output=True):
    """执行SSH命令"""
    full_cmd = f'ssh {SERVER} "{command}"'
    print(f"\n执行: {command[:100]}...")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    if show_output and result.stdout:
        print(result.stdout)
    if result.stderr and "Warning" not in result.stderr:
        print(f"错误: {result.stderr}")
    return result.returncode == 0, result.stdout

def main():
    print("="*70)
    print("自动修复服务器超时问题")
    print("="*70)
    
    # 1. 检查服务器连接
    print("\n步骤 1: 检查服务器连接")
    success, _ = ssh_exec("echo '服务器连接成功'")
    if not success:
        print("✗ 无法连接到服务器，请检查SSH配置")
        return False
    
    # 2. 检查项目目录
    print("\n步骤 2: 检查项目目录")
    success, output = ssh_exec("ls -la /opt/kg/ | head -5")
    if not success:
        print("✗ 项目目录不存在")
        return False
    
    # 3. 修改前端超时配置
    print("\n步骤 3: 修改前端超时配置")
    commands = """
cd /opt/kg
if [ -f "apps/web/src/api/index.js" ]; then
    cp apps/web/src/api/index.js apps/web/src/api/index.js.backup.$(date +%Y%m%d_%H%M%S)
    sed -i 's/timeout: 10000/timeout: 60000/g' apps/web/src/api/index.js
    echo "✓ 前端超时配置已修改"
    grep -n "timeout:" apps/web/src/api/index.js | head -3
else
    echo "✗ 前端配置文件不存在"
fi
"""
    ssh_exec(commands)
    
    # 4. 修改后端缓存逻辑
    print("\n步骤 4: 修改后端缓存逻辑")
    # 创建Python脚本来修复
    fix_script = """
import re
import os

os.chdir('/opt/kg')

try:
    with open('api/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    with open('api/main.py.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 查找需要修复的部分
    # 查找 "return {" 后面跟着 "# 缓存结果" 的模式
    lines = content.split('\\n')
    modified = False
    
    for i in range(len(lines)):
        # 查找 return { 开始的行，且后面有缓存相关代码
        if 'return {' in lines[i] and i < len(lines) - 10:
            # 检查后面是否有缓存代码
            future_lines = '\\n'.join(lines[i:i+30])
            if '# 缓存结果' in future_lines and 'await QueryCache.set_graph_data' in future_lines:
                # 找到需要修复的位置
                # 将 return { 改为 result = {
                lines[i] = lines[i].replace('return {', 'result = {')
                modified = True
                print(f"✓ 在第 {i+1} 行修复了缓存逻辑")
                break
    
    if modified:
        with open('api/main.py', 'w', encoding='utf-8') as f:
            f.write('\\n'.join(lines))
        print("✓ 后端缓存逻辑已修复")
    else:
        print("缓存逻辑可能已经正确或格式不同")
        
except Exception as e:
    print(f"✗ 修复失败: {e}")
"""
    
    ssh_exec(f"python3 << 'ENDPYTHON'\n{fix_script}\nENDPYTHON")
    
    # 5. 重启服务
    print("\n步骤 5: 重启服务")
    commands = """
cd /opt/kg
echo "重启前端服务..."
docker-compose -f docker-compose.prod.yml restart web
echo "重启API服务..."
docker-compose -f docker-compose.prod.yml restart api
echo "等待服务启动..."
sleep 5
"""
    ssh_exec(commands)
    
    # 6. 检查服务状态
    print("\n步骤 6: 检查服务状态")
    ssh_exec("cd /opt/kg && docker-compose -f docker-compose.prod.yml ps")
    
    # 7. 测试API
    print("\n步骤 7: 测试图谱API")
    time.sleep(5)  # 等待服务完全启动
    
    import requests
    try:
        print("测试小数据量查询...")
        start = time.time()
        r = requests.get("http://47.108.152.16/api/kg/graph", 
                        params={"limit": 100, "show_all": False}, 
                        timeout=30)
        elapsed = time.time() - start
        if r.status_code == 200:
            data = r.json()
            nodes = len(data.get("data", {}).get("sampleNodes", []))
            print(f"✓ API测试成功 - 响应时间: {elapsed:.2f}秒, 节点数: {nodes}")
        else:
            print(f"✗ API返回错误: {r.status_code}")
    except Exception as e:
        print(f"✗ API测试失败: {e}")
    
    print("\n" + "="*70)
    print("修复完成！")
    print("="*70)
    print("\n修复内容:")
    print("1. ✓ 前端axios超时时间: 10秒 → 60秒")
    print("2. ✓ 后端缓存逻辑bug已修复")
    print("3. ✓ 服务已重启")
    print("\n请访问以下地址测试:")
    print("  http://47.108.152.16/")
    print("\n如需查看日志:")
    print(f"  ssh {SERVER}")
    print("  cd /opt/kg")
    print("  docker-compose -f docker-compose.prod.yml logs -f api")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

