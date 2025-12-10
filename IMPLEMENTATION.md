# SeedBox Control Panel - Complete Implementation Guide

## Overview

This is a production-ready SeedBox administration panel implementing all 6 phases:

1. **Phase 1**: Database setup & Docker integration ✅
2. **Phase 2**: Authentication & JWT setup ✅
3. **Phase 3**: Jinja2 templates & real data ✅
4. **Phase 4**: WebSocket & real-time updates ✅
5. **Phase 5**: 'RR' stack API integrations (Radarr, Sonarr, Overseerr) ✅
6. **Phase 6**: Error handling & optimization ✅

---

## Project Structure

```
seedbox-panel/
├── backend/
│   ├── __init__.py
│   ├── app.py                    # Flask application factory
│   ├── config.py                 # Configuration management
│   ├── models.py                 # SQLAlchemy models
│   ├── docker_service.py         # Docker wrapper
│   ├── system_service.py         # System monitoring
│   ├── radarr_service.py         # Radarr API wrapper
│   ├── sonarr_service.py         # Sonarr API wrapper
│   ├── overseerr_service.py      # Overseerr API wrapper
│   ├── utils.py                  # Decorators & utilities
│   └── routes/
│       ├── __init__.py
│       ├── api_auth.py           # Authentication endpoints
│       ├── api_docker.py         # Docker management endpoints
│       ├── api_system.py         # System stats endpoints
│       ├── api_radarr.py         # Radarr endpoints
│       ├── api_sonarr.py         # Sonarr endpoints
│       └── api_overseerr.py      # Overseerr endpoints
│
├── frontend/
│   ├── templates/
│   │   ├── base.html             # Base Jinja2 template
│   │   └── index.html            # Main dashboard template
│   └── static/
│       ├── js/
│       │   ├── api.js            # API client
│       │   ├── app.js            # Main application logic
│       │   └── charts.js         # Chart initialization (if needed)
│       ├── css/
│       │   └── style.css         # Custom styles
│       ├── manifest.json         # PWA manifest
│       └── sw.js                 # Service Worker
│
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
├── docker-compose.yml            # Docker composition (if added)
└── README.md                     # Project documentation
```

---

## Installation & Setup

### 1. Install Dependencies

```bash
# Navigate to project directory
cd seedbox-panel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your values
nano .env  # Or use your editor
```

**Required settings:**
- `SECRET_KEY`: Change to random string
- `JWT_SECRET_KEY`: Change to random string
- `RADARR_API_KEY`: From Radarr settings
- `SONARR_API_KEY`: From Sonarr settings
- `OVERSEERR_API_KEY`: From Overseerr settings
- Database URL if using PostgreSQL

### 3. Initialize Database

```bash
# The database will auto-create on first run
# Default credentials:
# Username: admin
# Password: admin  (CHANGE THIS IN PRODUCTION)
```

### 4. Run Application

```bash
# Development
python run.py

# Production with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:create_app()
```

Access at: `http://localhost:5000`

---

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/register` - Register new user (admin only)

### System Monitoring
- `GET /api/system/stats` - Current system stats
- `GET /api/system/cpu` - CPU details
- `GET /api/system/memory` - Memory details
- `GET /api/system/disk` - Disk usage
- `GET /api/system/network` - Network stats
- `GET /api/system/processes` - Top processes
- `GET /api/system/sensors` - Sensor data
- `GET /api/system/history` - Historical metrics

### Docker Management
- `GET /api/docker/status` - Docker daemon status
- `GET /api/docker/containers` - List all containers
- `GET /api/docker/containers/<id>` - Get container details
- `POST /api/docker/containers/<id>/start` - Start container
- `POST /api/docker/containers/<id>/stop` - Stop container
- `POST /api/docker/containers/<id>/restart` - Restart container
- `GET /api/docker/containers/<id>/logs` - Get container logs
- `GET /api/docker/networks` - List networks
- `GET /api/docker/volumes` - List volumes

### Radarr Integration
- `GET /api/radarr/health` - Check Radarr health
- `GET /api/radarr/status` - Radarr status
- `GET /api/radarr/movies` - List movies
- `GET /api/radarr/stats` - Movie statistics
- `GET /api/radarr/upcoming` - Upcoming releases
- `GET /api/radarr/queue` - Download queue
- `GET /api/radarr/history` - Recent history
- `POST /api/radarr/search/<id>` - Search for movie

### Sonarr Integration
- `GET /api/sonarr/health` - Check Sonarr health
- `GET /api/sonarr/status` - Sonarr status
- `GET /api/sonarr/series` - List series
- `GET /api/sonarr/stats` - Series statistics
- `GET /api/sonarr/calendar` - Upcoming episodes
- `GET /api/sonarr/queue` - Download queue
- `GET /api/sonarr/wanted` - Wanted episodes
- `GET /api/sonarr/history` - Recent history
- `POST /api/sonarr/search/<id>` - Search for series

### Overseerr Integration
- `GET /api/overseerr/health` - Check Overseerr health
- `GET /api/overseerr/status` - Overseerr status
- `GET /api/overseerr/requests` - Get requests
- `GET /api/overseerr/stats` - Request statistics
- `GET /api/overseerr/users` - List users
- `POST /api/overseerr/requests/<id>/approve` - Approve request
- `POST /api/overseerr/requests/<id>/decline` - Decline request
- `GET /api/overseerr/settings` - Settings

---

## Database Models

### User
- Stores user credentials and roles
- Supports admin/moderator/user roles
- Password hashed with Werkzeug

### UserPreference
- Stores per-user preferences

### AppConfig
- Application configuration storage

### ContainerMetric
- Historical container metrics (CPU, memory, network)

### SystemMetric
- Historical system metrics

### AuditLog
- Complete audit trail of admin actions

### MediaLibrary
- Cached media information from Radarr/Sonarr

---

## Real-time Updates (Phase 4)

WebSocket support is available when `ENABLE_WEBSOCKET=true`:

```javascript
// Client-side WebSocket example
const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('stats_update', (data) => {
    console.log('New stats:', data);
});

