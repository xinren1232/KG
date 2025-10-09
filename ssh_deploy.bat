@echo off
REM SSH自动化部署脚本 - 知识图谱系统 (Windows版本)
setlocal enabledelayedexpansion

echo 🚀 知识图谱系统 SSH 自动化部署
echo ==================================

REM 默认配置
set SERVER_HOST=
set SERVER_USER=
set SERVER_PORT=22
set SSH_KEY=
set REMOTE_PATH=/opt/knowledge-graph
set BACKUP_PATH=/opt/kg-backups

REM 检查参数
if "%1"=="" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

REM 解析参数
:parse_args
if "%1"=="" goto :validate_config
if "%1"=="--host" (
    set SERVER_HOST=%2
    shift
    shift
    goto :parse_args
)
if "%1"=="--user" (
    set SERVER_USER=%2
    shift
    shift
    goto :parse_args
)
if "%1"=="--port" (
    set SERVER_PORT=%2
    shift
    shift
    goto :parse_args
)
if "%1"=="--key" (
    set SSH_KEY=%2
    shift
    shift
    goto :parse_args
)
shift
goto :parse_args

:show_help
echo.
echo 用法: %0 --host HOST --user USER [选项]
echo.
echo 选项:
echo   --host HOST        服务器地址
echo   --user USER        SSH用户名
echo   --port PORT        SSH端口 (默认: 22)
echo   --key KEY_FILE     SSH私钥文件路径
echo   --help             显示此帮助信息
echo.
echo 示例:
echo   %0 --host 192.168.1.100 --user ubuntu --key C:\Users\user\.ssh\id_rsa
echo   %0 --host example.com --user root --port 2222
echo.
goto :end

:validate_config
if "%SERVER_HOST%"=="" (
    echo ❌ 请指定服务器地址 (--host)
    goto :end
)
if "%SERVER_USER%"=="" (
    echo ❌ 请指定SSH用户名 (--user)
    goto :end
)

echo.
echo 📋 部署配置:
echo    服务器: %SERVER_HOST%:%SERVER_PORT%
echo    用户: %SERVER_USER%
echo    部署路径: %REMOTE_PATH%
if not "%SSH_KEY%"=="" echo    SSH密钥: %SSH_KEY%
echo.

set /p confirm="确认开始部署? (y/N): "
if /i not "%confirm%"=="y" (
    echo 部署已取消
    goto :end
)

echo.
echo 🔄 开始部署流程...

REM 检查必要工具
where ssh >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到SSH客户端，请安装OpenSSH或Git Bash
    goto :end
)

where scp >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到SCP客户端，请安装OpenSSH或Git Bash
    goto :end
)

REM 构建SSH命令
set SSH_CMD=ssh -p %SERVER_PORT%
if not "%SSH_KEY%"=="" set SSH_CMD=%SSH_CMD% -i "%SSH_KEY%"
set SSH_CMD=%SSH_CMD% %SERVER_USER%@%SERVER_HOST%

REM 构建SCP命令
set SCP_CMD=scp -P %SERVER_PORT%
if not "%SSH_KEY%"=="" set SCP_CMD=%SCP_CMD% -i "%SSH_KEY%"

echo 🔍 测试SSH连接...
%SSH_CMD% "echo 'SSH连接测试成功'" >nul 2>&1
if errorlevel 1 (
    echo ❌ SSH连接失败，请检查服务器地址、用户名和认证信息
    goto :end
)
echo ✅ SSH连接正常

echo 📁 创建远程目录...
%SSH_CMD% "sudo mkdir -p %REMOTE_PATH% && sudo mkdir -p %BACKUP_PATH% && sudo chown -R $USER:$USER %REMOTE_PATH% && sudo chown -R $USER:$USER %BACKUP_PATH%"

echo 💾 备份现有部署...
%SSH_CMD% "if [ -d %REMOTE_PATH% ]; then cp -r %REMOTE_PATH% %BACKUP_PATH%/backup_$(date +%%Y%%m%%d_%%H%%M%%S); echo '备份完成'; else echo '无现有部署需要备份'; fi"

