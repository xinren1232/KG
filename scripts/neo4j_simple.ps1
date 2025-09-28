param([string]$Action = "status")

Write-Host "Neo4j Desktop Manager" -ForegroundColor Cyan

if ($Action -eq "status") {
    Write-Host "Checking Neo4j status..." -ForegroundColor Yellow
    
    # Check processes
    $processes = Get-Process -Name "*Neo4j*" -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Host "Neo4j Desktop is running ($($processes.Count) processes)" -ForegroundColor Green
    } else {
        Write-Host "Neo4j Desktop is not running" -ForegroundColor Red
    }
    
    # Check ports
    $port7474 = netstat -an | Select-String ":7474.*LISTENING"
    $port7687 = netstat -an | Select-String ":7687.*LISTENING"
    
    if ($port7474) {
        Write-Host "Port 7474 (HTTP): LISTENING" -ForegroundColor Green
    } else {
        Write-Host "Port 7474 (HTTP): NOT LISTENING" -ForegroundColor Red
    }
    
    if ($port7687) {
        Write-Host "Port 7687 (Bolt): LISTENING" -ForegroundColor Green
    } else {
        Write-Host "Port 7687 (Bolt): NOT LISTENING" -ForegroundColor Red
    }
    
    # Test connection
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7474" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "HTTP connection: SUCCESS" -ForegroundColor Green
    } catch {
        Write-Host "HTTP connection: FAILED" -ForegroundColor Red
    }
}

if ($Action -eq "restart") {
    Write-Host "Restarting Neo4j..." -ForegroundColor Yellow
    
    # Stop processes
    $processes = Get-Process -Name "*Neo4j*" -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Host "Stopping Neo4j processes..." -ForegroundColor Yellow
        $processes | Stop-Process -Force
        Start-Sleep -Seconds 3
    }
    
    # Start Neo4j Desktop
    $paths = @(
        "$env:LOCALAPPDATA\Programs\Neo4j Desktop\Neo4j Desktop.exe",
        "$env:PROGRAMFILES\Neo4j Desktop\Neo4j Desktop.exe"
    )
    
    foreach ($path in $paths) {
        if (Test-Path $path) {
            Write-Host "Starting Neo4j Desktop..." -ForegroundColor Yellow
            Start-Process -FilePath $path
            break
        }
    }
    
    Write-Host "Please manually start the database instance in Neo4j Desktop" -ForegroundColor Yellow
}

if ($Action -eq "open") {
    Start-Process "http://localhost:7474"
}
