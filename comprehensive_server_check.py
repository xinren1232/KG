#!/usr/bin/env python3
"""全面检查服务器状态"""

try:
    import paramiko
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "paramiko"], check=True)
    import paramiko

import time
import requests
import json

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"

def exec_ssh(client, command, show_output=True):
    """执行SSH命令"""
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')
        
        if show_output and output:
            print(output)
        if error and "Warning" not in error and show_output:
            print(f"错误: {error}")
        
        return output, error
    except Exception as e:
        print(f"执行命令失败: {e}")
        return "", str(e)

def main():
    print("="*80)
    print("服务器全面状态检查")
    print("="*80)
    print(f"服务器: {SERVER_IP}")
    print(f"检查时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # 连接服务器
    print("\n连接到服务器...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=10)
        print("✓ 服务器连接成功\n")
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False
    
    try:
        # 1. 系统基本信息
        print("\n" + "="*80)
        print("1. 系统基本信息")
        print("="*80)
        
        print("\n系统版本:")
        exec_ssh(client, "cat /etc/os-release | grep PRETTY_NAME")
        
        print("\n系统运行时间:")
        exec_ssh(client, "uptime")
        
        print("\n内核版本:")
        exec_ssh(client, "uname -r")
        
        # 2. 资源使用情况
        print("\n" + "="*80)
        print("2. 系统资源使用情况")
        print("="*80)
        
        print("\nCPU使用率:")
        exec_ssh(client, "top -bn1 | grep 'Cpu(s)' | head -1")
        
        print("\n内存使用:")
        exec_ssh(client, "free -h")
        
        print("\n磁盘使用:")
        exec_ssh(client, "df -h | grep -E '^/dev|Filesystem'")
        
        # 3. 项目目录信息
        print("\n" + "="*80)
        print("3. 项目目录信息")
        print("="*80)
        
        project_dir = "/opt/knowledge-graph"
        print(f"\n项目目录: {project_dir}")
        
        print("\n目录大小:")
        exec_ssh(client, f"du -sh {project_dir}")
        
        print("\n主要文件:")
        exec_ssh(client, f"ls -lh {project_dir}/ | head -20")
        
        # 4. Docker状态
        print("\n" + "="*80)
        print("4. Docker服务状态")
        print("="*80)
        
        print("\nDocker版本:")
        exec_ssh(client, "docker --version")
        
        print("\nDocker Compose版本:")
        exec_ssh(client, "docker-compose --version")
        
        print("\n运行中的容器:")
        output, _ = exec_ssh(client, "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
        
        if not output.strip() or "NAMES" not in output:
            print("⚠ 没有运行中的Docker容器")
        
        print("\n所有容器（包括停止的）:")
        exec_ssh(client, "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'")
        
        print("\nDocker镜像:")
        exec_ssh(client, "docker images | head -10")
        
        # 5. 进程检查
        print("\n" + "="*80)
        print("5. 关键进程检查")
        print("="*80)
        
        print("\nPython进程:")
        output, _ = exec_ssh(client, "ps aux | grep python | grep -v grep | head -10")
        if output.strip():
            print(output)
        else:
            print("未找到Python进程")
        
        print("\nNode/Vite进程:")
        output, _ = exec_ssh(client, "ps aux | grep -E 'node|vite' | grep -v grep | head -10")
        if output.strip():
            print(output)
        else:
            print("未找到Node/Vite进程")
        
        print("\nNginx进程:")
        output, _ = exec_ssh(client, "ps aux | grep nginx | grep -v grep")
        if output.strip():
            print(output)
        else:
            print("未找到Nginx进程")
        
        # 6. 端口监听
        print("\n" + "="*80)
        print("6. 端口监听状态")
        print("="*80)
        
        print("\n监听的端口:")
        exec_ssh(client, "netstat -tlnp | grep LISTEN | grep -E '80|8000|3000|5173|7474|7687'")
        
        # 7. Systemd服务
        print("\n" + "="*80)
        print("7. Systemd服务状态")
        print("="*80)
        
        print("\n查找相关服务:")
        output, _ = exec_ssh(client, "systemctl list-units --type=service --all | grep -E 'kg|knowledge|nginx|docker'")
        if output.strip():
            print(output)
        else:
            print("未找到相关systemd服务")
        
        # 8. Neo4j状态
        print("\n" + "="*80)
        print("8. Neo4j数据库状态")
        print("="*80)
        
        print("\nNeo4j进程:")
        output, _ = exec_ssh(client, "ps aux | grep neo4j | grep -v grep")
        if output.strip():
            print(output)
        else:
            print("未找到Neo4j进程")
        
        print("\nNeo4j端口:")
        exec_ssh(client, "netstat -tlnp | grep -E '7474|7687'")
        
        # 9. 日志检查
        print("\n" + "="*80)
        print("9. 最近的系统日志")
        print("="*80)
        
        print("\n系统日志（最近10条错误）:")
        exec_ssh(client, "journalctl -p err -n 10 --no-pager")
        
        # 10. 网络连接
        print("\n" + "="*80)
        print("10. 网络连接状态")
        print("="*80)
        
        print("\n活动连接数:")
        exec_ssh(client, "netstat -an | grep ESTABLISHED | wc -l")
        
        print("\n外部连接:")
        exec_ssh(client, "netstat -an | grep ESTABLISHED | grep -E ':80|:8000' | head -10")
        
        # 11. 检查修复后的文件
        print("\n" + "="*80)
        print("11. 检查修复后的配置")
        print("="*80)
        
        print("\n前端超时配置:")
        exec_ssh(client, f"grep -n 'timeout:' {project_dir}/apps/web/src/api/index.js | head -3")
        
        print("\n备份文件:")
        exec_ssh(client, f"ls -lh {project_dir}/apps/web/src/api/index.js.backup* 2>/dev/null || echo '无备份文件'")
        exec_ssh(client, f"ls -lh {project_dir}/api/main.py.backup* 2>/dev/null || echo '无备份文件'")
        
        # 12. API测试
        print("\n" + "="*80)
        print("12. API功能测试")
        print("="*80)
        
        api_tests = [
            {"name": "健康检查", "url": f"http://{SERVER_IP}/api/health"},
            {"name": "图谱统计", "url": f"http://{SERVER_IP}/api/kg/stats"},
            {"name": "图谱数据", "url": f"http://{SERVER_IP}/api/kg/graph?limit=10"},
        ]
        
        for test in api_tests:
            try:
                print(f"\n测试: {test['name']}")
                start = time.time()
                r = requests.get(test['url'], timeout=10)
                elapsed = time.time() - start
                
                if r.status_code == 200:
                    print(f"  ✓ 成功 - 响应时间: {elapsed:.2f}秒, 状态码: {r.status_code}")
                else:
                    print(f"  ✗ 失败 - 状态码: {r.status_code}")
            except Exception as e:
                print(f"  ✗ 错误: {e}")
        
        # 13. 总结
        print("\n" + "="*80)
        print("检查总结")
        print("="*80)
        
        # 收集关键信息
        summary = {
            "服务器IP": SERVER_IP,
            "检查时间": time.strftime('%Y-%m-%d %H:%M:%S'),
            "项目目录": project_dir,
            "状态": []
        }
        
        # 检查Docker容器
        output, _ = exec_ssh(client, "docker ps", show_output=False)
        if "CONTAINER ID" in output and len(output.split('\n')) > 1:
            summary["状态"].append("✓ Docker容器运行中")
        else:
            summary["状态"].append("⚠ Docker容器未运行")
        
        # 检查API
        try:
            r = requests.get(f"http://{SERVER_IP}/api/health", timeout=5)
            if r.status_code == 200:
                summary["状态"].append("✓ API服务正常")
            else:
                summary["状态"].append("⚠ API服务异常")
        except:
            summary["状态"].append("⚠ API服务不可访问")
        
        # 检查前端
        try:
            r = requests.get(f"http://{SERVER_IP}/", timeout=5)
            if r.status_code == 200:
                summary["状态"].append("✓ 前端服务正常")
            else:
                summary["状态"].append("⚠ 前端服务异常")
        except:
            summary["状态"].append("⚠ 前端服务不可访问")
        
        print(f"\n服务器: {summary['服务器IP']}")
        print(f"检查时间: {summary['检查时间']}")
        print(f"项目目录: {summary['项目目录']}")
        print("\n状态:")
        for status in summary["状态"]:
            print(f"  {status}")
        
        print("\n" + "="*80)
        print("检查完成")
        print("="*80)
        
    finally:
        client.close()
        print("\n连接已关闭")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n检查已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

