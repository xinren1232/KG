# PowerShell脚本 - 诊断并修复服务器超时问题
# 使用方法: .\diagnose_and_fix.ps1

$SERVER = "root@47.108.152.16"
$PASSWORD = "Zxylsy.99"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "服务器全面诊断" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 函数：执行SSH命令
function Invoke-SSHCommand {
    param(
        [string]$Command,
        [bool]$ShowOutput = $true
    )
    
    Write-Host "`n执行: $($Command.Substring(0, [Math]::Min(80, $Command.Length)))..." -ForegroundColor Yellow
    
    # 使用plink或ssh
    $result = echo $PASSWORD | ssh -o StrictHostKeyChecking=no $SERVER $Command 2>&1
    
    if ($ShowOutput) {
        Write-Host $result
    }
    
    return $result
}

# 1. 测试服务器连接
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "1. 测试服务器连接" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

try {
    $result = Invoke-SSHCommand -Command "echo '连接成功'"
    if ($result -match "连接成功") {
        Write-Host "✓ 服务器连接正常" -ForegroundColor Green
    } else {
        Write-Host "✗ 服务器连接失败" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ 无法连接到服务器: $_" -ForegroundColor Red
    exit 1
}

# 2. 查找项目目录
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "2. 查找项目目录" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$projectDir = $null
$possiblePaths = @("/opt/kg", "/root/kg", "/home/kg")

foreach ($path in $possiblePaths) {
    $result = Invoke-SSHCommand -Command "[ -d $path ] && echo 'EXISTS' || echo 'NOT_FOUND'" -ShowOutput $false
    if ($result -match "EXISTS") {
        $projectDir = $path
        Write-Host "✓ 找到项目目录: $projectDir" -ForegroundColor Green
        break
    }
}

if (-not $projectDir) {
    Write-Host "✗ 未找到项目目录" -ForegroundColor Red
    exit 1
}

# 3. 检查项目文件结构
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "3. 检查项目文件结构" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

Invoke-SSHCommand -Command "ls -lh $projectDir/ | head -20"

# 4. 检查关键文件
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "4. 检查关键文件" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$filesToCheck = @{
    "前端API配置" = "$projectDir/apps/web/src/api/index.js"
    "后端API" = "$projectDir/api/main.py"
    "Docker配置" = "$projectDir/docker-compose.prod.yml"
}

$fileStatus = @{}
foreach ($name in $filesToCheck.Keys) {
    $path = $filesToCheck[$name]
    $result = Invoke-SSHCommand -Command "[ -f $path ] && echo 'EXISTS' || echo 'NOT_FOUND'" -ShowOutput $false
    $exists = $result -match "EXISTS"
    $fileStatus[$name] = @{
        "path" = $path
        "exists" = $exists
    }
    
    if ($exists) {
        Write-Host "✓ $name : $path" -ForegroundColor Green
    } else {
        Write-Host "✗ $name : $path" -ForegroundColor Red
    }
}

# 5. 检查前端超时配置
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "5. 检查前端超时配置" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

if ($fileStatus["前端API配置"].exists) {
    $frontendFile = $fileStatus["前端API配置"].path
    $result = Invoke-SSHCommand -Command "grep -n 'timeout:' $frontendFile | head -5"
    
    if ($result -match "timeout: 10000") {
        Write-Host "⚠ 发现问题: 前端超时设置为10秒（太短）" -ForegroundColor Yellow
        Write-Host "  建议: 改为60秒" -ForegroundColor Yellow
        $needsFix = $true
    } elseif ($result -match "timeout: 60000") {
        Write-Host "✓ 前端超时配置正确（60秒）" -ForegroundColor Green
        $needsFix = $false
    }
}

# 6. 检查Docker服务状态
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "6. 检查Docker服务状态" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

Invoke-SSHCommand -Command "cd $projectDir && docker-compose -f docker-compose.prod.yml ps"

# 7. 测试API响应时间
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "7. 测试API响应时间" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

Write-Host "`n测试: 图谱API (小数据量)"
try {
    $start = Get-Date
    $response = Invoke-WebRequest -Uri "http://47.108.152.16/api/kg/graph?limit=100" -TimeoutSec 30
    $elapsed = (Get-Date) - $start
    
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        $nodes = $data.data.sampleNodes.Count
        Write-Host "  ✓ 成功 - 响应时间: $($elapsed.TotalSeconds.ToString('F2'))秒, 节点数: $nodes" -ForegroundColor Green
    }
} catch {
    Write-Host "  ✗ 失败: $_" -ForegroundColor Red
}

