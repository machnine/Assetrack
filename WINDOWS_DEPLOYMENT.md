# Windows Deployment Guide

This guide explains how to deploy Assetrack as a Windows service.

## Prerequisites

1. **Windows Server** or Windows 10/11
2. **Python 3.12+** installed
3. **uv** package manager ([install guide](https://docs.astral.sh/uv/))
4. **WinSW** (Windows Service Wrapper) - [download](https://github.com/winsw/winsw/releases)
5. **Administrator privileges**

## Installation Steps

### 1. Install uv (if not already installed)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Download WinSW

Download the latest `WinSW.exe` from [GitHub releases](https://github.com/winsw/winsw/releases) and place it at:
```
C:\Service\winsw\WinSW.exe
```

### 3. Clone the Repository

```powershell
cd C:\Service
git clone <your-repo-url> assetrack
cd assetrack
```

### 4. Install Dependencies

```powershell
uv sync
```

### 5. Configure Environment

Create `.env` file (copy from `.env.example`):

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_SETTINGS_MODULE=core.settings.production

# Security Settings
ALLOWED_HOSTS=10.134.108.170,yourdomain.com
CSRF_TRUSTED_ORIGINS=http://10.134.108.170,http://yourdomain.com

# Server Configuration
WSGI_HOST=0.0.0.0
WSGI_PORT=7111
WSGI_THREADS=4
```

**Important:** Generate a secure `SECRET_KEY`:
```powershell
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Prepare Database

```powershell
# Run migrations
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Create superuser (optional)
uv run python manage.py createsuperuser
```

### 7. Open Firewall Port

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Assetrack Django" -Direction Inbound -Protocol TCP -LocalPort 7111 -Action Allow
```

### 8. Install as Windows Service

```powershell
# Run as Administrator
.\deploy_service.ps1 install
```

This will:
- Copy WinSW to the service directory
- Install the service
- Start the service automatically

## Service Management

### Check Service Status
```powershell
.\deploy_service.ps1 status
```

### Start Service
```powershell
.\deploy_service.ps1 start
```

### Stop Service
```powershell
.\deploy_service.ps1 stop
```

### Restart Service
```powershell
.\deploy_service.ps1 restart
```

### View Logs
```powershell
.\deploy_service.ps1 logs
```

Log files are located at:
- `C:\Service\assetrack\assetrack-service.out.log` - Standard output
- `C:\Service\assetrack\assetrack-service.err.log` - Error output

### Uninstall Service
```powershell
.\deploy_service.ps1 uninstall
```

## Updating the Application

```powershell
# Stop the service
.\deploy_service.ps1 stop

# Pull latest changes
git pull

# Install/update dependencies
uv sync

# Run migrations if needed
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Start the service
.\deploy_service.ps1 start
```

## Accessing the Application

Once the service is running, access the application at:
```
http://your-server-ip:7111/
```

Example:
```
http://10.134.108.170:7111/
```

## Troubleshooting

### Service won't start
1. Check logs: `.\deploy_service.ps1 logs`
2. Verify `.env` file exists and has correct settings
3. Check port 7111 is not already in use: `netstat -ano | findstr :7111`
4. Verify uv is in PATH: `uv --version`

### Can't access from other PCs
1. Check Windows Firewall rule exists
2. Verify `WSGI_HOST=0.0.0.0` in `.env`
3. Check network connectivity: `Test-NetConnection -ComputerName <server-ip> -Port 7111`

### Static/Media files not loading
1. Run `uv run python manage.py collectstatic --noinput`
2. Verify `staticfiles` and `media` directories exist
3. Check file permissions

### Database errors
1. Ensure `data` directory exists
2. Run migrations: `uv run python manage.py migrate`
3. Check SQLite file permissions

## Service Configuration

The service configuration is in `assetrack-service.xml`. You can customize:

- **Service name and description**
- **Environment variables**
- **Service account** (default: LocalSystem)
- **Restart behavior** on failure
- **Log rotation** settings

After modifying `assetrack-service.xml`:
1. Uninstall service: `.\deploy_service.ps1 uninstall`
2. Reinstall service: `.\deploy_service.ps1 install`

## Architecture

```
Browser → Django + Waitress (port 7111)
            ├─ WhiteNoise → Static files (/static/*)
            └─ Django views → Media files (/media/*)
```

- **Static files** (CSS, JS): Served by WhiteNoise middleware
- **Media files** (uploads): Served by Django
- **Database**: SQLite (located in `data/assetrack.sqlite3`)
- **Logs**: Rolling log files (10MB per file, keeps 8 files)

## Security Considerations

1. **Change SECRET_KEY** - Never use the default in production
2. **Set ALLOWED_HOSTS** - Only allow your specific domain/IP
3. **HTTPS** - Consider adding a reverse proxy (Caddy/Nginx) for HTTPS
4. **Firewall** - Only open port 7111 to trusted networks
5. **Backups** - Regularly backup `data/` and `media/` directories
6. **Updates** - Keep dependencies updated: `uv sync --upgrade`

## Docker vs Windows Deployment

| Feature | Docker (Linux) | Windows Service |
|---------|----------------|-----------------|
| Web Server | Gunicorn + Nginx | Waitress |
| Static Files | Nginx | WhiteNoise |
| Media Files | Nginx | Django |
| Service Management | Docker Compose | WinSW |
| Auto-start | Yes | Yes |
| Updates | Rebuild image | Git pull + restart |

The codebase is identical - platform differences are handled automatically!
