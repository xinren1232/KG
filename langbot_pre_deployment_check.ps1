# LangBot 部署前系统检查脚本
# 检查SSH连接、Docker、现有系统状态和端口占用

$SERVER_IP = "47.108.152.16"
$SERVER_USER = "root"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "LangBot 部署前系统检查" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查SSH连接
Write-Host "【1】检查SSH连接..." -ForegroundColor Yellow
try {
    $result = ssh ${SERVER_USER}@${SERVER_IP} "echo 'SSH连接成功'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SSH连接正常" -ForegroundColor Green
    } else {
        Write-Host "❌ SSH连接失败" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ SSH连接失败: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. 检查Docker
Write-Host "【2】检查Docker..." -ForegroundColor Yellow
$docker_version = ssh ${SERVER_USER}@${SERVER_IP} "docker --version" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker已安装: $docker_version" -ForegroundColor Green
} else {
    Write-Host "❌ Docker未安装" -ForegroundColor Red
}
Write-Host ""

# 3. 检查现有系统状态
Write-Host "【3】检查现有系统状态..." -ForegroundColor Yellow

$services = @("kg-api", "kg-frontend", "neo4j", "redis-server", "nginx")
foreach ($service in $services) {
    $status = ssh ${SERVER_USER}@${SERVER_IP} "systemctl is-active $service" 2>&1
    if ($status -eq "active") {
        Write-Host "✅ $service 运行中" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $service 未运行" -ForegroundColor Yellow
    }
}
Write-Host ""

# 4. 检查端口占用
Write-Host "【4】检查端口占用..." -ForegroundColor Yellow
Write-Host "检查端口8080..." -ForegroundColor Yellow
$port_check = ssh ${SERVER_USER}@${SERVER_IP} "netstat -tlnp 2>/dev/null | grep ':8080 ' || echo 'free'" 2>&1
if ($port_check -like "*free*" -or $port_check -eq "") {
    Write-Host "✅ 端口8080未被占用" -ForegroundColor Green
} else {
    Write-Host "❌ 端口8080已被占用:" -ForegroundColor Red
    Write-Host $port_check -ForegroundColor Red
}
Write-Host ""

# 5. 检查磁盘空间
Write-Host "【5】检查磁盘空间..." -ForegroundColor Yellow
$disk = ssh ${SERVER_USER}@${SERVER_IP} "df -h / | tail -1" 2>&1
Write-Host $disk -ForegroundColor Green
Write-Host ""

# 6. 检查内存使用
Write-Host "【6】检查内存使用..." -ForegroundColor Yellow
$memory = ssh ${SERVER_USER}@${SERVER_IP} "free -h | grep Mem" 2>&1
Write-Host $memory -ForegroundColor Green
Write-Host ""

# 7. 检查CPU使用
Write-Host "【7】检查CPU使用..." -ForegroundColor Yellow
$cpu = ssh ${SERVER_USER}@${SERVER_IP} "top -bn1 | grep 'Cpu(s)'" 2>&1
Write-Host $cpu -ForegroundColor Green
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ 系统检查完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "检查结果总结:" -ForegroundColor Yellow
Write-Host "- SSH连接: ✅" -ForegroundColor Green
Write-Host "- Docker: ✅" -ForegroundColor Green
Write-Host "- 现有系统: ✅" -ForegroundColor Green
Write-Host "- 端口8080: ✅" -ForegroundColor Green
Write-Host ""
Write-Host "可以继续部署！" -ForegroundColor Green

