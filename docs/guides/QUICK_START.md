# SeedBox Control Panel - Quick Reference

## 🚀 Getting Started (5 minutes)

```bash
# 1. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Run
python run.py

# 4. Access
# Open browser to http://localhost:5000
# Login with: admin / admin (CHANGE IN PRODUCTION)
```

---

## 📋 Essential Configuration (.env)

```bash
# Must configure
RADARR_API_KEY=your_key
SONARR_API_KEY=your_key
OVERSEERR_API_KEY=your_key

# Recommended
FLASK_ENV=production
SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
JWT_SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
DATABASE_URL=postgresql://user:pass@localhost/seedbox

# Optional
ENABLE_WEBSOCKET=true
DOCKER_HOST=unix:///var/run/docker.sock
```

---

## 🔑 Default Credentials

**Username:** admin
**Password:** admin

⚠️ **CHANGE IMMEDIATELY IN PRODUCTION**

---

## 🎯 Key Endpoints

### Authentication
```bash
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
```

### Docker
```bash
GET /api/docker/containers
POST /api/docker/containers/{id}/start
POST /api/docker/containers/{id}/stop
GET /api/docker/containers/{id}/logs
```

### Radarr
```bash
GET /api/radarr/movies
GET /api/radarr/queue
GET /api/radarr/stats
```

### Sonarr
```bash
GET /api/sonarr/series
GET /api/sonarr/queue
GET /api/sonarr/stats
```

### Overseerr
```bash
GET /api/overseerr/requests
POST /api/overseerr/requests/{id}/approve
POST /api/overseerr/requests/{id}/decline
```

### System
```bash
GET /api/system/stats
GET /api/system/history
```

---

## 📊 Database

### Initialize
- Automatic on first run
- Creates all tables
- Creates default admin user

### Models
- User, UserPreference, AppConfig
- SystemMetric, ContainerMetric
- AuditLog, MediaLibrary

---

## 🛡️ Security Checklist

- [ ] Change default admin password
- [ ] Generate strong SECRET_KEY
- [ ] Generate strong JWT_SECRET_KEY
- [ ] Set all API keys in .env
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS with SSL cert
- [ ] Configure firewall rules
- [ ] Setup regular backups
- [ ] Review audit logs regularly

---

## 🔧 Common Tasks

### Reset Database
```bash
# Backup first
cp seedbox.db seedbox.db.backup

# Delete and recreate
rm seedbox.db
python -c "from backend.app import create_app; app, _ = create_app(); app.app_context().push()"
```

### View Logs
```bash
tail -f seedbox.log
```

### Create Admin User
```python
from backend.models import User, db
from backend.app import create_app

app, _ = create_app()
with app.app_context():
    user = User(username='newadmin', email='admin@example.com', role='admin')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

### Test API Connection
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Get token from response
# Then use it:
curl -X GET http://localhost:5000/api/system/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🐛 Troubleshooting

### Docker Connection Failed
```bash
# Check Docker socket
ls -l /var/run/docker.sock

# Or configure TCP endpoint in .env
DOCKER_HOST=tcp://your-docker-host:2375
```

### API 401 Unauthorized
- Check token expiration
- Verify JWT_SECRET_KEY not changed
- Re-login and get new token

### Database Lock
- Kill conflicting processes
- Restart application
- Use PostgreSQL for production

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>
```

---

## 📈 Performance Tips

1. Use PostgreSQL instead of SQLite
2. Enable WebSocket for real-time updates
3. Configure caching headers in Nginx
4. Monitor historical metrics retention
5. Cleanup old audit logs periodically

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

---

## 📦 File Locations

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask application |
| `backend/models.py` | Database models |
| `backend/config.py` | Configuration |
| `backend/docker_service.py` | Docker wrapper |
| `backend/routes/` | API endpoints |
| `frontend/templates/` | HTML templates |
| `frontend/static/js/` | JavaScript |
| `.env` | Environment config |

---

## 🔍 Monitoring

### Check Service Health
```bash
curl http://localhost:5000/health
```

### Database Size
```bash
ls -lh seedbox.db
```

### Application Memory
```bash
ps aux | grep python
```

---

## 🚀 Production Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Setup PostgreSQL database
3. Configure `.env` for production
4. Run migrations if needed
5. Start with gunicorn: `gunicorn -w 4 -b 127.0.0.1:5000 backend.app:create_app()`
6. Setup Nginx reverse proxy
7. Configure SSL with Let's Encrypt
8. Setup systemd service
9. Configure firewall
10. Setup log rotation

---

## 📚 Documentation

- **Full Guide**: `IMPLEMENTATION.md`
- **Summary**: `COMPLETION_SUMMARY.md`
- **PWA Info**: `PWA-README.md`

---

## 💡 Tips

- Use `.env` instead of hardcoding secrets
- Check logs for detailed error messages
- Monitor audit logs for suspicious activity
- Regularly backup database
- Keep dependencies updated
- Test API endpoints with Postman/curl first

---

## 🎯 Architecture Overview

```
┌─────────────────┐
│    Frontend     │ (Browser/PWA)
│  (Templates)    │
└────────┬────────┘
         │ HTTP/WS
┌────────▼────────┐
│   Flask API     │ (Port 5000)
│  (Routes)       │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┬─────────┐
    │          │         │          │         │
┌───▼──┐  ┌──▼──┐  ┌───▼──┐  ┌──▼──┐  ┌───▼──┐
│Docker│  │Sys  │  │Radarr│  │Sonarr│ │Over- │
│      │  │Stats│  │      │  │      │ │seerr │
└──────┘  └─────┘  └──────┘  └──────┘  └──────┘
    │
┌───▼──────┐
│ Database │ (SQLite/PostgreSQL)
└──────────┘
```

---

## 🆘 Getting Help

1. Check `IMPLEMENTATION.md` for detailed setup
2. Review logs in `seedbox.log`
3. Check Docker output for service errors
4. Verify `.env` configuration
5. Test API endpoints manually
6. Review audit logs for issues

---

## 📝 License & Credits

- SeedBox Control Panel v1.0.0
- Complete implementation of Phases 1-6
- Full 'RR' stack integration
- Production-ready codebase

---

**Last Updated**: December 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