# 8. 诊断总结
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "诊断报告总结" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

Write-Host "`n项目目录: $projectDir"
Write-Host "`n文件检查:"
foreach ($name in $fileStatus.Keys) {
    $status = if ($fileStatus[$name].exists) { "✓" } else { "✗" }
    $color = if ($fileStatus[$name].exists) { "Green" } else { "Red" }
    Write-Host "  $status $name" -ForegroundColor $color
}

# 9. 询问是否执行修复
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "是否执行自动修复？" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

Write-Host "`n修复内容:"
Write-Host "  1. 将前端超时从10秒改为60秒"
Write-Host "  2. 修复后端缓存逻辑bug"
Write-Host "  3. 重启相关服务"

$confirm = Read-Host "`n是否继续执行修复？(y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "`n开始执行修复..." -ForegroundColor Green
    
    # 修复1: 修改前端超时配置
    Write-Host "`n修复1: 修改前端超时配置" -ForegroundColor Yellow
    if ($fileStatus["前端API配置"].exists) {
        $frontendFile = $fileStatus["前端API配置"].path
        Invoke-SSHCommand -Command @"
cd $projectDir
cp $frontendFile ${frontendFile}.backup.`$(date +%Y%m%d_%H%M%S)
sed -i 's/timeout: 10000/timeout: 60000/g' $frontendFile
echo '✓ 前端超时配置已修改'
grep -n 'timeout:' $frontendFile | head -3
"@
    }
    
    # 修复2: 修改后端缓存逻辑
    Write-Host "`n修复2: 修改后端缓存逻辑" -ForegroundColor Yellow
    if ($fileStatus["后端API"].exists) {
        $backendFile = $fileStatus["后端API"].path
        Invoke-SSHCommand -Command @"
cd $projectDir
cp $backendFile ${backendFile}.backup.`$(date +%Y%m%d_%H%M%S)
python3 << 'ENDPYTHON'
try:
    with open('$backendFile', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    modified = False
    
    for i in range(len(lines)):
        if 'return {' in lines[i] and i < len(lines) - 10:
            future_lines = '\n'.join(lines[i:min(i+30, len(lines))])
            if '# 缓存结果' in future_lines and 'QueryCache.set_graph_data' in future_lines:
                lines[i] = lines[i].replace('return {', 'result = {')
                modified = True
                print(f'✓ 在第 {i+1} 行修复了缓存逻辑')
                break
    
    if modified:
        with open('$backendFile', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print('✓ 后端缓存逻辑已修复')
    else:
        print('缓存逻辑可能已经正确')
except Exception as e:
    print(f'✗ 修复失败: {e}')
ENDPYTHON
"@
    }
    
    # 修复3: 重启服务
    Write-Host "`n修复3: 重启服务" -ForegroundColor Yellow
    Invoke-SSHCommand -Command @"
cd $projectDir
echo '重启前端服务...'
docker-compose -f docker-compose.prod.yml restart web
echo '重启API服务...'
docker-compose -f docker-compose.prod.yml restart api
echo '等待服务启动...'
sleep 10
echo '检查服务状态:'
docker-compose -f docker-compose.prod.yml ps
"@
    
    Write-Host "`n================================================================================" -ForegroundColor Green
    Write-Host "修复完成！" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    
    Write-Host "`n请在浏览器中测试: http://47.108.152.16/"
    
} else {
    Write-Host "`n已取消修复操作" -ForegroundColor Yellow
}

