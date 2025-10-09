# SSH Helper Script with Password
param(
    [string]$Command
)

$password = "Zxylsy.99"
$username = "root"
$server = "47.108.152.16"

# 使用plink (PuTTY的命令行工具) 或者创建临时密钥
# 由于Windows限制，我们使用expect-like的方式

# 创建临时脚本
$tempScript = @"
`$password = ConvertTo-SecureString '$password' -AsPlainText -Force
`$cred = New-Object System.Management.Automation.PSCredential ('$username', `$password)
`$session = New-SSHSession -ComputerName $server -Credential `$cred
Invoke-SSHCommand -SessionId `$session.SessionId -Command '$Command'
Remove-SSHSession -SessionId `$session.SessionId
"@

Write-Output $tempScript

