# Neo4j Desktop 管理脚本

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("status", "start", "stop", "restart", "open")]
    [string]$Action
)

Write-Host "🔍 Neo4j Desktop 管理工具" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

function Get-Neo4jStatus {
    Write-Host "📊 检查Neo4j状态..." -ForegroundColor Yellow
    
    # 检查Neo4j Desktop进程
    $desktopProcesses = Get-Process -Name "*Neo4j Desktop*" -ErrorAction SilentlyContinue
    if ($desktopProcesses) {
        Write-Host "✅ Neo4j Desktop 正在运行 ($($desktopProcesses.Count) 个进程)" -ForegroundColor Green
        foreach ($proc in $desktopProcesses) {
            Write-Host "   - PID: $($proc.Id), 内存: $([math]::Round($proc.WorkingSet/1MB, 2)) MB" -ForegroundColor Gray
        }
    } else {
        Write-Host "❌ Neo4j Desktop 未运行" -ForegroundColor Red
    }
    
    # 检查端口
    Write-Host "`n🌐 检查Neo4j端口..." -ForegroundColor Yellow
    
    $port7474 = netstat -an | Select-String ":7474.*LISTENING"
    $port7687 = netstat -an | Select-String ":7687.*LISTENING"
    
    if ($port7474) {
        Write-Host "✅ HTTP端口 7474: 正在监听" -ForegroundColor Green
        Write-Host "   Web界面: http://localhost:7474" -ForegroundColor Gray
    } else {
        Write-Host "❌ HTTP端口 7474: 未监听" -ForegroundColor Red
    }
    
    if ($port7687) {
        Write-Host "✅ Bolt端口 7687: 正在监听" -ForegroundColor Green
        Write-Host "   连接地址: bolt://localhost:7687" -ForegroundColor Gray
    } else {
        Write-Host "❌ Bolt端口 7687: 未监听" -ForegroundColor Red
    }
    
    # 尝试HTTP连接测试
    Write-Host "`n🔗 测试连接..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7474" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ HTTP连接成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ HTTP连接失败: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Start-Neo4jDesktop {
    Write-Host "🚀 启动Neo4j Desktop..." -ForegroundColor Yellow
    
    # 查找Neo4j Desktop安装路径
    $possiblePaths = @(
        "$env:LOCALAPPDATA\Programs\Neo4j Desktop\Neo4j Desktop.exe",
        "$env:PROGRAMFILES\Neo4j Desktop\Neo4j Desktop.exe",
        "${env:PROGRAMFILES(X86)}\Neo4j Desktop\Neo4j Desktop.exe"
    )
    
    $neo4jPath = $null
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $neo4jPath = $path
            break
        }
    }
    
    if ($neo4jPath) {
        Write-Host "📍 找到Neo4j Desktop: $neo4jPath" -ForegroundColor Gray
        Start-Process -FilePath $neo4jPath
        Write-Host "✅ Neo4j Desktop 启动命令已执行" -ForegroundColor Green
        Write-Host "⏳ 请在Neo4j Desktop中手动启动数据库实例" -ForegroundColor Yellow
    } else {
        Write-Host "❌ 未找到Neo4j Desktop安装路径" -ForegroundColor Red
        Write-Host "💡 请手动启动Neo4j Desktop应用程序" -ForegroundColor Yellow
    }
}

function Stop-Neo4jProcesses {
    Write-Host "🛑 停止Neo4j进程..." -ForegroundColor Yellow
    
    $processes = Get-Process -Name "*Neo4j*" -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($proc in $processes) {
            try {
                Write-Host "🔄 停止进程: $($proc.ProcessName) (PID: $($proc.Id))" -ForegroundColor Gray
                $proc.Kill()
                Write-Host "✅ 进程已停止" -ForegroundColor Green
            } catch {
                Write-Host "❌ 无法停止进程: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "ℹ️ 没有找到Neo4j进程" -ForegroundColor Blue
    }
}

function Open-Neo4jBrowser {
    Write-Host "🌐 打开Neo4j浏览器..." -ForegroundColor Yellow
    Start-Process "http://localhost:7474"
}

# 主逻辑
switch ($Action) {
    "status" {
        Get-Neo4jStatus
    }
    "start" {
        Start-Neo4jDesktop
        Start-Sleep -Seconds 3
        Get-Neo4jStatus
    }
    "stop" {
        Stop-Neo4jProcesses
        Start-Sleep -Seconds 2
        Get-Neo4jStatus
    }
    "restart" {
        Write-Host "🔄 重启Neo4j..." -ForegroundColor Yellow
        Stop-Neo4jProcesses
        Start-Sleep -Seconds 3
        Start-Neo4jDesktop
        Start-Sleep -Seconds 5
        Get-Neo4jStatus
    }
    "open" {
        Open-Neo4jBrowser
    }
}

Write-Host "`n📋 可用命令:" -ForegroundColor Cyan
Write-Host "  status  - 检查状态" -ForegroundColor Gray
Write-Host "  start   - 启动Neo4j Desktop" -ForegroundColor Gray
Write-Host "  stop    - 停止所有Neo4j进程" -ForegroundColor Gray
Write-Host "  restart - 重启Neo4j" -ForegroundColor Gray
Write-Host "  open    - 打开Neo4j浏览器" -ForegroundColor Gray
