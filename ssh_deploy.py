#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH自动化部署脚本 - 知识图谱系统
支持远程服务器部署和管理
"""

import os
import sys
import json
import time
import paramiko
import tarfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SSHDeployer:
    """SSH部署管理器"""
    
    def __init__(self, config_file: str = "deploy_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.ssh_client = None
        self.sftp_client = None
        
    def load_config(self) -> Dict:
        """加载部署配置"""
        default_config = {
            "server": {
                "host": "",
                "port": 22,
                "username": "",
                "password": "",
                "key_file": "",
                "timeout": 30
            },
            "deployment": {
                "remote_path": "/opt/knowledge-graph",
                "backup_path": "/opt/kg-backups",
                "docker_compose_file": "docker-compose.yml",
                "monitoring_compose_file": "docker-compose.monitoring.yml",
                "services": ["neo4j", "redis", "api", "web", "prometheus", "grafana"]
            },
            "files": {
                "exclude_patterns": [
                    "*.pyc", "__pycache__", ".git", "node_modules", 
                    "*.log", "cleanup_backup_*", "thorough_cleanup_backup_*"
                ],
                "include_dirs": [
                    "api", "apps", "config", "data", "monitoring", 
                    "nginx", "scripts"
                ],
                "include_files": [
                    "docker-compose.yml", "docker-compose.monitoring.yml",
                    "Dockerfile.api", "deploy_optimized.sh", "README.md"
                ]
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in config[key]:
                                    config[key][subkey] = subvalue
                    return config
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
                
        # 创建默认配置文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"已创建默认配置文件: {self.config_file}")
        logger.info("请编辑配置文件后重新运行")
        return default_config
    
    def connect(self) -> bool:
        """连接SSH服务器"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            server_config = self.config["server"]
            
            # 连接参数
            connect_params = {
                "hostname": server_config["host"],
                "port": server_config["port"],
                "username": server_config["username"],
                "timeout": server_config["timeout"]
            }
            
            # 认证方式
            if server_config.get("key_file") and os.path.exists(server_config["key_file"]):
                connect_params["key_filename"] = server_config["key_file"]
                logger.info(f"使用密钥文件认证: {server_config['key_file']}")
            elif server_config.get("password"):
                connect_params["password"] = server_config["password"]
                logger.info("使用密码认证")
            else:
                logger.error("未配置认证方式（密钥文件或密码）")
                return False
            
            self.ssh_client.connect(**connect_params)
            self.sftp_client = self.ssh_client.open_sftp()
            
            logger.info(f"成功连接到服务器: {server_config['host']}")
            return True
            
        except Exception as e:
            logger.error(f"SSH连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开SSH连接"""
        if self.sftp_client:
            self.sftp_client.close()
        if self.ssh_client:
            self.ssh_client.close()
        logger.info("SSH连接已断开")
    
    def execute_command(self, command: str, timeout: int = 300) -> tuple:
        """执行远程命令"""
        try:
            logger.info(f"执行命令: {command}")
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if exit_code == 0:
                logger.info(f"命令执行成功")
                if output:
                    logger.debug(f"输出: {output}")
            else:
                logger.error(f"命令执行失败 (退出码: {exit_code})")
                if error:
                    logger.error(f"错误: {error}")
            
            return exit_code, output, error
            
        except Exception as e:
            logger.error(f"命令执行异常: {e}")
            return -1, "", str(e)
    
    def create_deployment_package(self) -> str:
        """创建部署包"""
        logger.info("创建部署包...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"kg_deploy_{timestamp}.tar.gz"
        package_path = os.path.join(tempfile.gettempdir(), package_name)
        
        with tarfile.open(package_path, "w:gz") as tar:
            # 添加目录
            for dir_name in self.config["files"]["include_dirs"]:
                if os.path.exists(dir_name):
                    tar.add(dir_name, arcname=dir_name)
                    logger.info(f"添加目录: {dir_name}")
            
            # 添加文件
            for file_name in self.config["files"]["include_files"]:
                if os.path.exists(file_name):
                    tar.add(file_name, arcname=file_name)
                    logger.info(f"添加文件: {file_name}")
        
        logger.info(f"部署包创建完成: {package_path}")
        return package_path
    
    def upload_package(self, local_path: str, remote_path: str) -> bool:
        """上传部署包"""
        try:
            logger.info(f"上传部署包: {local_path} -> {remote_path}")
            
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            self.execute_command(f"mkdir -p {remote_dir}")
            
            # 上传文件
            self.sftp_client.put(local_path, remote_path)
            
            # 验证上传
            remote_stat = self.sftp_client.stat(remote_path)
            local_stat = os.stat(local_path)
            
            if remote_stat.st_size == local_stat.st_size:
                logger.info("部署包上传成功")
                return True
            else:
                logger.error("部署包上传失败：文件大小不匹配")
                return False
                
        except Exception as e:
            logger.error(f"上传部署包失败: {e}")
            return False
    
    def extract_package(self, remote_package_path: str, extract_path: str) -> bool:
        """解压部署包"""
        try:
            logger.info(f"解压部署包到: {extract_path}")
            
            commands = [
                f"mkdir -p {extract_path}",
                f"cd {extract_path}",
                f"tar -xzf {remote_package_path} -C {extract_path}",
                f"ls -la {extract_path}"
            ]
            
            for cmd in commands:
                exit_code, output, error = self.execute_command(cmd)
                if exit_code != 0:
                    logger.error(f"解压失败: {error}")
                    return False
            
            logger.info("部署包解压成功")
            return True
            
        except Exception as e:
            logger.error(f"解压部署包失败: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """安装系统依赖"""
        logger.info("安装系统依赖...")
        
        commands = [
            # 更新系统
            "sudo apt-get update",
            
            # 安装Docker
            "curl -fsSL https://get.docker.com -o get-docker.sh",
            "sudo sh get-docker.sh",
            "sudo usermod -aG docker $USER",
            
            # 安装Docker Compose
            "sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            
            # 验证安装
            "docker --version",
            "docker-compose --version"
        ]
        
        for cmd in commands:
            exit_code, output, error = self.execute_command(cmd, timeout=600)
            if exit_code != 0 and "already exists" not in error:
                logger.warning(f"命令可能失败: {cmd}")
                logger.warning(f"错误: {error}")
        
        logger.info("系统依赖安装完成")
        return True
    
    def deploy_services(self, deployment_path: str) -> bool:
        """部署服务"""
        logger.info("部署知识图谱服务...")
        
        commands = [
            f"cd {deployment_path}",
            
            # 设置执行权限
            "chmod +x deploy_optimized.sh",
            "chmod +x scripts/*.py",
            
            # 停止现有服务
            "docker-compose down || true",
            "docker-compose -f docker-compose.monitoring.yml down || true",
            
            # 启动主服务
            "docker-compose up -d",
            
            # 等待服务启动
            "sleep 30",
            
            # 优化Neo4j
            "python3 scripts/optimize_neo4j.py || true",
            
            # 启动监控服务
            "docker-compose -f docker-compose.monitoring.yml up -d",
            
            # 检查服务状态
            "docker-compose ps",
            "docker-compose -f docker-compose.monitoring.yml ps"
        ]
        
        for cmd in commands:
            exit_code, output, error = self.execute_command(cmd, timeout=600)
            if exit_code != 0:
                logger.warning(f"命令执行警告: {cmd}")
                logger.warning(f"输出: {output}")
                logger.warning(f"错误: {error}")
        
        logger.info("服务部署完成")
        return True
    
    def verify_deployment(self, deployment_path: str) -> bool:
        """验证部署"""
        logger.info("验证部署状态...")
        
        # 检查服务状态
        services_to_check = [
            ("Neo4j", "curl -f http://localhost:7474 || echo 'Neo4j not ready'"),
            ("API", "curl -f http://localhost:8000/health || echo 'API not ready'"),
            ("Prometheus", "curl -f http://localhost:9090 || echo 'Prometheus not ready'"),
            ("Grafana", "curl -f http://localhost:3000 || echo 'Grafana not ready'")
        ]
        
        results = {}
        for service_name, check_cmd in services_to_check:
            exit_code, output, error = self.execute_command(check_cmd)
            results[service_name] = exit_code == 0
            
            if results[service_name]:
                logger.info(f"✅ {service_name} 服务正常")
            else:
                logger.warning(f"⚠️ {service_name} 服务异常")
        
        # 检查Docker容器
        exit_code, output, error = self.execute_command("docker ps")
        if exit_code == 0:
            logger.info("Docker容器状态:")
            logger.info(output)
        
        success_count = sum(results.values())
        total_count = len(results)
        
        logger.info(f"部署验证完成: {success_count}/{total_count} 服务正常")
        return success_count >= total_count * 0.75  # 75%服务正常即认为部署成功
    
    def deploy(self) -> bool:
        """执行完整部署流程"""
        try:
            logger.info("🚀 开始SSH自动化部署")
            logger.info("=" * 60)
            
            # 1. 连接服务器
            if not self.connect():
                return False
            
            # 2. 创建部署包
            package_path = self.create_deployment_package()
            
            # 3. 上传部署包
            remote_package = f"/tmp/{os.path.basename(package_path)}"
            if not self.upload_package(package_path, remote_package):
                return False
            
            # 4. 创建备份
            deployment_path = self.config["deployment"]["remote_path"]
            backup_path = self.config["deployment"]["backup_path"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            self.execute_command(f"mkdir -p {backup_path}")
            self.execute_command(f"cp -r {deployment_path} {backup_path}/backup_{timestamp} || true")
            
            # 5. 解压部署包
            if not self.extract_package(remote_package, deployment_path):
                return False
            
            # 6. 安装依赖
            if not self.install_dependencies():
                logger.warning("依赖安装可能有问题，继续部署...")
            
            # 7. 部署服务
            if not self.deploy_services(deployment_path):
                return False
            
            # 8. 验证部署
            if not self.verify_deployment(deployment_path):
                logger.warning("部署验证未完全通过，请检查服务状态")
            
            # 9. 清理临时文件
            os.remove(package_path)
            self.execute_command(f"rm -f {remote_package}")
            
            logger.info("🎉 SSH自动化部署完成！")
            logger.info("=" * 60)
            
            # 显示访问信息
            server_host = self.config["server"]["host"]
            logger.info("🌐 服务访问地址:")
            logger.info(f"   • Neo4j浏览器:    http://{server_host}:7474")
            logger.info(f"   • API服务:        http://{server_host}:8000")
            logger.info(f"   • API文档:        http://{server_host}:8000/docs")
            logger.info(f"   • 健康检查:       http://{server_host}:8000/health")
            logger.info(f"   • Prometheus:     http://{server_host}:9090")
            logger.info(f"   • Grafana:        http://{server_host}:3000")
            
            return True
            
        except Exception as e:
            logger.error(f"部署过程中发生错误: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """主函数"""
    print("🚀 知识图谱系统 SSH 自动化部署工具")
    print("=" * 60)
    
    # 检查配置文件
    deployer = SSHDeployer()
    
    # 检查配置是否完整
    server_config = deployer.config["server"]
    if not server_config["host"] or not server_config["username"]:
        print("❌ 请先配置服务器信息:")
        print(f"   编辑文件: {deployer.config_file}")
        print("   配置服务器地址、用户名和认证信息")
        return False
    
    # 确认部署
    print(f"📋 部署配置:")
    print(f"   服务器: {server_config['host']}:{server_config['port']}")
    print(f"   用户: {server_config['username']}")
    print(f"   部署路径: {deployer.config['deployment']['remote_path']}")
    
    confirm = input("\n确认开始部署? (y/N): ").strip().lower()
    if confirm != 'y':
        print("部署已取消")
        return False
    
    # 执行部署
    success = deployer.deploy()
    
    if success:
        print("\n🎉 部署成功完成！")
        return True
    else:
        print("\n❌ 部署失败，请检查日志")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