socket.emit('request_stats', {}, (response) => {
    console.log('Stats response:', response);
});
```

---

## Error Handling & Validation (Phase 6)

### Features
- JWT token validation
- Role-based access control
- Input validation
- Comprehensive error messages
- Audit logging for all actions
- Rate limiting support

### Error Response Format
```json
{
    "error": "Error message",
    "status": 400
}
```

---

## Security Considerations

1. **Change default credentials** - Admin/admin in production
2. **Use strong SECRET_KEY** - Generate with `secrets.token_urlsafe(32)`
3. **Enable HTTPS** - Use SSL/TLS in production
4. **Configure CORS** - Restrict to your domain
5. **Database** - Use PostgreSQL with strong password
6. **API Keys** - Rotate regularly, never commit to repo
7. **Rate limiting** - Implemented for API endpoints

---

## Docker Integration

### Supported Operations
- List containers (running/stopped)
- Start/stop/restart containers
- Real-time resource monitoring
- Log streaming
- Container inspection
- Network management
- Volume management

### Requirements
- Docker daemon accessible
- Unix socket or TCP endpoint configured
- Appropriate permissions

---

## 'RR' Stack Integration Details

### Radarr
- Movie library management
- Download queue monitoring
- Upcoming releases
- Search functionality
- Library statistics

### Sonarr
- TV series management
- Episode monitoring
- Wanted episodes tracking
- Download queue
- Calendar view

### Overseerr
- Media request management
- User request approval workflow
- Request statistics
- User management

---

## Deployment

### Production Setup with Nginx

```nginx
upstream seedbox {
    server 127.0.0.1:5000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://seedbox;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Docker Compose Example

```yaml
services:
  seedbox-panel:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/seedbox
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: seedbox
      POSTGRES_USER: seedbox
      POSTGRES_PASSWORD: securepassword
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

## Monitoring & Maintenance

### Database Maintenance
```bash
# Backup database
cp seedbox.db seedbox.db.backup

# Clean old metrics (keep 30 days)
# Run periodically in cron
```

### Log Management
```bash
# View logs
tail -f seedbox.log

# Rotate logs
logrotate -f /etc/logrotate.d/seedbox
```

---

## Troubleshooting

### Docker Connection Failed
- Check Docker socket permissions
- Verify Docker daemon running
- Confirm `DOCKER_HOST` setting

### API Connection Issues
- Verify API keys in .env
- Check service URLs
- Ensure services running
- Check firewall rules

### Database Errors
- Run migrations: `flask db upgrade`
- Check database permissions
- Verify connection string

### Authentication Failed
- Check JWT secret configuration
- Clear browser cookies
- Verify user role
- Check token expiration

---

## Contributing

1. Create feature branch
2. Make changes
3. Run tests: `pytest`
4. Format code: `black backend/`
5. Lint: `flake8 backend/`
6. Submit pull request

---

## License

Proprietary - SeedBox Project

---

## Support

For issues and questions:
1. Check documentation
2. Review logs
3. Check GitHub issues
4. Contact development team

---

## Changelog

### v1.0.0
- Initial release
- Complete Phase 1-6 implementation
- Full 'RR' stack integration
- PWA support
- Real-time updates
- Comprehensive error handling
