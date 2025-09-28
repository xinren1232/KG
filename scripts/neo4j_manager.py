#!/usr/bin/env python3
"""
Neo4j 数据库管理脚本
用于启动、停止、重启和检查Neo4j数据库状态
"""

import subprocess
import time
import sys
import platform
import requests
from pathlib import Path

class Neo4jManager:
    def __init__(self):
        self.system = platform.system().lower()
        self.neo4j_url = "http://localhost:7474"
        self.bolt_url = "bolt://localhost:7687"
        
    def run_command(self, command, shell=True):
        """执行系统命令"""
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "命令执行超时"
        except Exception as e:
            return False, "", str(e)
    
    def check_neo4j_status(self):
        """检查Neo4j状态"""
        try:
            response = requests.get(f"{self.neo4j_url}/db/data/", timeout=5)
            if response.status_code == 200:
                return True, "Neo4j正在运行"
            else:
                return False, f"Neo4j响应异常: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "无法连接到Neo4j"
        except Exception as e:
            return False, f"检查状态失败: {str(e)}"
    
    def start_neo4j(self):
        """启动Neo4j"""
        print("🚀 正在启动Neo4j...")
        
        if self.system == "windows":
            # Windows系统
            commands = [
                "neo4j start",
                "neo4j.bat start",
                r"C:\neo4j\bin\neo4j.bat start",
                r"C:\Program Files\Neo4j CE 4.4.0\bin\neo4j.bat start"
            ]
        else:
            # Linux/Mac系统
            commands = [
                "neo4j start",
                "sudo neo4j start",
                "/usr/bin/neo4j start",
                "systemctl start neo4j"
            ]
        
        for cmd in commands:
            print(f"尝试命令: {cmd}")
            success, stdout, stderr = self.run_command(cmd)
            if success:
                print(f"✅ Neo4j启动成功")
                print(f"输出: {stdout}")
                return True
            else:
                print(f"❌ 命令失败: {stderr}")
        
        print("❌ 所有启动命令都失败了")
        return False
    
    def stop_neo4j(self):
        """停止Neo4j"""
        print("🛑 正在停止Neo4j...")
        
        if self.system == "windows":
            commands = [
                "neo4j stop",
                "neo4j.bat stop",
                r"C:\neo4j\bin\neo4j.bat stop",
                r"C:\Program Files\Neo4j CE 4.4.0\bin\neo4j.bat stop"
            ]
        else:
            commands = [
                "neo4j stop",
                "sudo neo4j stop",
                "/usr/bin/neo4j stop",
                "systemctl stop neo4j"
            ]
        
        for cmd in commands:
            print(f"尝试命令: {cmd}")
            success, stdout, stderr = self.run_command(cmd)
            if success:
                print(f"✅ Neo4j停止成功")
                print(f"输出: {stdout}")
                return True
            else:
                print(f"❌ 命令失败: {stderr}")
        
        print("❌ 所有停止命令都失败了")
        return False
    
    def restart_neo4j(self):
        """重启Neo4j"""
        print("🔄 正在重启Neo4j...")
        
        # 先停止
        self.stop_neo4j()
        time.sleep(3)
        
        # 再启动
        return self.start_neo4j()
    
    def wait_for_neo4j(self, timeout=60):
        """等待Neo4j启动完成"""
        print("⏳ 等待Neo4j启动完成...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            is_running, message = self.check_neo4j_status()
            if is_running:
                print(f"✅ {message}")
                return True
            
            print(f"⏳ {message}, 继续等待...")
            time.sleep(2)
        
        print(f"❌ 等待超时({timeout}秒)")
        return False
    
    def get_neo4j_info(self):
        """获取Neo4j信息"""
        print("ℹ️ Neo4j信息:")
        print(f"  HTTP URL: {self.neo4j_url}")
        print(f"  Bolt URL: {self.bolt_url}")
        print(f"  操作系统: {self.system}")
        
        is_running, message = self.check_neo4j_status()
        print(f"  状态: {message}")
        
        return is_running

def main():
    manager = Neo4jManager()
    
    if len(sys.argv) < 2:
        print("Neo4j 管理脚本")
        print("用法:")
        print("  python neo4j_manager.py status   - 检查状态")
        print("  python neo4j_manager.py start    - 启动Neo4j")
        print("  python neo4j_manager.py stop     - 停止Neo4j")
        print("  python neo4j_manager.py restart  - 重启Neo4j")
        print("  python neo4j_manager.py info     - 显示信息")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        is_running, message = manager.check_neo4j_status()
        print(f"Neo4j状态: {message}")
        sys.exit(0 if is_running else 1)
    
    elif command == "start":
        if manager.start_neo4j():
            manager.wait_for_neo4j()
        sys.exit(0)
    
    elif command == "stop":
        manager.stop_neo4j()
        sys.exit(0)
    
    elif command == "restart":
        if manager.restart_neo4j():
            manager.wait_for_neo4j()
        sys.exit(0)
    
    elif command == "info":
        manager.get_neo4j_info()
        sys.exit(0)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
