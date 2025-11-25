# Assetrack Windows Service Deployment Script
# Manages the Assetrack Django application as a Windows service using WinSW

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('install', 'uninstall', 'start', 'stop', 'restart', 'status', 'logs')]
    [string]$Action = 'status',

    [Parameter(Mandatory=$false)]
    [string]$ServicePath = "C:\Service\assetrack",

    [Parameter(Mandatory=$false)]
    [string]$WinSWPath = "C:\Service\winsw\WinSW.exe"
)

$ErrorActionPreference = "Stop"

# Service configuration
$ServiceName = "assetrack"
$ServiceDisplayName = "Assetrack"
$ServiceXML = Join-Path $ServicePath "assetrack-service.xml"
$ServiceExe = Join-Path $ServicePath "assetrack-service.exe"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) {
    Write-ColorOutput Green "✓ $message"
}

function Write-Info($message) {
    Write-ColorOutput Cyan "ℹ $message"
}

function Write-Warning($message) {
    Write-ColorOutput Yellow "⚠ $message"
}

function Write-Error($message) {
    Write-ColorOutput Red "✗ $message"
}

# Check if running as administrator
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."

    # Check administrator
    if (-not (Test-Administrator)) {
        Write-Error "This script must be run as Administrator"
        exit 1
    }

    # Check service path exists
    if (-not (Test-Path $ServicePath)) {
        Write-Error "Service path not found: $ServicePath"
        exit 1
    }

    # Check WinSW exists
    if (-not (Test-Path $WinSWPath)) {
        Write-Error "WinSW not found at: $WinSWPath"
        Write-Info "Download from: https://github.com/winsw/winsw/releases"
        exit 1
    }

    # Check uv is installed
    try {
        $uvVersion = & uv --version 2>&1
        Write-Success "uv is installed: $uvVersion"
    } catch {
        Write-Error "uv is not installed or not in PATH"
        Write-Info "Install from: https://docs.astral.sh/uv/"
        exit 1
    }

    # Check .env file exists
    $envFile = Join-Path $ServicePath ".env"
    if (-not (Test-Path $envFile)) {
        Write-Warning ".env file not found at: $envFile"
        Write-Info "Create .env file with required settings (see .env.example)"
    } else {
        Write-Success ".env file found"
    }

    # Check XML config exists
    if (-not (Test-Path $ServiceXML)) {
        Write-Error "Service XML not found: $ServiceXML"
        exit 1
    }

    Write-Success "Prerequisites check passed"
}

# Install service
function Install-Service {
    Write-Info "Installing $ServiceDisplayName service..."

    Test-Prerequisites

    # Copy WinSW to service directory with service name
    Copy-Item $WinSWPath $ServiceExe -Force
    Write-Success "WinSW copied to $ServiceExe"

    # Install service
    try {
        & $ServiceExe install
        Write-Success "$ServiceDisplayName service installed"

        # Start service
        Start-Sleep -Seconds 2
        & $ServiceExe start
        Write-Success "$ServiceDisplayName service started"

        Write-Info "Service logs: $ServicePath\assetrack-service.out.log"
        Write-Info "Error logs: $ServicePath\assetrack-service.err.log"
    } catch {
        Write-Error "Failed to install service: $_"
        exit 1
    }
}

# Uninstall service
function Uninstall-Service {
    Write-Info "Uninstalling $ServiceDisplayName service..."

    if (-not (Test-Path $ServiceExe)) {
        Write-Warning "Service executable not found, service may not be installed"
        return
    }

    try {
        # Stop service first
        & $ServiceExe stop 2>&1 | Out-Null
        Start-Sleep -Seconds 2

        # Uninstall
        & $ServiceExe uninstall
        Write-Success "$ServiceDisplayName service uninstalled"

        # Remove service executable
        Remove-Item $ServiceExe -Force
        Write-Success "Service executable removed"
    } catch {
        Write-Error "Failed to uninstall service: $_"
        exit 1
    }
}

# Start service
function Start-Service {
    Write-Info "Starting $ServiceDisplayName service..."

    if (-not (Test-Path $ServiceExe)) {
        Write-Error "Service not installed. Run: .\deploy_service.ps1 install"
        exit 1
    }

    try {
        & $ServiceExe start
        Write-Success "$ServiceDisplayName service started"
    } catch {
        Write-Error "Failed to start service: $_"
        exit 1
    }
}

# Stop service
function Stop-Service {
    Write-Info "Stopping $ServiceDisplayName service..."

    if (-not (Test-Path $ServiceExe)) {
        Write-Error "Service not installed"
        exit 1
    }

    try {
        & $ServiceExe stop
        Write-Success "$ServiceDisplayName service stopped"
    } catch {
        Write-Error "Failed to stop service: $_"
        exit 1
    }
}

# Restart service
function Restart-Service {
    Write-Info "Restarting $ServiceDisplayName service..."
    Stop-Service
    Start-Sleep -Seconds 2
    Start-Service
}

# Get service status
function Get-ServiceStatus {
    Write-Info "Checking $ServiceDisplayName service status..."

    if (-not (Test-Path $ServiceExe)) {
        Write-Warning "Service executable not found - service not installed"
        return
    }

    try {
        & $ServiceExe status
    } catch {
        Write-Error "Failed to get service status: $_"
        exit 1
    }
}

# Show logs
function Show-Logs {
    Write-Info "Showing recent logs for $ServiceDisplayName..."

    $outLog = Join-Path $ServicePath "assetrack-service.out.log"
    $errLog = Join-Path $ServicePath "assetrack-service.err.log"

    if (Test-Path $outLog) {
        Write-Info "`n=== Standard Output Log (last 20 lines) ==="
        Get-Content $outLog -Tail 20
    } else {
        Write-Warning "Output log not found: $outLog"
    }

    if (Test-Path $errLog) {
        $errContent = Get-Content $errLog -Tail 20
        if ($errContent) {
            Write-Info "`n=== Error Log (last 20 lines) ==="
            $errContent
        }
    } else {
        Write-Warning "Error log not found: $errLog"
    }
}

# Main execution
Write-Info "Assetrack Service Deployment Script"
Write-Info "Action: $Action"
Write-Info ""

switch ($Action) {
    'install'   { Install-Service }
    'uninstall' { Uninstall-Service }
    'start'     { Start-Service }
    'stop'      { Stop-Service }
    'restart'   { Restart-Service }
    'status'    { Get-ServiceStatus }
    'logs'      { Show-Logs }
}

Write-Info "`nDone."
