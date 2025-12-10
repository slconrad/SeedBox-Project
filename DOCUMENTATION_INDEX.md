# 📖 SeedBox Control Panel - Documentation Index

## 🎯 Quick Navigation

### For First-Time Setup
1. **Start here**: [`QUICK_START.md`](QUICK_START.md) - 5-minute setup guide
2. **Then read**: [`STACK_UPDATE.md`](STACK_UPDATE.md) - New features overview
3. **Environment**: [`.env.example`](.env.example) - Configuration template

### For Developers
1. **Architecture**: [`IMPLEMENTATION.md`](IMPLEMENTATION.md) - Complete architecture guide
2. **Changes**: [`EXPANSION_SUMMARY.md`](EXPANSION_SUMMARY.md) - All modifications made
3. **Reference**: [`SERVICES_REFERENCE.md`](SERVICES_REFERENCE.md) - API endpoints & examples

### For Operations
1. **Getting Started**: [`QUICK_START.md`](QUICK_START.md) - Basic operations
2. **Features**: [`STACK_UPDATE.md`](STACK_UPDATE.md) - What's available
3. **Troubleshooting**: [`SERVICES_REFERENCE.md`](SERVICES_REFERENCE.md) - Common issues

### For Verification
1. **Summary**: [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) - What was built
2. **Coverage**: [`EXPANSION_SUMMARY.md`](EXPANSION_SUMMARY.md) - Testing checklist

---

## 📚 All Documentation Files

### Core Documentation

| File | Purpose | Audience | Length |
|------|---------|----------|--------|
| **QUICK_START.md** | Fast setup and operation guide | Everyone | 5 min read |
| **STACK_UPDATE.md** | Complete feature overview and guide | Operators | 20 min read |
| **SERVICES_REFERENCE.md** | Quick reference and examples | Developers | 15 min read |
| **IMPLEMENTATION.md** | Full architecture and setup | Developers | 30 min read |
| **EXPANSION_SUMMARY.md** | Change manifest and details | Developers | 15 min read |
| **COMPLETION_REPORT.md** | Delivery summary | Project Managers | 10 min read |
| **COMPLETION_SUMMARY.md** | Previous implementation summary | Reference | 20 min read |
| **PWA-README.md** | Progressive Web App features | Frontend Devs | 10 min read |

---

## 🗂️ Project Structure

### Backend Services
```
backend/
├── app.py                       # Flask app factory
├── config.py                    # Configuration management
├── models.py                    # Database models
├── utils.py                     # Utility functions
├── docker_service.py            # Docker API wrapper
├── system_service.py            # System monitoring
├── radarr_service.py           # Radarr integration
├── sonarr_service.py           # Sonarr integration
├── overseerr_service.py        # Overseerr integration
├── plex_service.py             # Plex integration (NEW)
├── tautulli_service.py         # Tautulli integration (NEW)
├── utorrent_service.py         # uTorrent integration (NEW)
├── rutorrent_service.py        # ruTorrent integration (NEW)
└── routes/
    ├── api_auth.py             # Authentication endpoints
    ├── api_docker.py           # Docker management
    ├── api_system.py           # System monitoring
    ├── api_radarr.py           # Radarr endpoints
    ├── api_sonarr.py           # Sonarr endpoints
    ├── api_overseerr.py        # Overseerr endpoints
    ├── api_plex.py             # Plex endpoints (NEW)
    ├── api_tautulli.py         # Tautulli endpoints (NEW)
    ├── api_utorrent.py         # uTorrent endpoints (NEW)
    └── api_rutorrent.py        # ruTorrent endpoints (NEW)
```

### Frontend Assets
```
frontend/
├── templates/
│   ├── base.html               # Base template with PWA tags
│   └── index.html              # Main dashboard (UPDATED)
└── static/
    ├── js/
    │   ├── api.js              # API client (UPDATED)
    │   └── app.js              # Application logic (UPDATED)
    └── css/
        └── style.css           # Styling
```

### Configuration & Utilities
```
.env.example                     # Environment template (UPDATED)
requirements.txt                # Python dependencies
run.py                          # Application entry point
seedbox.db                      # SQLite database (created on first run)
```

---

## 🔑 Key Concepts

### Service Wrappers
Each service has a dedicated wrapper class:
- **Purpose**: Isolate service communication logic
- **Pattern**: Consistent error handling, logging, retry logic
- **Files**: `{service}_service.py` in `backend/`

### API Routes
Each service has dedicated API endpoints:
- **Purpose**: REST interface for service management
- **Pattern**: JWT authentication, audit logging, error handling
- **Files**: `api_{service}.py` in `backend/routes/`

### Frontend Integration
JavaScript handles all UI interactions:
- **API Client**: `api.js` - Centralized service calls
- **Application Logic**: `app.js` - UI updates and interactions
- **Templates**: `index.html` - HTML structure

---

## 🚀 Deployment Workflow

### 1. Pre-Deployment (5 min)
```bash
# Copy environment template
cp .env.example .env

# Edit with your service URLs and API keys
vim .env  # Configure all 4 new services
```

