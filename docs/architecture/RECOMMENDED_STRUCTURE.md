# Recommended Project Structure

## 📁 Proposed Directory Organization

```
SeedBox-Project/
│
├── 📄 README.md                          # Main project overview (keep in root)
├── .gitignore
├── .env.example
├── requirements.txt
├── run.py                                # Entry point
│
├── 📁 docs/                              # All documentation
│   ├── 📄 INDEX.md                       # Documentation index/TOC
│   ├── 📄 QUICK_START.md                 # Quick start guide
│   │
│   ├── 📁 guides/                        # User & setup guides
│   │   ├── STACK_UPDATE.md               # Stack expansion details
│   │   ├── EXPANSION_SUMMARY.md          # Change summary
│   │   └── SERVICES_REFERENCE.md         # Service quick reference
│   │
│   ├── 📁 security/                      # Security documentation
│   │   ├── SECURITY_ANALYSIS.md          # Security audit & recommendations
│   │   ├── SECURITY_CHECKLIST.md         # Pre-deployment checklist
│   │   └── SECURITY_PROCEDURES.md        # Security procedures
│   │
│   ├── 📁 operations/                    # Operations & deployment
│   │   ├── BETA_RECOMMENDATIONS.md       # Beta testing plan
│   │   ├── DEPLOYMENT.md                 # Deployment procedures
│   │   ├── RUNBOOKS.md                   # Operational runbooks
│   │   └── TROUBLESHOOTING.md            # Troubleshooting guide
│   │
│   ├── 📁 api/                           # API documentation
│   │   ├── API_OVERVIEW.md               # API architecture
│   │   ├── ENDPOINTS.md                  # All endpoints listed
│   │   └── EXAMPLES.md                   # API usage examples
│   │
│   └── 📁 architecture/                  # System architecture
│       ├── ARCHITECTURE.md               # System design
│       ├── DATABASE.md                   # Database schema
│       └── SERVICES.md                   # Service descriptions
│
├── 📁 backend/                           # Flask backend
│   ├── __init__.py
│   ├── app.py                            # Flask app factory
│   ├── config.py                         # Configuration
│   ├── models.py                         # Database models
│   ├── utils.py                          # Utilities & decorators
│   │
│   ├── 📁 routes/                        # API route blueprints
│   │   ├── __init__.py
│   │   ├── api_auth.py                   # Authentication endpoints
│   │   ├── api_system.py                 # System endpoints
│   │   ├── api_docker.py                 # Docker endpoints
│   │   ├── api_radarr.py                 # Radarr endpoints
│   │   ├── api_sonarr.py                 # Sonarr endpoints
│   │   ├── api_overseerr.py              # Overseerr endpoints
│   │   ├── api_plex.py                   # Plex endpoints
│   │   ├── api_tautulli.py               # Tautulli endpoints
│   │   ├── api_utorrent.py               # uTorrent endpoints
│   │   └── api_rutorrent.py              # ruTorrent endpoints
│   │
│   ├── 📁 services/                      # Service wrappers
│   │   ├── __init__.py
│   │   ├── docker_service.py             # Docker wrapper
│   │   ├── system_service.py             # System wrapper
│   │   ├── radarr_service.py             # Radarr wrapper
│   │   ├── sonarr_service.py             # Sonarr wrapper
│   │   ├── overseerr_service.py          # Overseerr wrapper
│   │   ├── plex_service.py               # Plex wrapper
│   │   ├── tautulli_service.py           # Tautulli wrapper
│   │   ├── utorrent_service.py           # uTorrent wrapper
│   │   └── rutorrent_service.py          # ruTorrent wrapper
│   │
│   └── 📁 migrations/                    # Database migrations (if using Alembic)
│       └── [migration files]
│
├── 📁 frontend/                          # Web frontend
│   ├── 📁 templates/
│   │   ├── index.html                    # Main page
│   │   ├── base.html                     # Base template
│   │   └── [other templates]
│   │
│   └── 📁 static/
│       ├── 📁 css/
│       │   ├── style.css                 # Main stylesheet
│       │   └── [other stylesheets]
│       │
│       ├── 📁 js/
│       │   ├── app.js                    # Main app logic
│       │   ├── api.js                    # API client
│       │   └── [other scripts]
│       │
│       └── 📁 images/
│           └── [image assets]
│
├── 📁 tests/                             # Test suite
│   ├── __init__.py
│   ├── conftest.py                       # Pytest configuration
│   ├── 📁 unit/                          # Unit tests
│   │   ├── test_auth.py
│   │   ├── test_services.py
│   │   └── [other unit tests]
│   ├── 📁 integration/                   # Integration tests
│   │   ├── test_api.py
│   │   └── [other integration tests]
│   └── 📁 fixtures/                      # Test fixtures & mocks
│       └── sample_data.py
│
├── 📁 scripts/                           # Utility scripts
│   ├── backup.sh                         # Backup script
│   ├── restore.sh                        # Restore script
│   ├── deploy.sh                         # Deployment script
│   ├── setup_env.sh                      # Environment setup
│   └── [other utility scripts]
│
├── 📁 config/                            # Configuration files
│   ├── docker-compose.yml                # Docker Compose config
│   ├── nginx.conf                        # Nginx reverse proxy config
│   ├── supervisord.conf                  # Supervisor config (if used)
│   └── [other config files]
│
├── 📁 logs/                              # Log files (gitignored)
│   ├── .gitkeep
│   └── [log files generated at runtime]
│
├── 📁 backups/                           # Database backups (gitignored)
│   ├── .gitkeep
│   └── [backup files generated at runtime]
│
├── 📁 venv/                              # Virtual environment (gitignored)
│   └── [virtual env files]
│
└── 📁 .github/                           # GitHub specific
    ├── 📁 workflows/
    │   ├── tests.yml                     # Test CI/CD
    │   ├── security.yml                  # Security scanning
    │   └── deploy.yml                    # Deploy workflow
    └── ISSUE_TEMPLATE/
        └── bug_report.md

```

