# PowerShell脚本 - 部署词典和图谱更新到服务器
# 服务器: 47.108.152.16

$SERVER = "root@47.108.152.16"
$REMOTE_PATH = "/opt/knowledge-graph"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "📦 开始部署词典和图谱更新到服务器" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. 备份服务器现有数据
Write-Host ""
Write-Host "1️⃣ 备份服务器现有数据..." -ForegroundColor Yellow
ssh $SERVER "cd $REMOTE_PATH && mkdir -p backups && cp api/data/dictionary.json backups/dictionary_backup_`$(date +%Y%m%d_%H%M%S).json && echo '✅ 备份完成'"

# 2. 上传更新后的词典文件
Write-Host ""
Write-Host "2️⃣ 上传更新后的词典文件..." -ForegroundColor Yellow
scp api/data/dictionary.json "${SERVER}:${REMOTE_PATH}/api/data/"
Write-Host "✅ 词典文件上传完成" -ForegroundColor Green

# 3. 上传同步脚本
Write-Host ""
Write-Host "3️⃣ 上传Neo4j同步脚本..." -ForegroundColor Yellow
scp sync_to_neo4j.py "${SERVER}:${REMOTE_PATH}/"
Write-Host "✅ 同步脚本上传完成" -ForegroundColor Green

# 4. 在服务器上同步到Neo4j
Write-Host ""
Write-Host "4️⃣ 在服务器上同步到Neo4j图谱..." -ForegroundColor Yellow
ssh $SERVER "cd $REMOTE_PATH && echo '开始同步到Neo4j...' && python3 sync_to_neo4j.py"
Write-Host "✅ Neo4j同步完成" -ForegroundColor Green

# 5. 重启后端API服务
Write-Host ""
Write-Host "5️⃣ 重启后端API服务..." -ForegroundColor Yellow
ssh $SERVER "systemctl restart kg-api && sleep 3 && systemctl status kg-api | head -10"

# 6. 验证部署
Write-Host ""
Write-Host "6️⃣ 验证部署..." -ForegroundColor Yellow
Write-Host "检查API状态..." -ForegroundColor Cyan
$response = Invoke-RestMethod -Uri "http://47.108.152.16/kg/stats" -Method Get
$response | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 验证步骤:" -ForegroundColor Yellow
Write-Host "  1. 访问: http://47.108.152.16"
Write-Host "  2. 检查词典数量是否为 1326 条"
Write-Host "  3. 检查图谱节点数量"
Write-Host "  4. 测试搜索功能"
Write-Host ""
Write-Host "📝 回滚方法（如有问题）:" -ForegroundColor Yellow
Write-Host "  ssh root@47.108.152.16"
Write-Host "  cd /opt/knowledge-graph"
Write-Host "  cp backups/dictionary_backup_*.json api/data/dictionary.json"
Write-Host "  systemctl restart kg-api"
Write-Host ""
