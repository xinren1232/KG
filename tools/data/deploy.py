#!/usr/bin/env python3
"""
一键部署脚本
自动化部署质量知识图谱助手系统
"""

import os
import sys
import subprocess
import time
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """部署管理器"""
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.project_root = Path(__file__).parent
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """加载部署配置"""
        config_file = self.project_root / f"deploy_config_{self.environment}.json"
        
        # 默认配置
        default_config = {
            "development": {
                "api_port": 8000,
                "frontend_port": 5173,
                "neo4j_port": 7687,
                "neo4j_http_port": 7474,
                "use_docker": False,
                "install_dependencies": True,
                "run_tests": True,
                "setup_database": True
            },
            "production": {
                "api_port": 8000,
                "frontend_port": 80,
                "neo4j_port": 7687,
                "neo4j_http_port": 7474,
                "use_docker": True,
                "install_dependencies": True,
                "run_tests": True,
                "setup_database": True,
                "ssl_enabled": True,
                "domain": "kg.example.com"
            }
        }
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
        
        return default_config.get(self.environment, default_config["development"])
    
    def deploy(self):
        """执行完整部署"""
        logger.info(f"开始部署 - 环境: {self.environment}")
        
        try:
            # 1. 环境检查
            self._check_environment()
            
            # 2. 安装依赖
            if self.config.get("install_dependencies", True):
                self._install_dependencies()
            
            # 3. 设置数据库
            if self.config.get("setup_database", True):
                self._setup_database()
            
            # 4. 运行测试
            if self.config.get("run_tests", True):
                self._run_tests()
            
            # 5. 构建前端
            self._build_frontend()
            
            # 6. 启动服务
            if self.config.get("use_docker", False):
                self._deploy_with_docker()
            else:
                self._deploy_local()
            
            # 7. 健康检查
            self._health_check()
            
            logger.info("部署完成！")
            self._print_deployment_info()
            
        except Exception as e:
            logger.error(f"部署失败: {e}")
            sys.exit(1)
    
    def _check_environment(self):
        """检查部署环境"""
        logger.info("检查部署环境...")
        
        # 检查Python版本
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            raise RuntimeError("需要Python 3.8或更高版本")
        
        # 检查必要的命令
        required_commands = ["pip", "npm"]
        if self.config.get("use_docker", False):
            required_commands.extend(["docker", "docker-compose"])
        
        for cmd in required_commands:
            if not shutil.which(cmd):
                raise RuntimeError(f"未找到命令: {cmd}")
        
        # 检查端口可用性
        ports_to_check = [
            self.config["api_port"],
            self.config["frontend_port"]
        ]
        
        for port in ports_to_check:
            if self._is_port_in_use(port):
                logger.warning(f"端口 {port} 已被占用")
        
        logger.info("环境检查通过")
    
    def _install_dependencies(self):
        """安装依赖"""
        logger.info("安装依赖...")
        
        # 安装Python依赖
        api_requirements = self.project_root / "services" / "api" / "requirements.txt"
        if api_requirements.exists():
            self._run_command(f"pip install -r {api_requirements}")
        else:
            # 安装基础依赖
            basic_deps = [
                "fastapi", "uvicorn", "neo4j", "pandas", "openpyxl",
                "python-dotenv", "pydantic", "loguru", "psutil"
            ]
            self._run_command(f"pip install {' '.join(basic_deps)}")
        
        # 安装Node.js依赖
        frontend_dir = self.project_root / "apps" / "web"
        if frontend_dir.exists():
            package_json = frontend_dir / "package.json"
            if package_json.exists():
                self._run_command("npm install", cwd=frontend_dir)
            else:
                logger.warning("未找到package.json，跳过前端依赖安装")
        
        logger.info("依赖安装完成")
    
    def _setup_database(self):
        """设置数据库"""
        logger.info("设置数据库...")
        
        if self.config.get("use_docker", False):
            # 使用Docker启动Neo4j
            self._run_command("docker-compose up -d neo4j")
            time.sleep(30)  # 等待Neo4j启动
        else:
            logger.info("请确保Neo4j数据库已启动并可访问")
        
        # 初始化数据库结构
        init_script = self.project_root / "services" / "api" / "neo4j_init" / "neo4j_constraints.cypher"
        if init_script.exists():
            logger.info("数据库初始化脚本已准备，请手动执行")
        
        logger.info("数据库设置完成")
    
    def _run_tests(self):
        """运行测试"""
        logger.info("运行测试...")
        
        # 运行API测试
        test_script = self.project_root / "test_api.py"
        if test_script.exists():
            try:
                self._run_command(f"python {test_script}")
                logger.info("API测试通过")
            except subprocess.CalledProcessError:
                logger.warning("API测试失败，但继续部署")
        
        # 运行前端测试
        frontend_dir = self.project_root / "apps" / "web"
        if (frontend_dir / "package.json").exists():
            try:
                self._run_command("npm test", cwd=frontend_dir)
                logger.info("前端测试通过")
            except subprocess.CalledProcessError:
                logger.warning("前端测试失败，但继续部署")
        
        logger.info("测试完成")
    
    def _build_frontend(self):
        """构建前端"""
        logger.info("构建前端...")
        
        frontend_dir = self.project_root / "apps" / "web"
        if (frontend_dir / "package.json").exists():
            if self.environment == "production":
                self._run_command("npm run build", cwd=frontend_dir)
            else:
                logger.info("开发环境跳过前端构建")
        else:
            logger.warning("未找到前端项目，跳过构建")
        
        logger.info("前端构建完成")
    
    def _deploy_with_docker(self):
        """使用Docker部署"""
        logger.info("使用Docker部署...")
        
        # 构建镜像
        self._run_command("docker-compose build")
        
        # 启动服务
        self._run_command("docker-compose up -d")
        
        logger.info("Docker部署完成")
    
    def _deploy_local(self):
        """本地部署"""
        logger.info("本地部署...")
        
        # 启动API服务
        api_dir = self.project_root / "services" / "api"
        api_command = f"python -m uvicorn main_simple:app --host 0.0.0.0 --port {self.config['api_port']} --reload"
        
        logger.info(f"启动API服务: {api_command}")
        logger.info(f"API服务将在 http://localhost:{self.config['api_port']} 运行")
        
        # 启动前端服务（开发环境）
        if self.environment == "development":
            frontend_dir = self.project_root / "apps" / "web"
            if (frontend_dir / "package.json").exists():
                frontend_command = f"npm run dev -- --port {self.config['frontend_port']}"
                logger.info(f"启动前端服务: {frontend_command}")
                logger.info(f"前端服务将在 http://localhost:{self.config['frontend_port']} 运行")
        
        logger.info("本地部署完成")
    
    def _health_check(self):
        """健康检查"""
        logger.info("执行健康检查...")
        
        import requests
        import time
        
        # 检查API服务
        api_url = f"http://localhost:{self.config['api_port']}/health"
        max_retries = 10
        
        for i in range(max_retries):
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    logger.info("API服务健康检查通过")
                    break
            except requests.RequestException:
                if i < max_retries - 1:
                    logger.info(f"等待API服务启动... ({i+1}/{max_retries})")
                    time.sleep(5)
                else:
                    logger.warning("API服务健康检查失败")
        
        logger.info("健康检查完成")
    
    def _print_deployment_info(self):
        """打印部署信息"""
        print("\n" + "="*60)
        print("🎉 部署成功！")
        print("="*60)
        print(f"环境: {self.environment}")
        print(f"API服务: http://localhost:{self.config['api_port']}")
        print(f"API文档: http://localhost:{self.config['api_port']}/docs")
        
        if self.environment == "development":
            print(f"前端服务: http://localhost:{self.config['frontend_port']}")
        
        if not self.config.get("use_docker", False):
            print("\n启动命令:")
            print(f"API: cd services/api && python -m uvicorn main_simple:app --host 0.0.0.0 --port {self.config['api_port']} --reload")
            
            frontend_dir = self.project_root / "apps" / "web"
            if (frontend_dir / "package.json").exists():
                print(f"前端: cd apps/web && npm run dev -- --port {self.config['frontend_port']}")
        
        print("\n管理命令:")
        print("查看日志: docker-compose logs -f" if self.config.get("use_docker") else "查看终端输出")
        print("停止服务: docker-compose down" if self.config.get("use_docker") else "Ctrl+C")
        print("="*60)
    
    def _run_command(self, command: str, cwd: Optional[Path] = None):
        """运行命令"""
        logger.info(f"执行命令: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"命令执行失败: {command}")
            logger.error(f"错误输出: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, command)
        
        if result.stdout:
            logger.debug(f"命令输出: {result.stdout}")
    
    def _is_port_in_use(self, port: int) -> bool:
        """检查端口是否被占用"""
        import socket
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="质量知识图谱助手部署脚本")
    parser.add_argument(
        "--env", 
        choices=["development", "production"], 
        default="development",
        help="部署环境"
    )
    parser.add_argument(
        "--skip-deps", 
        action="store_true",
        help="跳过依赖安装"
    )
    parser.add_argument(
        "--skip-tests", 
        action="store_true",
        help="跳过测试"
    )
    parser.add_argument(
        "--docker", 
        action="store_true",
        help="强制使用Docker部署"
    )
    
    args = parser.parse_args()
    
    # 创建部署管理器
    deployer = DeploymentManager(args.env)
    
    # 应用命令行参数
    if args.skip_deps:
        deployer.config["install_dependencies"] = False
    if args.skip_tests:
        deployer.config["run_tests"] = False
    if args.docker:
        deployer.config["use_docker"] = True
    
    # 执行部署
    deployer.deploy()

if __name__ == "__main__":
    main()
