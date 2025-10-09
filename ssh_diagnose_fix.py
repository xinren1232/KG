#!/usr/bin/env python3
"""使用SSH连接诊断并修复服务器"""

import time
import requests

try:
    import paramiko
except ImportError:
    print("正在安装paramiko库...")
    import subprocess
    subprocess.run(["pip", "install", "paramiko"], check=True)
    import paramiko

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
SERVER_PORT = 22

class SSHClient:
    def __init__(self):
        self.client = None
        self.project_dir = None
        
    def connect(self):
        """连接到服务器"""
        print("\n连接到服务器...")
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                SERVER_IP,
                port=SERVER_PORT,
                username=SERVER_USER,
                password=SERVER_PASSWORD,
                timeout=10
            )
            print("✓ 服务器连接成功")
            return True
        except Exception as e:
            print(f"✗ 连接失败: {e}")
            return False
    
    def exec_command(self, command, show_output=True):
        """执行SSH命令"""
        if not self.client:
            print("✗ 未连接到服务器")
            return False, "", ""
        
        try:
            if show_output:
                print(f"\n执行: {command[:80]}...")
            
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            stdout_text = stdout.read().decode('utf-8', errors='ignore')
            stderr_text = stderr.read().decode('utf-8', errors='ignore')
            exit_code = stdout.channel.recv_exit_status()
            
            if show_output and stdout_text:
                print(stdout_text)
            
            if stderr_text and "Warning" not in stderr_text:
                if show_output:
                    print(f"错误: {stderr_text}")
            
            return exit_code == 0, stdout_text, stderr_text
        except Exception as e:
            print(f"✗ 执行命令失败: {e}")
            return False, "", str(e)
    
    def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            print("\n连接已关闭")