---

## 📊 Structure Summary

### **Root Level** (Keep Minimal)
- `README.md` - Main entry point for project
- `.gitignore` - Git ignore rules
- `.env.example` - Example environment variables
- `requirements.txt` - Python dependencies
- `run.py` - Application entry point

### **docs/** (All Documentation)
- **guides/** - User and setup guides
- **security/** - Security documentation
- **operations/** - Deployment and operational docs
- **api/** - API documentation
- **architecture/** - System architecture docs

### **backend/** (Flask Application)
- **routes/** - API route blueprints (organized by service)
- **services/** - Service wrapper classes
- Core files: `app.py`, `config.py`, `models.py`, `utils.py`

### **frontend/** (Web Interface)
- **templates/** - HTML templates
- **static/** - CSS, JavaScript, images

### **tests/** (Test Suite)
- **unit/** - Unit tests
- **integration/** - Integration tests
- **fixtures/** - Test fixtures

### **scripts/** - Utility & automation scripts
### **config/** - Configuration files (Docker, Nginx, etc.)
### **logs/** - Runtime logs (gitignored)
### **backups/** - Database backups (gitignored)

---

## 🚀 Implementation Steps

### Step 1: Create Directory Structure
```bash
cd /Users/shawnconrad/Library/Mobile\ Documents/com~apple~CloudDocs/Development/SeedBox\ Project

# Create all directories
mkdir -p docs/{guides,security,operations,api,architecture}
mkdir -p backend/routes
mkdir -p backend/services
mkdir -p backend/migrations
mkdir -p frontend/templates
mkdir -p frontend/static/{css,js,images}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p scripts
mkdir -p config
mkdir -p logs
mkdir -p backups

# Create .gitkeep files to preserve empty directories
touch logs/.gitkeep
touch backups/.gitkeep
```

### Step 2: Move Files
```bash
# Move markdown files to docs
mv *.md docs/

# Move service files to backend/services
mv backend/plex_service.py backend/services/
mv backend/tautulli_service.py backend/services/
mv backend/utorrent_service.py backend/services/
mv backend/rutorrent_service.py backend/services/
# ... move other service files

# Move API route files to backend/routes
mv backend/routes/api_*.py backend/routes/
# (if not already there)

# Move static files to frontend
# (if needed)
```

### Step 3: Create INDEX.md
Create `docs/INDEX.md` as the documentation entry point:

```markdown
# SeedBox Documentation Index

## Getting Started
- [Quick Start Guide](QUICK_START.md)
- [Setup Instructions](guides/SETUP.md)

## Features
- [Stack Update](guides/STACK_UPDATE.md)
- [Services Reference](guides/SERVICES_REFERENCE.md)
- [API Overview](api/API_OVERVIEW.md)

## Security
- [Security Analysis](security/SECURITY_ANALYSIS.md)
- [Security Checklist](security/SECURITY_CHECKLIST.md)

## Operations
- [Beta Testing](operations/BETA_RECOMMENDATIONS.md)
- [Deployment Guide](operations/DEPLOYMENT.md)
- [Troubleshooting](operations/TROUBLESHOOTING.md)

## Architecture
- [System Architecture](architecture/ARCHITECTURE.md)
- [Database Schema](architecture/DATABASE.md)
```

### Step 4: Update .gitignore
```bash
# Add to .gitignore
venv/
__pycache__/
*.pyc
.env
logs/
backups/
.DS_Store
*.sqlite
*.db
.vscode/settings.json
```

### Step 5: Commit Changes
```bash
git add .
git commit -m "refactor: reorganize project structure

- Create docs/ for all documentation by category
- Create backend/services/ for service wrappers
- Create tests/ directory structure
- Create config/, scripts/, logs/, backups/ directories
- Add .gitkeep files for empty directories
- Update .gitignore"
```

---

## 📋 File Organization Checklist

**Documentation Files:**
- [ ] Move all .md files to `docs/`
- [ ] Organize into subdirectories (guides/, security/, operations/, api/, architecture/)
- [ ] Create `docs/INDEX.md` as entry point
- [ ] Update README.md with links to documentation

**Backend Files:**
- [ ] Move all service_*.py files to `backend/services/`
- [ ] Verify all route files are in `backend/routes/`
- [ ] Keep core files in `backend/` (app.py, config.py, models.py, utils.py)
- [ ] Create `__init__.py` files in all subdirectories

**Frontend Files:**
- [ ] Verify structure in `frontend/templates/` and `frontend/static/`
- [ ] Organize static files into css/, js/, images/

**Testing:**
- [ ] Create test files in `tests/unit/` and `tests/integration/`
- [ ] Create `conftest.py` for pytest configuration

**Other:**
- [ ] Move utility scripts to `scripts/`
- [ ] Move configuration files to `config/`
- [ ] Create `.gitkeep` in logs/ and backups/

---

## ✅ Benefits of This Structure

✅ **Organized** - Easy to navigate and find files  
✅ **Scalable** - Room to grow without cluttering  
✅ **Professional** - Follows Python project conventions  
✅ **Maintainable** - Clear separation of concerns  
✅ **Testable** - Dedicated tests/ directory  
✅ **Documented** - docs/ organized by topic  
✅ **Deployable** - config/ and scripts/ ready for production  
✅ **Git-friendly** - Easy to navigate history  

---

## 🔄 Before & After

### Before (Current):
```
SeedBox-Project/
├── *.md files (scattered)
├── backend/
│   ├── *_service.py (mixed with other files)
│   └── routes/
├── frontend/
└── requirements.txt
```

### After (Recommended):
```
SeedBox-Project/
├── docs/                    ← All documentation organized
├── backend/
│   ├── services/           ← Service wrappers organized
│   ├── routes/             ← API routes organized
│   └── core files
├── frontend/               ← Frontend organized
├── tests/                  ← Test suite
├── scripts/                ← Utilities
└── config/                 ← Configuration
```

---

**Ready to implement? I can help with the actual file moves and reorganization!** 🚀