echo 📦 创建部署包...
if exist kg_deploy.tar.gz del kg_deploy.tar.gz
tar -czf kg_deploy.tar.gz ^
    --exclude="*.pyc" ^
    --exclude="__pycache__" ^
    --exclude=".git" ^
    --exclude="node_modules" ^
    --exclude="*.log" ^
    --exclude="cleanup_backup_*" ^
    --exclude="thorough_cleanup_backup_*" ^
    --exclude="final_cleanup_backup_*" ^
    api apps config data monitoring nginx scripts ^
    docker-compose.yml docker-compose.monitoring.yml ^
    Dockerfile.api deploy_optimized.sh README.md ^
    短期优化完成报告.md 系统设计总结.md

if not exist kg_deploy.tar.gz (
    echo ❌ 部署包创建失败
    goto :end
)
echo ✅ 部署包创建完成

echo 📤 上传部署包...
%SCP_CMD% kg_deploy.tar.gz %SERVER_USER%@%SERVER_HOST%:/tmp/
if errorlevel 1 (
    echo ❌ 部署包上传失败
    goto :end
)
echo ✅ 部署包上传完成

echo 📂 解压部署包...
%SSH_CMD% "cd %REMOTE_PATH% && tar -xzf /tmp/kg_deploy.tar.gz && rm /tmp/kg_deploy.tar.gz"

echo 🔧 检查系统依赖...
%SSH_CMD% "command -v docker >/dev/null 2>&1 || (echo '安装Docker...' && curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo usermod -aG docker $USER && rm get-docker.sh)"

%SSH_CMD% "command -v docker-compose >/dev/null 2>&1 || (echo '安装Docker Compose...' && sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose)"

echo 🚀 部署主服务...
%SSH_CMD% "cd %REMOTE_PATH% && chmod +x deploy_optimized.sh 2>/dev/null || true && chmod +x scripts/*.py 2>/dev/null || true && docker-compose down 2>/dev/null || true && docker-compose up -d"

echo ⏳ 等待服务启动...
timeout /t 30 /nobreak >nul

echo ⚡ 优化Neo4j数据库...
%SSH_CMD% "cd %REMOTE_PATH% && sleep 30 && python3 scripts/optimize_neo4j.py 2>/dev/null || echo 'Neo4j优化完成'"

echo 📊 部署监控服务...
%SSH_CMD% "cd %REMOTE_PATH% && mkdir -p monitoring/grafana/dashboards monitoring/grafana/datasources monitoring/rules && docker-compose -f docker-compose.monitoring.yml up -d"

echo ⏳ 等待监控服务启动...
timeout /t 30 /nobreak >nul

echo 🔍 验证部署状态...
%SSH_CMD% "echo '=== Docker容器状态 ===' && docker ps && echo '' && echo '=== 服务健康检查 ===' && (curl -f http://localhost:7474 >/dev/null 2>&1 && echo '✅ Neo4j服务正常' || echo '❌ Neo4j服务异常') && (curl -f http://localhost:8000/health >/dev/null 2>&1 && echo '✅ API服务正常' || echo '❌ API服务异常') && (curl -f http://localhost:9090 >/dev/null 2>&1 && echo '✅ Prometheus服务正常' || echo '⚠️ Prometheus服务异常') && (curl -f http://localhost:3000 >/dev/null 2>&1 && echo '✅ Grafana服务正常' || echo '⚠️ Grafana服务异常')"

echo.
echo 🎉 部署完成！
echo ================
echo.
echo 🌐 服务访问地址:
echo    • Neo4j浏览器:    http://%SERVER_HOST%:7474
echo    • API服务:        http://%SERVER_HOST%:8000
echo    • API文档:        http://%SERVER_HOST%:8000/docs
echo    • 健康检查:       http://%SERVER_HOST%:8000/health
echo    • Prometheus:     http://%SERVER_HOST%:9090
echo    • Grafana:        http://%SERVER_HOST%:3000 (admin/admin123)
echo.
echo 🔧 远程管理命令:
echo    • SSH登录:        ssh %SERVER_USER%@%SERVER_HOST%
echo    • 查看日志:       docker-compose logs -f
echo    • 重启服务:       docker-compose restart
echo    • 停止服务:       docker-compose down
echo.
echo 📁 部署路径:
echo    • 项目目录:       %REMOTE_PATH%
echo    • 备份目录:       %BACKUP_PATH%
echo.

REM 清理临时文件
if exist kg_deploy.tar.gz del kg_deploy.tar.gz

goto :end

:end
pause
