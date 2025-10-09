#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器诊断脚本 - 检查阿里云服务器上的部署状态
"""

import subprocess
import sys
import json

SERVER_IP = "47.108.152.16"
SERVER_USER = "root"
SERVER_PATH = "/opt/kg"

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}{title}{Colors.NC}")
    print('='*60)

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.NC}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.NC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.NC}")

def run_ssh_command(cmd):
    """在服务器上执行命令"""
    full_cmd = f'ssh {SERVER_USER}@{SERVER_IP} "{cmd}"'
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_ssh_connection():
    """检查SSH连接"""
    print_section("1. 检查SSH连接")
    success, stdout, stderr = run_ssh_command("echo 'SSH连接成功'")
    if success:
        print_success("SSH连接正常")
        return True
    else:
        print_error(f"SSH连接失败: {stderr}")
        return False

def check_docker_status():
    """检查Docker状态"""
    print_section("2. 检查Docker服务")
    
    # 检查Docker是否运行
    success, stdout, stderr = run_ssh_command("docker --version")
    if success:
        print_success(f"Docker已安装: {stdout.strip()}")
    else:
        print_error("Docker未安装或未运行")
        return False
    
    # 检查Docker Compose
    success, stdout, stderr = run_ssh_command("docker-compose --version")
    if success:
        print_success(f"Docker Compose已安装: {stdout.strip()}")
    else:
        print_error("Docker Compose未安装")
        return False
    
    return True

def check_containers():
    """检查容器状态"""
    print_section("3. 检查容器状态")
    
    cmd = f"cd {SERVER_PATH} && docker-compose -f docker-compose.prod.yml ps"
    success, stdout, stderr = run_ssh_command(cmd)
    
    if success:
        print(stdout)
        
        # 检查关键容器
        containers = {
            'kg_nginx_prod': 'Nginx',
            'kg_api_prod': 'API服务',
            'kg_neo4j_prod': 'Neo4j数据库',
            'kg_redis_prod': 'Redis缓存'
        }
        
        for container, name in containers.items():
            if container in stdout and 'Up' in stdout:
                print_success(f"{name} 运行中")
            else:
                print_error(f"{name} 未运行")
    else:
        print_error(f"无法获取容器状态: {stderr}")
        return False
    
    return True

def check_api_logs():
    """检查API日志"""
    print_section("4. 检查API服务日志")
    
    cmd = f"cd {SERVER_PATH} && docker-compose -f docker-compose.prod.yml logs api --tail=50"
    success, stdout, stderr = run_ssh_command(cmd)
    
    if success:
        print(stdout)
        
        # 检查常见错误
        if "error" in stdout.lower() or "exception" in stdout.lower():
            print_warning("发现错误信息，请查看上面的日志")
        if "redis" in stdout.lower() and "error" in stdout.lower():
            print_error("Redis连接可能有问题")
        if "neo4j" in stdout.lower() and "error" in stdout.lower():
            print_error("Neo4j连接可能有问题")
    else:
        print_error(f"无法获取API日志: {stderr}")

def check_nginx_logs():
    """检查Nginx日志"""
    print_section("5. 检查Nginx日志")
    
    cmd = f"cd {SERVER_PATH} && docker-compose -f docker-compose.prod.yml logs nginx --tail=30"
    success, stdout, stderr = run_ssh_command(cmd)
    
    if success:
        print(stdout)
    else:
        print_error(f"无法获取Nginx日志: {stderr}")

def check_api_health():
    """检查API健康状态"""
    print_section("6. 检查API健康状态")
    
    # 从容器内部检查
    cmd = f"cd {SERVER_PATH} && docker exec kg_api_prod curl -s http://localhost:8000/health"
    success, stdout, stderr = run_ssh_command(cmd)
    
    if success:
        print_success("API健康检查通过")
        print(f"响应: {stdout}")
    else:
        print_error(f"API健康检查失败: {stderr}")
        
        # 检查API是否在监听
        cmd = f"cd {SERVER_PATH} && docker exec kg_api_prod netstat -tlnp | grep 8000"
        success2, stdout2, stderr2 = run_ssh_command(cmd)
        if success2:
            print(f"端口监听状态: {stdout2}")
        else:
            print_error("API服务可能未启动")

def check_file_structure():
    """检查文件结构"""
    print_section("7. 检查文件结构")
    
    files_to_check = [
        "dist/index.html",
        "nginx/nginx.conf",
        "docker-compose.prod.yml",
        "api/main.py",
        "config/frontend_real_data.json"
    ]
    
    for file in files_to_check:
        cmd = f"test -f {SERVER_PATH}/{file} && echo 'exists' || echo 'missing'"
        success, stdout, stderr = run_ssh_command(cmd)
        
        if 'exists' in stdout:
            print_success(f"{file} 存在")
        else:
            print_error(f"{file} 缺失")

def check_api_endpoint():
    """检查API端点"""
    print_section("8. 测试API端点")
    
    # 测试/kg/real-stats端点
    cmd = f"cd {SERVER_PATH} && docker exec kg_api_prod curl -s http://localhost:8000/kg/real-stats"
    success, stdout, stderr = run_ssh_command(cmd)
    
    if success:
        try:
            data = json.loads(stdout)
            if data.get('ok') or data.get('success'):
                print_success("/kg/real-stats 端点正常")
                print(f"数据: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
            else:
                print_error(f"/kg/real-stats 返回错误: {data}")
        except:
            print_error(f"/kg/real-stats 返回非JSON数据: {stdout[:200]}")
    else:
        print_error(f"/kg/real-stats 请求失败: {stderr}")

def get_recommendations():
    """提供修复建议"""
    print_section("修复建议")
    
    print(f"""
{Colors.YELLOW}常见问题和解决方案:{Colors.NC}

1. API服务502错误:
   - 检查API容器是否正常运行
   - 查看API日志中的错误信息
   - 确认Redis和Neo4j连接正常
   
   修复命令:
   ssh {SERVER_USER}@{SERVER_IP}
   cd {SERVER_PATH}
   docker-compose -f docker-compose.prod.yml restart api
   docker-compose -f docker-compose.prod.yml logs -f api

2. Redis连接错误:
   - 检查Redis容器状态
   - 确认环境变量配置正确
   
   修复命令:
   docker-compose -f docker-compose.prod.yml restart redis
   docker-compose -f docker-compose.prod.yml restart api

3. Neo4j连接错误:
   - 检查Neo4j容器状态
   - 确认密码配置正确
   
   修复命令:
   docker-compose -f docker-compose.prod.yml restart neo4j
   docker-compose -f docker-compose.prod.yml restart api

4. 完全重启所有服务:
   cd {SERVER_PATH}
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d
   docker-compose -f docker-compose.prod.yml logs -f
    """)

def main():
    print(f"""
{'='*60}
阿里云服务器诊断工具
服务器: {SERVER_IP}
{'='*60}
    """)
    
    # 执行检查
    if not check_ssh_connection():
        print_error("\n无法连接到服务器，请检查:")
        print("  1. 服务器IP是否正确")
        print("  2. SSH密钥是否配置")
        print("  3. 网络连接是否正常")
        sys.exit(1)
    
    check_docker_status()
    check_containers()
    check_file_structure()
    check_api_health()
    check_api_endpoint()
    check_api_logs()
    check_nginx_logs()
    get_recommendations()
    
    print(f"\n{'='*60}")
    print(f"{Colors.GREEN}诊断完成{Colors.NC}")
    print('='*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n诊断已取消")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