### 2. Installation (5 min)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch (2 min)
```bash
# Start application
python run.py

# Access at http://localhost:5000
# Login with admin/admin (change password!)
```

### 4. Verification (5 min)
- [ ] Dashboard loads
- [ ] Torrents tab accessible
- [ ] Plex tab accessible
- [ ] Can see service status

---

## 📋 API Endpoint Summary

| Service | Endpoints | Purpose |
|---------|-----------|---------|
| **Plex** | 9 | Media server management |
| **Tautulli** | 10 | Plex monitoring |
| **uTorrent** | 11 | Torrent management |
| **ruTorrent** | 10 | Web torrent client |
| **Radarr** | 7 | Movie automation |
| **Sonarr** | 7 | TV automation |
| **Overseerr** | 6 | Media requests |
| **Docker** | 9 | Container management |
| **System** | 7 | Resource monitoring |
| **Auth** | 6 | Authentication |
| **TOTAL** | **80+** | Complete platform |

---

## 🔒 Security Checklist

Before going to production:

- [ ] Change default admin password
- [ ] Generate strong SECRET_KEY
- [ ] Generate strong JWT_SECRET_KEY
- [ ] Store all API keys in `.env`
- [ ] Never commit `.env` to version control
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Setup backup schedule
- [ ] Monitor audit logs

---

## 🧪 Testing Guide

### Unit Tests (Per Service)
```bash
# Test authentication
pytest tests/test_auth.py

# Test Docker service
pytest tests/test_docker.py

# Test API endpoints
pytest tests/test_api.py
```

### Integration Tests
```bash
# Test full workflow
pytest tests/integration/

# Test all endpoints
pytest tests/endpoints/
```

### Manual Testing Checklist
- [ ] Login works
- [ ] Dashboard loads
- [ ] Each tab loads
- [ ] Service actions execute
- [ ] Audit logs record actions

---

## 📊 Monitoring & Logs

### Log Locations
- **Application**: `seedbox.log`
- **Database**: `seedbox.db`
- **Config**: `.env`

### Important Log Lines
```bash
# Monitor in real-time
tail -f seedbox.log

# Check for errors
grep ERROR seedbox.log

# Check audit trail
sqlite3 seedbox.db "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 10;"
```

---

## 🎓 Architecture Decisions

### Why This Design?

**Service Wrappers**
- Encapsulation of external API logic
- Easy to test and mock
- Simple to add new services

**Blueprints**
- Organize routes by service
- Independent testing
- Clear separation of concerns

**Jinja2 Templates**
- Server-side rendering
- Security (no template injection)
- SEO-friendly

**Environment Configuration**
- Secrets not in code
- Easy deployment to different environments
- Follows 12-factor app principles

---

## 🔧 Customization Guide

### Adding a New Service

1. Create service wrapper:
   ```python
   # backend/myservice_service.py
   class MyServiceService:
       def __init__(self, url, api_key):
           # Initialize connection
   ```

2. Create API routes:
   ```python
   # backend/routes/api_myservice.py
   @bp.route('/status', methods=['GET'])
   def get_status():
       # Return status
   ```

3. Register blueprint:
   ```python
   # backend/app.py
   from routes import api_myservice
   app.register_blueprint(api_myservice.bp)
   ```

4. Add API methods:
   ```javascript
   // frontend/static/js/api.js
   async getMyServiceStatus() {
       return this.get('/myservice/status');
   }
   ```

5. Update UI:
   ```html
   <!-- frontend/templates/index.html -->
   <button onclick="showTab('myservice')">My Service</button>
   ```

---

## 📞 Support & Resources

### Internal Documentation
- `STACK_UPDATE.md` - Feature deep dive
- `SERVICES_REFERENCE.md` - API examples
- `IMPLEMENTATION.md` - Architecture details

### External Resources
- **Plex API**: https://www.plex.tv/
- **Tautulli**: https://tautulli.com/
- **uTorrent**: https://www.bittorrent.com/
- **ruTorrent**: https://github.com/rakshasa/rtorrent/
- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/

### Common Issues
See `SERVICES_REFERENCE.md` section: "Troubleshooting"

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | Dec 2025 | Added Plex, Tautulli, uTorrent, ruTorrent |
| 1.0.0 | Dec 2025 | Initial release with Docker, Radarr, Sonarr, Overseerr |

---

## ✅ Status

**Current Version**: 2.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: December 9, 2025  
**Maintainer**: Shawn Conrad  

---

## 📝 Document Legend

- 📖 = Read First
- 🚀 = Setup & Deployment
- 🔧 = Configuration
- 📚 = Reference
- 🧪 = Testing
- 🔒 = Security

---

## 💡 Pro Tips

1. **Use Docker Compose** - Run all services in containers
2. **Enable Backups** - Backup database regularly
3. **Monitor Logs** - Watch for errors early
4. **Audit Regularly** - Review audit logs weekly
5. **Update Services** - Keep all services up to date
6. **Test First** - Test in dev before production

---

**For questions or issues, refer to the documentation index above or check SERVICES_REFERENCE.md for troubleshooting.**
