# SeedBox Stack Update - Plex, Tautulli, uTorrent & ruTorrent

## Overview

The SeedBox Control Panel has been updated to include complete management and monitoring support for:
- **Plex Media Server** - Media streaming and library management
- **Tautulli** - Plex activity monitoring and analytics
- **uTorrent** - Torrent client management
- **ruTorrent** - Web-based rtorrent client management

## New Features

### Backend Services

#### 1. Plex Service Wrapper (`backend/plex_service.py`)
- Server status and information retrieval
- Library management (list all libraries, get stats)
- Active streaming session monitoring
- Recent stream history
- Database optimization
- Library scanning triggers
- Server restart capabilities

#### 2. Tautulli Service Wrapper (`backend/tautulli_service.py`)
- Server status and version info
- Current activity monitoring (streams, bandwidth)
- Statistics collection (plays, time watched, users)
- User management and activity tracking
- Library-level analytics
- Playback history retrieval
- Service restart capabilities

#### 3. uTorrent Service Wrapper (`backend/utorrent_service.py`)
- Server connectivity and status
- Torrent listing and management
- Start/stop/pause/resume torrent operations
- Remove torrents (with optional file deletion)
- Add torrents from URL
- Bandwidth statistics
- Torrent statistics (active, seeding, total size)

#### 4. ruTorrent Service Wrapper (`backend/rutorrent_service.py`)
- Server connectivity and status
- Torrent listing and management
- Start/stop/pause/resume torrent operations
- Remove torrents (with optional file deletion)
- Bandwidth statistics
- Torrent statistics and ratio tracking
- rtorrent daemon restart

### API Endpoints

#### Plex API Routes (`/api/plex`)
```
GET    /health                      - Check Plex server connectivity
GET    /status                      - Get server status and info
GET    /libraries                   - List all media libraries
GET    /libraries/<key>/stats       - Get library statistics
GET    /sessions                    - Get active streaming sessions
GET    /streams                     - Get recent stream history
POST   /restart                     - Restart Plex server
POST   /optimize                    - Optimize Plex database
POST   /libraries/<key>/scan        - Trigger library scan
```

#### Tautulli API Routes (`/api/tautulli`)
```
GET    /health                      - Check Tautulli connectivity
GET    /status                      - Get server status
GET    /activity                    - Get current Plex activity
GET    /stats                       - Get statistics
GET    /users                       - List Plex users
GET    /libraries                   - Get library stats
GET    /history                     - Get playback history
GET    /server-info                 - Get Plex server info
POST   /restart                     - Restart Tautulli
```

#### uTorrent API Routes (`/api/utorrent`)
```
GET    /health                      - Check uTorrent connectivity
GET    /status                      - Get server status
GET    /torrents                    - List all torrents
GET    /stats                       - Get torrent statistics
GET    /bandwidth                   - Get bandwidth stats
POST   /torrents/<hash>/start       - Start torrent
POST   /torrents/<hash>/stop        - Stop torrent
POST   /torrents/<hash>/pause       - Pause torrent
POST   /torrents/<hash>/resume      - Resume torrent
POST   /torrents/<hash>/remove      - Remove torrent
POST   /torrents/add-url            - Add torrent from URL
```

#### ruTorrent API Routes (`/api/rutorrent`)
```
GET    /health                      - Check ruTorrent connectivity
GET    /status                      - Get server status
GET    /torrents                    - List all torrents
GET    /stats                       - Get torrent statistics
GET    /bandwidth                   - Get bandwidth stats
POST   /torrents/<hash>/start       - Start torrent
POST   /torrents/<hash>/stop        - Stop torrent
POST   /torrents/<hash>/pause       - Pause torrent
POST   /torrents/<hash>/resume      - Resume torrent
POST   /torrents/<hash>/remove      - Remove torrent
POST   /restart                     - Restart rtorrent daemon
```

### Frontend Updates

#### New Navigation Tabs
1. **Torrents Tab** - Combined uTorrent and ruTorrent management
2. **Plex Tab** - Plex server, Tautulli monitoring, and user activity

#### Torrents Tab Features
- uTorrent statistics (active, seeding, total size, bandwidth)
- ruTorrent statistics (total torrents, size, ratio)
- Torrent list from both clients
- Individual torrent control (start/stop/pause/resume)
- Service restart buttons

#### Plex Tab Features
- Plex server status and version information
- Tautulli server status and Plex version
- Active streaming sessions display
- Media libraries with scan triggers
- User list with play statistics
- Recent stream history

### Configuration Updates

#### New Environment Variables
```bash
# Plex Media Server
PLEX_URL=http://localhost:32400
PLEX_TOKEN=your_plex_token

# Tautulli (Plex Monitoring)
TAUTULLI_URL=http://localhost:8181
TAUTULLI_API_KEY=your_tautulli_api_key

# ruTorrent (rtorrent web interface)
RUTORRENT_URL=http://localhost:8081
RUTORRENT_USERNAME=your_username
RUTORRENT_PASSWORD=your_password
```

#### Updated Configuration File
- `backend/config.py` updated with all new service URLs and API keys
- Environment-based configuration for all services

## Installation & Setup

### 1. Update Environment File
```bash
cp .env.example .env
```

