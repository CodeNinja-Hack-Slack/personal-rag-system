# RAG System 一键启动脚本
# Usage: 双击 start.bat 或运行 .\start.ps1

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

Write-Host "=== RAG System 启动中 ===" -ForegroundColor Cyan

# 检查 .env
if (-not (Test-Path "$backend\.env")) {
    if (Test-Path "$backend\.env.example") {
        Write-Host "未找到 .env，正在从 .env.example 创建..." -ForegroundColor Yellow
        Copy-Item "$backend\.env.example" "$backend\.env"
        Write-Host "请编辑 backend\.env 配置 API Key，然后重新运行此脚本。" -ForegroundColor Red
        Write-Host ""
        Write-Host "按任意键退出..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# 检查依赖
if (-not (Test-Path "$backend\.venv")) {
    Write-Host "首次运行，正在安装后端依赖..." -ForegroundColor Yellow
    Push-Location $backend
    pip install -r requirements.txt
    Pop-Location
}

if (-not (Test-Path "$frontend\node_modules")) {
    Write-Host "首次运行，正在安装前端依赖..." -ForegroundColor Yellow
    Push-Location $frontend
    npm install
    Pop-Location
}

# 启动后端
Write-Host "启动后端 (FastAPI)..." -ForegroundColor Green
$backendProc = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$backend'; uvicorn app.main:app --reload --port 8000" -PassThru

# 启动前端
Write-Host "启动前端 (Next.js)..." -ForegroundColor Green
$frontendProc = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$frontend'; npm run dev" -PassThru

Write-Host ""
Write-Host "=== 启动完成 ===" -ForegroundColor Cyan
Write-Host "后端: http://localhost:8000" -ForegroundColor White
Write-Host "前端: http://localhost:3000" -ForegroundColor White
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "按任意键关闭所有服务..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 关闭进程
Write-Host "正在关闭服务..." -ForegroundColor Yellow
Stop-Process -Id $backendProc.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontendProc.Id -Force -ErrorAction SilentlyContinue
Write-Host "已关闭。" -ForegroundColor Green
Start-Sleep -Seconds 2
