#!/usr/bin/env python3
"""
全面检查阿里云服务器部署状态
检查所有已部署的服务和文件
"""

import paramiko
import json
from datetime import datetime

SERVER_IP = "47.108.152.16"
USERNAME = "root"
PASSWORD = "Zxylsy.99"

def run_ssh_command(ssh, command):
    """执行SSH命令并返回输出"""
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return output, error
    except Exception as e:
        return "", str(e)

def main():
    print("=" * 80)
    print("🔍 全面检查阿里云服务器部署状态")
    print("=" * 80)
    print(f"服务器: {SERVER_IP}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 连接服务器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("📡 正在连接服务器...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD, timeout=10)
        print("✅ 连接成功\n")
        
        report = {
            "检查时间": datetime.now().isoformat(),
            "服务器IP": SERVER_IP,
            "检查结果": {}
        }
        
        # 1. 检查运行的进程
        print("=" * 80)
        print("1️⃣  检查运行的进程")
        print("=" * 80)
        
        processes = [
            ("Python进程", "ps aux | grep python | grep -v grep"),
            ("Node.js进程", "ps aux | grep node | grep -v grep"),
            ("Neo4j进程", "ps aux | grep neo4j | grep -v grep"),
            ("Redis进程", "ps aux | grep redis | grep -v grep"),
            ("Nginx进程", "ps aux | grep nginx | grep -v grep"),
            ("Java进程", "ps aux | grep java | grep -v grep"),
        ]
        
        report["检查结果"]["运行进程"] = {}
        
        for name, cmd in processes:
            output, error = run_ssh_command(ssh, cmd)
            if output.strip():
                print(f"✅ {name}:")
                for line in output.strip().split('\n'):
                    print(f"   {line}")
                report["检查结果"]["运行进程"][name] = output.strip().split('\n')
            else:
                print(f"❌ {name}: 未运行")
                report["检查结果"]["运行进程"][name] = "未运行"
        print()
        
        # 2. 检查监听的端口
        print("=" * 80)
        print("2️⃣  检查监听的端口")
        print("=" * 80)
        
        ports = [
            ("80", "HTTP/Nginx"),
            ("443", "HTTPS"),
            ("5173", "前端开发服务器"),
            ("8000", "API服务"),
            ("7474", "Neo4j HTTP"),
            ("7687", "Neo4j Bolt"),
            ("6379", "Redis"),
            ("3000", "Grafana"),
            ("9090", "Prometheus"),
        ]
        
        report["检查结果"]["监听端口"] = {}
        
        for port, service in ports:
            output, error = run_ssh_command(ssh, f"netstat -tlnp | grep :{port}")
            if output.strip():
                print(f"✅ 端口 {port} ({service}): 正在监听")
                print(f"   {output.strip()}")
                report["检查结果"]["监听端口"][port] = {
                    "服务": service,
                    "状态": "监听中",
                    "详情": output.strip()
                }
            else:
                print(f"❌ 端口 {port} ({service}): 未监听")
                report["检查结果"]["监听端口"][port] = {
                    "服务": service,
                    "状态": "未监听"
                }
        print()
        
        # 3. 检查项目目录和文件
        print("=" * 80)
        print("3️⃣  检查项目目录和文件")
        print("=" * 80)
        
        directories = [
            "/opt/kg",
            "/var/www/html",
            "/etc/nginx/sites-available",
            "/etc/nginx/sites-enabled",
            "/home",
            "/root",
        ]
        
        report["检查结果"]["目录结构"] = {}
        
        for directory in directories:
            output, error = run_ssh_command(ssh, f"ls -la {directory} 2>/dev/null")
            if output.strip():
                print(f"📁 {directory}:")
                lines = output.strip().split('\n')
                for line in lines[:10]:  # 只显示前10行
                    print(f"   {line}")
                if len(lines) > 10:
                    print(f"   ... (还有 {len(lines) - 10} 行)")
                report["检查结果"]["目录结构"][directory] = lines
            else:
                print(f"❌ {directory}: 不存在或无权限")
                report["检查结果"]["目录结构"][directory] = "不存在"
            print()
        
        # 4. 检查Nginx配置
        print("=" * 80)
        print("4️⃣  检查Nginx配置")
        print("=" * 80)
        
        nginx_configs = [
            "/etc/nginx/sites-available/default",
            "/etc/nginx/sites-available/knowledge-graph",
            "/etc/nginx/sites-enabled/default",
            "/etc/nginx/sites-enabled/knowledge-graph",
        ]
        
        report["检查结果"]["Nginx配置"] = {}
        
        for config in nginx_configs:
            output, error = run_ssh_command(ssh, f"cat {config} 2>/dev/null")
            if output.strip():
                print(f"✅ {config}: 存在")
                lines = output.strip().split('\n')
                print(f"   (共 {len(lines)} 行)")
                report["检查结果"]["Nginx配置"][config] = "存在"
            else:
                print(f"❌ {config}: 不存在")
                report["检查结果"]["Nginx配置"][config] = "不存在"
        print()
        
        # 5. 检查systemd服务
        print("=" * 80)
        print("5️⃣  检查systemd服务")
        print("=" * 80)
        
        services = [
            "nginx",
            "neo4j",
            "redis",
            "redis-server",
        ]
        
        report["检查结果"]["系统服务"] = {}
        
        for service in services:
            output, error = run_ssh_command(ssh, f"systemctl status {service} 2>/dev/null | head -20")
            if "Active: active" in output:
                print(f"✅ {service}: 运行中")
                report["检查结果"]["系统服务"][service] = "运行中"
            elif "could not be found" in output or "not be found" in error:
                print(f"⚪ {service}: 未安装")
                report["检查结果"]["系统服务"][service] = "未安装"
            else:
                print(f"❌ {service}: 已停止")
                report["检查结果"]["系统服务"][service] = "已停止"
        print()
        
        # 6. 查找项目文件
        print("=" * 80)
        print("6️⃣  查找项目相关文件")
        print("=" * 80)
        
        search_patterns = [
            ("main.py", "find /opt /home /root -name 'main.py' 2>/dev/null"),
            ("package.json", "find /opt /home /root -name 'package.json' 2>/dev/null"),
            ("docker-compose*.yml", "find /opt /home /root -name 'docker-compose*.yml' 2>/dev/null"),
            ("requirements.txt", "find /opt /home /root -name 'requirements.txt' 2>/dev/null"),
        ]
        
        report["检查结果"]["项目文件"] = {}
        
        for name, cmd in search_patterns:
            print(f"🔍 查找 {name}...")
            output, error = run_ssh_command(ssh, cmd)
            if output.strip():
                files = output.strip().split('\n')
                print(f"✅ 找到 {len(files)} 个文件:")
                for f in files[:5]:
                    print(f"   {f}")
                if len(files) > 5:
                    print(f"   ... (还有 {len(files) - 5} 个)")
                report["检查结果"]["项目文件"][name] = files
            else:
                print(f"❌ 未找到 {name}")
                report["检查结果"]["项目文件"][name] = []
        print()
        
        # 7. 检查环境变量和软件版本
        print("=" * 80)
        print("7️⃣  检查环境和软件版本")
        print("=" * 80)
        
        commands = [
            ("Python版本", "python3 --version 2>&1"),
            ("Node.js版本", "node --version 2>&1"),
            ("npm版本", "npm --version 2>&1"),
            ("Docker版本", "docker --version 2>&1"),
            ("Docker Compose版本", "docker-compose --version 2>&1"),
            ("系统信息", "uname -a"),
            ("内存使用", "free -h"),
            ("磁盘使用", "df -h /"),
        ]
        
        report["检查结果"]["环境信息"] = {}
        
        for name, cmd in commands:
            output, error = run_ssh_command(ssh, cmd)
            result = output.strip() if output.strip() else error.strip()
            if result and "not found" not in result.lower():
                print(f"✅ {name}:")
                print(f"   {result}")
                report["检查结果"]["环境信息"][name] = result
            else:
                print(f"❌ {name}: 未安装或不可用")
                report["检查结果"]["环境信息"][name] = "未安装"
        print()
        
        # 8. 测试HTTP端点
        print("=" * 80)
        print("8️⃣  测试HTTP端点")
        print("=" * 80)
        
        endpoints = [
            ("主页", "http://localhost/"),
            ("API健康检查", "http://localhost:8000/health"),
            ("API文档", "http://localhost:8000/docs"),
            ("Neo4j", "http://localhost:7474/"),
            ("前端", "http://localhost:5173/"),
        ]
        
        report["检查结果"]["HTTP端点"] = {}
        
        for name, url in endpoints:
            output, error = run_ssh_command(ssh, f"curl -s -o /dev/null -w '%{{http_code}}' {url} 2>&1")
            status_code = output.strip()
            if status_code.isdigit():
                code = int(status_code)
                if 200 <= code < 300:
                    print(f"✅ {name} ({url}): {code}")
                    report["检查结果"]["HTTP端点"][name] = {"url": url, "状态码": code, "状态": "正常"}
                elif 300 <= code < 400:
                    print(f"⚠️  {name} ({url}): {code} (重定向)")
                    report["检查结果"]["HTTP端点"][name] = {"url": url, "状态码": code, "状态": "重定向"}
                elif code == 502:
                    print(f"❌ {name} ({url}): {code} (Bad Gateway - 后端服务未运行)")
                    report["检查结果"]["HTTP端点"][name] = {"url": url, "状态码": code, "状态": "后端未运行"}
                else:
                    print(f"❌ {name} ({url}): {code}")
                    report["检查结果"]["HTTP端点"][name] = {"url": url, "状态码": code, "状态": "错误"}
            else:
                print(f"❌ {name} ({url}): 无法连接")
                report["检查结果"]["HTTP端点"][name] = {"url": url, "状态": "无法连接"}
        print()
        
        # 保存报告
        report_file = f"服务器部署状态报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("=" * 80)
        print("📊 检查完成")
        print("=" * 80)
        print(f"详细报告已保存到: {report_file}")
        print()
        
        # 生成总结
        print("=" * 80)
        print("📋 部署状态总结")
        print("=" * 80)
        
        running_processes = [k for k, v in report["检查结果"]["运行进程"].items() if v != "未运行"]
        listening_ports = [k for k, v in report["检查结果"]["监听端口"].items() if v.get("状态") == "监听中"]
        active_services = [k for k, v in report["检查结果"]["系统服务"].items() if v == "运行中"]
        
        print(f"✅ 运行中的进程: {len(running_processes)}")
        for p in running_processes:
            print(f"   - {p}")
        print()
        
        print(f"✅ 监听中的端口: {len(listening_ports)}")
        for p in listening_ports:
            service = report["检查结果"]["监听端口"][p]["服务"]
            print(f"   - 端口 {p} ({service})")
        print()
        
        print(f"✅ 运行中的系统服务: {len(active_services)}")
        for s in active_services:
            print(f"   - {s}")
        print()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("🔌 连接已关闭")

if __name__ == "__main__":
    main()

