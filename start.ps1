# RAG System 一键启动脚本
# Usage: 双击 start.bat 或运行 .\start.ps1
# 所有服务日志集中在一个窗口中显示

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

# 日志文件路径
$backendLog = Join-Path $root "backend.log"
$frontendLog = Join-Path $root "frontend.log"

# 统一日志输出
function Write-Log {
    param([string]$Service, [string]$Message, [ConsoleColor]$Color = "White")
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] " -NoNewline -ForegroundColor DarkGray
    Write-Host "[$Service] " -NoNewline -ForegroundColor $Color
    Write-Host $Message
}

function Show-Banner {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "        RAG System 一键启动" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Check-Dependencies {
    # 检查 .env
    if (-not (Test-Path "$backend\.env")) {
        if (Test-Path "$backend\.env.example") {
            Write-Log "系统" "未找到 .env，正在从 .env.example 创建..." -Color Yellow
            Copy-Item "$backend\.env.example" "$backend\.env"
            Write-Log "系统" "请编辑 backend\.env 配置 API Key，然后重新运行此脚本。" -Color Red
            Read-Host "按 Enter 退出"
            exit 1
        }
    }

    # 检查后端依赖
    if (-not (Test-Path "$backend\requirements.txt")) {
        Write-Log "系统" "未找到 backend/requirements.txt" -Color Red
        exit 1
    }

    # 检查前端依赖
    if (-not (Test-Path "$frontend\node_modules")) {
        Write-Log "前端" "首次运行，正在安装前端依赖..." -Color Yellow
        Push-Location $frontend
        npm install
        Pop-Location
    }
}

function Seed-Knowledge {
    $seedScript = Join-Path $backend "seed_knowledge.py"
    if (-not (Test-Path $seedScript)) {
        return
    }

    # 检查知识库是否已有数据
    $dbPath = Join-Path $backend "data\sqlite\knowledge.db"
    $needSeed = $false

    if (-not (Test-Path $dbPath)) {
        $needSeed = $true
    } else {
        # 检查数据库中是否有知识条目
        $countResult = & {
            Set-Location $backend
            python -c "from app.db.sqlite import SessionLocal; from app.models.knowledge import KnowledgeItem; db=SessionLocal(); print(db.query(KnowledgeItem).count()); db.close()" 2>$null
        }
        if ($countResult -eq "0" -or -not $countResult) {
            $needSeed = $true
        }
    }

    if ($needSeed) {
        Write-Log "知识库" "首次启动，正在导入编程知识..." -Color Magenta
        Set-Location $backend
        python seed_knowledge.py
        Set-Location $root
        Write-Log "知识库" "编程知识导入完成" -Color Green
    } else {
        Write-Log "知识库" "已有 $countResult 条知识，跳过导入" -Color DarkGray
    }
}

function Start-Services {
    Write-Host ""
    Write-Host "------------------------------------------" -ForegroundColor DarkGray
    Write-Host "  启动服务 (日志将显示在本窗口)" -ForegroundColor DarkGray
    Write-Host "------------------------------------------" -ForegroundColor DarkGray
    Write-Host ""

    # 清空旧日志（截断而非删除，避免文件锁定问题）
    if (Test-Path $backendLog) { Clear-Content $backendLog -ErrorAction SilentlyContinue }
    if (Test-Path $frontendLog) { Clear-Content $frontendLog -ErrorAction SilentlyContinue }

    # 创建日志文件
    New-Item -ItemType File -Path $backendLog -Force -ErrorAction SilentlyContinue | Out-Null
    New-Item -ItemType File -Path $frontendLog -Force -ErrorAction SilentlyContinue | Out-Null

    # 启动后端 - PowerShell 原生重定向 *> (stdout + stderr -> 文件)
    Write-Log "后端" "启动 FastAPI (端口 8000)..." -Color Green
    $script:backendProc = Start-Process -FilePath "powershell" -ArgumentList @(
        "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
        "Set-Location '$backend'; python -m uvicorn app.main:app --reload --port 8000 *> '$backendLog'"
    ) -PassThru -WindowStyle Hidden

    # 启动前端
    Write-Log "前端" "启动 Next.js (端口 3000)..." -Color Blue
    $script:frontendProc = Start-Process -FilePath "powershell" -ArgumentList @(
        "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
        "Set-Location '$frontend'; npm run dev *> '$frontendLog'"
    ) -PassThru -WindowStyle Hidden

    Start-Sleep -Seconds 2
}

function Wait-ForServices {
    $maxWait = 30
    $waited = 0

    Write-Host ""
    Write-Log "系统" "等待服务就绪..." -Color Cyan

    while ($waited -lt $maxWait) {
        $backendReady = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
        $frontendReady = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue

        if ($backendReady.TcpTestSucceeded -and $frontendReady.TcpTestSucceeded) {
            return $true
        }

        Start-Sleep -Seconds 1
        $waited++
    }

    return $false
}

function Show-Status {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "          服务状态" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan

    $backendUp = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    $frontendUp = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue

    if ($backendUp.TcpTestSucceeded) {
        Write-Log "后端" "运行中  http://localhost:8000" -Color Green
    } else {
        Write-Log "后端" "未就绪 (请稍候...)" -Color Yellow
    }

    if ($frontendUp.TcpTestSucceeded) {
        Write-Log "前端" "运行中  http://localhost:3000" -Color Green
    } else {
        Write-Log "前端" "未就绪 (请稍候...)" -Color Yellow
    }

    Write-Host ""
    Write-Host "------------------------------------------" -ForegroundColor DarkGray
    Write-Host "  访问地址:" -ForegroundColor White
    Write-Host "    前端:      http://localhost:3000" -ForegroundColor White
    Write-Host "    后端:      http://localhost:8000" -ForegroundColor White
    Write-Host "    API 文档:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host "------------------------------------------" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  日志文件:" -ForegroundColor DarkGray
    Write-Host "    后端日志:  $backendLog" -ForegroundColor DarkGray
    Write-Host "    前端日志:  $frontendLog" -ForegroundColor DarkGray
    Write-Host "------------------------------------------" -ForegroundColor DarkGray
    Write-Host ""
}

function Test-PortOpen {
    param([int]$Port)
    try {
        $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Watch-Logs {
    Write-Log "系统" "实时日志 (按 Ctrl+C 退出监控)" -Color Cyan
    Write-Host ""

    $backendPos = 0
    $frontendPos = 0
    $backendWasDown = $false
    $frontendWasDown = $false

    try {
        while ($true) {
            # 显示后端新日志
            if (Test-Path $backendLog) {
                $backendContent = Get-Content $backendLog -ErrorAction SilentlyContinue
                if ($backendContent -and $backendContent.Count -gt $backendPos) {
                    $newLines = $backendContent[$backendPos..($backendContent.Count - 1)]
                    foreach ($line in $newLines) {
                        if ($line.Trim()) {
                            $ts = Get-Date -Format "HH:mm:ss"
                            Write-Host "[$ts] " -NoNewline -ForegroundColor DarkGray
                            Write-Host "[后端] " -NoNewline -ForegroundColor Green
                            Write-Host $line
                        }
                    }
                    $backendPos = $backendContent.Count
                }
            }

            # 显示前端新日志
            if (Test-Path $frontendLog) {
                $frontendContent = Get-Content $frontendLog -ErrorAction SilentlyContinue
                if ($frontendContent -and $frontendContent.Count -gt $frontendPos) {
                    $newLines = $frontendContent[$frontendPos..($frontendContent.Count - 1)]
                    foreach ($line in $newLines) {
                        if ($line.Trim()) {
                            $ts = Get-Date -Format "HH:mm:ss"
                            Write-Host "[$ts] " -NoNewline -ForegroundColor DarkGray
                            Write-Host "[前端] " -NoNewline -ForegroundColor Blue
                            Write-Host $line
                        }
                    }
                    $frontendPos = $frontendContent.Count
                }
            }

            # 通过端口检测服务是否存活
            $backendUp = Test-PortOpen -Port 8000
            $frontendUp = Test-PortOpen -Port 3000

            if (-not $backendUp) {
                if (-not $backendWasDown) {
                    Write-Log "后端" "服务已停止!" -Color Red
                    $backendWasDown = $true
                }
            } else {
                $backendWasDown = $false
            }

            if (-not $frontendUp) {
                if (-not $frontendWasDown) {
                    Write-Log "前端" "服务已停止!" -Color Red
                    $frontendWasDown = $true
                }
            } else {
                $frontendWasDown = $false
            }

            Start-Sleep -Seconds 2
        }
    } finally {
        Stop-Services
    }
}

function Stop-Services {
    Write-Host ""
    Write-Log "系统" "正在关闭所有服务..." -Color Yellow

    # 通过命令行匹配杀掉实际的子进程
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*uvicorn*" } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Log "后端" "已关闭 (PID: $($_.ProcessId))" -Color DarkGray
        }

    Get-CimInstance Win32_Process -Filter "Name='node.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*next*" } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Log "前端" "已关闭 (PID: $($_.ProcessId))" -Color DarkGray
        }

    # 清理日志文件
    Clear-Content $backendLog -ErrorAction SilentlyContinue
    Clear-Content $frontendLog -ErrorAction SilentlyContinue

    Write-Log "系统" "所有服务已关闭" -Color Green
    Start-Sleep -Seconds 2
}

# ============ 主流程 ============
Show-Banner
Check-Dependencies
Seed-Knowledge
Start-Services

$allReady = Wait-ForServices
if ($allReady) {
    Write-Log "系统" "所有服务已就绪!" -Color Green
} else {
    Write-Log "系统" "部分服务启动超时，请检查日志" -Color Yellow
}

Show-Status
Watch-Logs