Add your service URLs and API keys:
```bash
# Plex
PLEX_URL=http://your-plex-server:32400
PLEX_TOKEN=your_plex_token_here

# Tautulli
TAUTULLI_URL=http://your-tautulli-server:8181
TAUTULLI_API_KEY=your_tautulli_api_key

# uTorrent
UTORRENT_URL=http://your-utorrent-server:8080
UTORRENT_USERNAME=admin
UTORRENT_PASSWORD=your_password

# ruTorrent
RUTORRENT_URL=http://your-rutorrent-server:8081
RUTORRENT_USERNAME=your_username
RUTORRENT_PASSWORD=your_password
```

### 2. Install/Update Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Restart Application
```bash
python run.py
```

## Operation Guide

### Accessing New Features

#### Torrent Management
1. Navigate to **Torrents** tab
2. View statistics from both uTorrent and ruTorrent
3. Manage individual torrents:
   - Click **Start** to resume downloading
   - Click **Stop** to halt torrent
   - Click **Pause** to temporarily stop
   - Click **Resume** to continue paused torrent
4. Click **Restart** button to restart the service

#### Plex Media Management
1. Navigate to **Plex** tab
2. View server status and active sessions
3. Monitor user activity in Plex
4. Trigger library scans by clicking **Scan** on any library
5. View recent streaming history
6. Monitor Tautulli statistics

### API Examples

#### Get Plex Libraries
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/plex/libraries
```

#### Start uTorrent Torrent
```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:5000/api/utorrent/torrents/HASH/start
```

#### Get Tautulli Activity
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/tautulli/activity
```

#### Get ruTorrent Statistics
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/rutorrent/stats
```

## Service Management

### Docker Control
For uTorrent and ruTorrent containers, use the **Applications** tab to:
- Start/stop the service
- Restart the service
- View logs
- Monitor resource usage

### Direct API Control
All services support restart capabilities through their API endpoints:
```bash
# Restart Plex
POST /api/plex/restart

# Restart Tautulli
POST /api/tautulli/restart

# Restart ruTorrent
POST /api/rutorrent/restart
```

## Architecture

### Service Wrappers
Each service has a dedicated wrapper class that handles:
- Connection management and error handling
- API request formatting
- Response parsing and transformation
- Health checks and status reporting

### API Blueprints
Each service has dedicated API routes that:
- Require JWT authentication
- Handle errors gracefully
- Log all administrative actions via audit log
- Return consistent JSON responses

### Frontend Integration
JavaScript client provides:
- Automatic token refresh
- Error handling and user notifications
- Real-time data loading
- Interactive UI controls

## Troubleshooting

### Plex Server Not Connecting
1. Verify `PLEX_URL` is correct
2. Verify `PLEX_TOKEN` is valid
3. Check Plex server is running: `curl http://localhost:32400`
4. Check firewall allows connection

### Tautulli Not Accessible
1. Verify `TAUTULLI_URL` is correct
2. Verify `TAUTULLI_API_KEY` is valid
3. Check Tautulli is running on configured port
4. Verify Tautulli has API enabled in settings

### uTorrent Connection Failed
1. Verify `UTORRENT_URL` is correct
2. Verify `UTORRENT_USERNAME` and `UTORRENT_PASSWORD` are correct
3. Check uTorrent WebUI is enabled
4. Verify firewall allows connection

### ruTorrent Not Found
1. Verify `RUTORRENT_URL` is correct
2. Verify credentials if required
3. Check rtorrent daemon is running
4. Verify ruTorrent is accessible at configured URL

## Database

No database schema changes required. New services are managed via:
- Environment configuration
- API clients (no local persistence)
- Container metadata from Docker API
- Audit logs for administrative actions

## Security Considerations

1. **API Tokens**: Store all service API keys in `.env`, never in code
2. **Credentials**: Use strong passwords for uTorrent and ruTorrent
3. **HTTPS**: Enable SSL in production for API endpoint security
4. **Firewall**: Restrict access to admin panel and service management endpoints
5. **Audit Logs**: Monitor audit logs for unusual admin activity
6. **Default Credentials**: Change default admin password immediately

## Performance Notes

- Plex library queries cached for performance
- Torrent lists updated every 10 seconds in UI
- Tautulli data fetched on-demand
- Stream monitoring minimal impact on server

## File Structure

```
backend/
├── plex_service.py          # Plex API wrapper
├── tautulli_service.py      # Tautulli API wrapper
├── utorrent_service.py      # uTorrent API wrapper
├── rutorrent_service.py     # ruTorrent API wrapper
├── routes/
│   ├── api_plex.py          # Plex endpoints
│   ├── api_tautulli.py      # Tautulli endpoints
│   ├── api_utorrent.py      # uTorrent endpoints
│   ├── api_rutorrent.py     # ruTorrent endpoints
│   └── ...
└── config.py                # Updated with new services

frontend/
├── templates/
│   └── index.html           # Updated with new tabs
└── static/js/
    ├── api.js               # Updated with new endpoints
    └── app.js               # Updated with new functions
```

## Next Steps

1. Configure all service URLs and credentials in `.env`
2. Verify each service is accessible from the control panel
3. Test start/stop/restart operations for each service
4. Monitor audit logs for successful operations
5. Setup monitoring alerts if desired

## Support for Additional Services

The architecture supports easy addition of more services:
1. Create new service wrapper in `backend/`
2. Create API routes in `backend/routes/`
3. Register blueprint in `backend/app.py`
4. Add API client methods in `frontend/static/js/api.js`
5. Add UI components in `frontend/templates/index.html`
6. Add JavaScript handlers in `frontend/static/js/app.js`

---

**Version**: 2.0.0
**Updated**: December 2025
**Status**: Production Ready