def main():
    print("="*80)
    print("服务器全面诊断与修复")
    print("="*80)
    
    ssh = SSHClient()
    
    # 1. 连接服务器
    print("\n" + "="*80)
    print("1. 连接服务器")
    print("="*80)
    
    if not ssh.connect():
        return False
    
    try:
        # 2. 查找项目目录
        print("\n" + "="*80)
        print("2. 查找项目目录")
        print("="*80)

        project_dir = None
        for path in ["/opt/knowledge-graph", "/opt/kg", "/root/kg", "/home/kg"]:
            success, output, _ = ssh.exec_command(f"[ -d {path} ] && echo 'EXISTS' || echo 'NOT_FOUND'", show_output=False)
            if "EXISTS" in output:
                project_dir = path
                print(f"✓ 找到项目目录: {project_dir}")
                break

        if not project_dir:
            print("✗ 未找到项目目录")
            # 尝试查找
            print("尝试查找项目目录...")
            ssh.exec_command("find /opt -maxdepth 2 -name 'docker-compose*.yml' 2>/dev/null")
            return False
        
        ssh.project_dir = project_dir
        
        # 3. 检查项目文件结构
        print("\n" + "="*80)
        print("3. 检查项目文件结构")
        print("="*80)
        
        ssh.exec_command(f"ls -lh {project_dir}/ | head -20")
        
        # 4. 检查关键文件
        print("\n" + "="*80)
        print("4. 检查关键文件")
        print("="*80)
        
        files_to_check = {
            "前端API配置": f"{project_dir}/apps/web/src/api/index.js",
            "后端API": f"{project_dir}/api/main.py",
            "Docker配置": f"{project_dir}/docker-compose.prod.yml",
        }
        
        file_status = {}
        for name, path in files_to_check.items():
            success, output, _ = ssh.exec_command(f"[ -f {path} ] && echo 'EXISTS' || echo 'NOT_FOUND'", show_output=False)
            exists = "EXISTS" in output
            file_status[name] = {"path": path, "exists": exists}
            status = "✓" if exists else "✗"
            print(f"{status} {name}: {path}")
        
        # 5. 检查前端超时配置
        print("\n" + "="*80)
        print("5. 检查前端超时配置")
        print("="*80)
        
        needs_fix = False
        if file_status["前端API配置"]["exists"]:
            frontend_file = file_status["前端API配置"]["path"]
            success, output, _ = ssh.exec_command(f"grep -n 'timeout:' {frontend_file} | head -5")
            
            if "timeout: 10000" in output:
                print("⚠ 发现问题: 前端超时设置为10秒（太短）")
                print("  建议: 改为60秒")
                needs_fix = True
            elif "timeout: 60000" in output:
                print("✓ 前端超时配置正确（60秒）")
            else:
                print("? 前端超时配置未知")
        
        # 6. 检查Docker服务状态
        print("\n" + "="*80)
        print("6. 检查Docker服务状态")
        print("="*80)
        
        ssh.exec_command(f"cd {project_dir} && docker-compose -f docker-compose.prod.yml ps")
        
        # 7. 测试API响应时间
        print("\n" + "="*80)
        print("7. 测试API响应时间")
        print("="*80)
        
        test_cases = [
            {"name": "健康检查", "url": "http://47.108.152.16/api/health"},
            {"name": "图谱统计", "url": "http://47.108.152.16/api/kg/stats"},
            {"name": "小数据量图谱", "url": "http://47.108.152.16/api/kg/graph?limit=100"},
        ]
        
        for test in test_cases:
            try:
                print(f"\n测试: {test['name']}")
                start = time.time()
                r = requests.get(test['url'], timeout=30)
                elapsed = time.time() - start
                
                if r.status_code == 200:
                    print(f"  ✓ 成功 - 响应时间: {elapsed:.2f}秒")
                    
                    if '/kg/graph' in test['url']:
                        try:
                            data = r.json()
                            nodes = len(data.get('data', {}).get('sampleNodes', []))
                            rels = len(data.get('data', {}).get('sampleRelations', []))
                            print(f"    节点: {nodes}, 关系: {rels}")
                        except:
                            pass
                else:
                    print(f"  ✗ 失败 - 状态码: {r.status_code}")
            except requests.exceptions.Timeout:
                print(f"  ✗ 超时")
            except Exception as e:
                print(f"  ✗ 错误: {e}")
        
        # 8. 诊断总结
        print("\n" + "="*80)
        print("诊断报告总结")
        print("="*80)
        
        print(f"\n项目目录: {project_dir}")
        print("\n文件检查:")
        for name, info in file_status.items():
            status = "✓" if info["exists"] else "✗"
            print(f"  {status} {name}")
        
        print("\n发现的问题:")
        if needs_fix:
            print("  ⚠ 前端超时配置需要修改（10秒 → 60秒）")
        else:
            print("  未发现明显问题")
        
        # 9. 询问是否执行修复
        print("\n" + "="*80)
        print("是否执行自动修复？")
        print("="*80)
        
        print("\n修复内容:")
        print("  1. 将前端超时从10秒改为60秒")
        print("  2. 修复后端缓存逻辑bug")
        print("  3. 重启相关服务")
        
        confirm = input("\n是否继续执行修复？(y/n): ")
        
        if confirm.lower() == 'y':
            print("\n开始执行修复...")
            
            # 修复1: 修改前端超时配置
            print("\n" + "="*80)
            print("修复1: 修改前端超时配置")
            print("="*80)
            
            if file_status["前端API配置"]["exists"]:
                frontend_file = file_status["前端API配置"]["path"]
                ssh.exec_command(f"""
cd {project_dir}
cp {frontend_file} {frontend_file}.backup.$(date +%Y%m%d_%H%M%S)
sed -i 's/timeout: 10000/timeout: 60000/g' {frontend_file}
echo '✓ 前端超时配置已修改'
grep -n 'timeout:' {frontend_file} | head -3
""")
            
            # 修复2: 修改后端缓存逻辑
            print("\n" + "="*80)
            print("修复2: 修改后端缓存逻辑")
            print("="*80)
            
            if file_status["后端API"]["exists"]:
                backend_file = file_status["后端API"]["path"]
                fix_script = f"""
cd {project_dir}
cp {backend_file} {backend_file}.backup.$(date +%Y%m%d_%H%M%S)
python3 << 'ENDPYTHON'
try:
    with open('{backend_file}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\\n')
    modified = False
    
    for i in range(len(lines)):
        if 'return {{' in lines[i] and i < len(lines) - 10:
            future_lines = '\\n'.join(lines[i:min(i+30, len(lines))])
            if '# 缓存结果' in future_lines and 'QueryCache.set_graph_data' in future_lines:
                lines[i] = lines[i].replace('return {{', 'result = {{')
                modified = True
                print(f'✓ 在第 {{i+1}} 行修复了缓存逻辑')
                break
    
    if modified:
        with open('{backend_file}', 'w', encoding='utf-8') as f:
            f.write('\\n'.join(lines))
        print('✓ 后端缓存逻辑已修复')
    else:
        print('缓存逻辑可能已经正确')
except Exception as e:
    print(f'✗ 修复失败: {{e}}')
ENDPYTHON
"""
                ssh.exec_command(fix_script)
            
            # 修复3: 重启服务
            print("\n" + "="*80)
            print("修复3: 重启服务")
            print("="*80)
            
            ssh.exec_command(f"""
cd {project_dir}
echo '重启前端服务...'
docker-compose -f docker-compose.prod.yml restart web
echo '重启API服务...'
docker-compose -f docker-compose.prod.yml restart api
echo '等待服务启动...'
sleep 10
echo '检查服务状态:'
docker-compose -f docker-compose.prod.yml ps
""")
            
            print("\n" + "="*80)
            print("修复完成！")
            print("="*80)
            
            print("\n请在浏览器中测试: http://47.108.152.16/")
            print("点击 '图谱可视化' 菜单，应该不再出现超时错误")
            
        else:
            print("\n已取消修复操作")
        
    finally:
        ssh.close()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

