$ErrorActionPreference = "Stop"

$SERVER = "root@47.108.152.16"
$PASSWORD = "Zxylsy.99"
$REMOTE_DIR = "/opt/knowledge-graph"

Write-Host "Deploying graph visualization improvements..." -ForegroundColor Cyan

Write-Host "Uploading frontend file..." -ForegroundColor Yellow
& sshpass -p $PASSWORD scp apps/web/src/views/GraphVisualization.vue "${SERVER}:${REMOTE_DIR}/apps/web/src/views/"

Write-Host "Uploading backend router..." -ForegroundColor Yellow
& sshpass -p $PASSWORD scp services/api/routers/kg_router.py "${SERVER}:${REMOTE_DIR}/services/api/routers/"

Write-Host "Uploading Neo4j client..." -ForegroundColor Yellow
& sshpass -p $PASSWORD scp services/api/database/neo4j_client.py "${SERVER}:${REMOTE_DIR}/services/api/database/"

Write-Host "Restarting services..." -ForegroundColor Yellow
& sshpass -p $PASSWORD ssh $SERVER "systemctl restart kg-frontend && systemctl restart kg-api && sleep 5 && systemctl status kg-frontend --no-pager | head -10 && systemctl status kg-api --no-pager | head -10"

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "URL: http://47.108.152.16/" -ForegroundColor Cyan

