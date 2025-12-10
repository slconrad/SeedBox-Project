# Beta Testing & Deployment Recommendations

## 🎯 Beta Phase Strategy

Since you're moving from development to beta, here's a structured approach to validate the system before full production.

---

## 📋 Pre-Beta Checklist

### Environment Setup
- [ ] Create separate `.env.beta` file (keep `.env.production` for later)
- [ ] Use test/staging instances of all services (don't point to production)
- [ ] Set up isolated database (SQLite for beta is fine, but backup regularly)
- [ ] Document all configuration values used
- [ ] Create `BETA_CONFIG.md` with your setup details

### Code Quality
- [ ] Run bandit for security issues: `bandit -r backend/`
- [ ] Check for unused imports: `pip install vulture && vulture backend/`
- [ ] Verify all new endpoints are documented
- [ ] Test database migrations (if adding new models)
- [ ] Validate all environment variables are used

### Testing
- [ ] Test each new service endpoint individually
- [ ] Verify JWT authentication on all 40+ new endpoints
- [ ] Check error handling (try invalid inputs)
- [ ] Validate audit logging is working
- [ ] Test with concurrent users/requests

---

## 🔧 Beta Configuration

### Recommended Settings

```python
# backend/config.py - Add BetaConfig
class BetaConfig(Config):
    """Beta testing configuration"""
    DEBUG = False  # No debug mode in beta
    TESTING = False
    
    # Tighter security than dev but allow some debugging
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    
    # More aggressive rate limiting for testing
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Comprehensive logging
    LOG_LEVEL = "DEBUG"  # Capture everything
    
    # Database backups
    DATABASE_BACKUP_ENABLED = True
    DATABASE_BACKUP_INTERVAL = 3600  # Every hour
    
    # Token expiration - shorter for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=3)
    
    # Session timeout
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
```

### .env.beta Template
```bash
# Flask Configuration
FLASK_ENV=beta
FLASK_DEBUG=False
SECRET_KEY=your-beta-secret-key-change-this-regularly
JWT_SECRET_KEY=your-beta-jwt-key-change-this-regularly

# Database (beta can use SQLite or PostgreSQL)
DATABASE_URL=sqlite:///beta_seedbox.db

# Logging
LOG_FILE=logs/beta.log
LOG_LEVEL=DEBUG

# Service URLs (POINT TO TEST/STAGING INSTANCES)
PLEX_URL=http://localhost:32400  # or your test instance
PLEX_TOKEN=your_test_plex_token

TAUTULLI_URL=http://localhost:8181
TAUTULLI_API_KEY=your_test_api_key

UTORRENT_URL=http://localhost:8080
UTORRENT_USERNAME=testuser
UTORRENT_PASSWORD=testpass

RUTORRENT_URL=http://localhost:8081
RUTORRENT_USERNAME=testuser
RUTORRENT_PASSWORD=testpass

# Radarr, Sonarr, Overseerr URLs (existing)
RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_test_key

SONARR_URL=http://localhost:8989
SONARR_API_KEY=your_test_key

OVERSEERR_URL=http://localhost:5055
OVERSEERR_API_KEY=your_test_key

# Docker Configuration
DOCKER_SOCKET=/var/run/docker.sock

# CORS (restrict to beta tester domains)
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:5000

# Admin Panel Access (beta - can be loose, production will be tight)
ADMIN_IP_WHITELIST=127.0.0.1,localhost

# Backup Settings
BACKUP_ENABLED=True
BACKUP_INTERVAL=3600
BACKUP_RETENTION_DAYS=7
```

---

## 🧪 Beta Testing Plan

### Phase 1: Functionality Testing (Week 1)
**Goal**: Verify all features work as expected

#### Test Each Service
```bash
# Test 1: Plex Service
- [ ] Can retrieve server info
- [ ] Can list libraries
- [ ] Can view active sessions
- [ ] Can refresh library
- [ ] Can restart server
- [ ] Error handling works (test with wrong token)

# Test 2: Tautulli Service
- [ ] Can retrieve stats
- [ ] Can view user activity
- [ ] Can see watch history
- [ ] Error handling for invalid API key

# Test 3: uTorrent Service
- [ ] Can list torrents
- [ ] Can add torrent from URL
- [ ] Can pause/resume/stop torrent
- [ ] Can remove torrent
- [ ] Bandwidth stats display correctly
- [ ] Error handling for connection failures

# Test 4: ruTorrent Service
- [ ] Can list torrents
- [ ] Can start/stop torrents
- [ ] Can remove torrents
- [ ] Stats display correctly
- [ ] Restart functionality works
```

#### Test Admin Panel UI
```bash
# Frontend Testing
- [ ] Torrents tab loads without errors
- [ ] Plex tab loads without errors
- [ ] All buttons are functional
- [ ] Tables display data correctly
- [ ] Search/filter functions work
- [ ] Real-time updates work (if WebSocket enabled)
- [ ] Error messages are helpful
- [ ] Loading spinners show during API calls
```

#### Test Authentication & Security
```bash
- [ ] Login works with valid credentials
- [ ] Login fails with invalid credentials
- [ ] JWT tokens are created
- [ ] Tokens expire properly
- [ ] Can't access admin endpoints without auth
- [ ] Audit logs record all actions
- [ ] Password change works
- [ ] Rate limiting blocks repeated attempts
```

### Phase 2: Performance Testing (Week 2)
**Goal**: Identify bottlenecks and optimize

#### Load Testing
```bash
# Install load testing tool
pip install locust

# Test concurrent API calls
- [ ] Can handle 5 simultaneous users
- [ ] Can handle 10 simultaneous users
- [ ] API response times < 2 seconds
- [ ] No memory leaks over 1 hour usage
- [ ] Database connections stay stable
```

#### Database Performance
```bash
- [ ] Audit logs don't slow down operations
- [ ] Large torrent lists load quickly
- [ ] Library scans don't block UI
- [ ] Database backups don't impact performance
```

#### Service Integration Performance
```bash
- [ ] Plex API calls complete < 3 seconds
- [ ] Tautulli API calls complete < 2 seconds
- [ ] uTorrent/ruTorrent calls complete < 1 second
- [ ] No hanging requests
- [ ] Timeouts handled gracefully
```

### Phase 3: Stability Testing (Week 3)
**Goal**: Ensure reliability over extended use

#### Continuous Operation
```bash
- [ ] Run for 24+ hours without crashing
- [ ] Restart services without data loss
- [ ] Auto-recovery from service failures
- [ ] Graceful handling of service unavailability
- [ ] No memory growth over time
```

#### Failure Scenarios
```bash
- [ ] Plex service goes down → handled gracefully
- [ ] Database connection lost → reconnected
- [ ] Network timeout → retry logic works
- [ ] Invalid credentials → clear error message
- [ ] Disk space low → warning logged
- [ ] Docker socket unavailable → graceful fallback
```

#### Data Integrity
```bash
- [ ] Audit logs never lost
- [ ] Settings preserved after restart
- [ ] User data not corrupted
- [ ] Database backups are valid
- [ ] No orphaned records
```

### Phase 4: Security Testing (Week 4)
**Goal**: Validate security measures work

#### Authentication Testing
```bash
- [ ] SQL injection attempts blocked
- [ ] XSS attempts sanitized
- [ ] CSRF protection works (after implementation)
- [ ] Default credentials changed
- [ ] Weak passwords rejected
- [ ] Brute force attacks throttled
```

#### API Security
```bash
- [ ] CORS properly restricts origins
- [ ] Invalid tokens rejected
- [ ] Expired tokens rejected
- [ ] Privilege escalation attempts blocked
- [ ] API keys never exposed in logs
```

#### Data Security
```bash
- [ ] Passwords hashed properly
- [ ] API keys encrypted in transit
- [ ] Audit logs contain no sensitive data
- [ ] Error messages don't leak info
- [ ] Backups are secured
```

---

## 🐛 Beta Bug Tracking

### Create Issue Template
```markdown
## Bug Report
**Title**: [Brief description]

**Environment**
- Date: [YYYY-MM-DD]
- Browser: [Chrome/Firefox/etc]
- Version: Beta v1.0
- Service affected: [Plex/Tautulli/uTorrent/ruTorrent]

**Steps to Reproduce**
1. [First step]
2. [Second step]
3. [etc]

**Expected Behavior**
[What should happen]

**Actual Behavior**
[What actually happened]

**Logs**
```
[Relevant error logs]
```

**Screenshots**
[If applicable]

**Severity**
- [ ] Critical (system down)
- [ ] High (feature broken)
- [ ] Medium (workaround exists)
- [ ] Low (cosmetic issue)
```

### Bug Tracking Commands
```bash
# View all logs in beta
tail -f logs/beta.log

# Search for errors
grep "ERROR\|EXCEPTION\|CRITICAL" logs/beta.log

# Monitor in real-time
watch -n 1 'tail -20 logs/beta.log'

# Check audit logs
sqlite3 beta_seedbox.db "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 20;"

# Count errors by type
grep "ERROR" logs/beta.log | cut -d' ' -f4 | sort | uniq -c | sort -rn
```

---

## 📊 Monitoring During Beta

### Setup Basic Monitoring
```bash
# Install monitoring tools
pip install prometheus-client psutil

# Create monitoring dashboard
# Monitor: CPU, Memory, Disk, Requests/sec, Errors
```

### Key Metrics to Watch
```python
# backend/monitoring.py (create this)
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Request duration')

# Error metrics
error_count = Counter('errors_total', 'Total errors', ['service'])

# Service metrics
service_health = Gauge('service_health', 'Service health', ['service'])
api_response_time = Histogram('api_response_time', 'API response time', ['service'])

# Database metrics
db_queries = Counter('db_queries', 'Database queries', ['operation'])
db_connections = Gauge('db_connections_active', 'Active database connections')
```

### Health Check Endpoint
```python
# backend/routes/api_health.py
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'version': '2.0.0-beta',
        'services': {
            'plex': check_plex_health(),
            'tautulli': check_tautulli_health(),
            'utorrent': check_utorrent_health(),
            'rutorrent': check_rutorrent_health(),
            'database': check_db_health(),
        },
        'timestamp': datetime.utcnow().isoformat()
    })
```

---

## 🔄 Rollback & Recovery Plan

### Backup Strategy
```bash
# Automated daily backups
0 2 * * * /path/to/backup.sh  # 2 AM daily

# Backup script: backup.sh
#!/bin/bash
BACKUP_DIR="/backups/seedbox"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup database
cp /path/to/beta_seedbox.db "$BACKUP_DIR/db_$TIMESTAMP.db"

# Backup configuration
cp .env.beta "$BACKUP_DIR/env_$TIMESTAMP"

# Compress
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" "$BACKUP_DIR"

# Keep only last 7 days
find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "Backup completed: $TIMESTAMP"
```

### Quick Rollback
```bash
# If something breaks, quickly restore:
# 1. Stop application
systemctl stop seedbox

# 2. Restore from backup
cp /backups/seedbox/db_latest.db /path/to/beta_seedbox.db
cp /backups/seedbox/env_latest /path/to/.env.beta

# 3. Start application
systemctl start seedbox

# 4. Verify
curl http://localhost:5000/api/health
```

### Version Control
```bash
# Tag beta releases
git tag -a beta-v2.0.0 -m "First beta release"
git push origin beta-v2.0.0

# Easy rollback if needed
git checkout beta-v2.0.0

# Compare with production
git diff main beta-v2.0.0
```

---

## 📝 Logging & Diagnostics

### Enhanced Logging Setup
```python
# backend/logging_config.py (create this)
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger

def setup_logging(app):
    """Configure comprehensive logging for beta"""
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Console handler (for immediate feedback)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler (JSON for parsing)
    file_handler = logging.FileHandler('logs/beta.log')
    json_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(json_formatter)
    
    # Rotating file handler (prevent huge files)
    rotating_handler = logging.handlers.RotatingFileHandler(
        'logs/beta_errors.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    rotating_handler.setFormatter(json_formatter)
    rotating_handler.setLevel(logging.ERROR)
    
    # Configure app logger
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(rotating_handler)
    app.logger.setLevel(logging.DEBUG)
    
    return app.logger
```

### Diagnostic Commands
```bash
# Check system resources
free -h          # Memory
df -h            # Disk space
top -b -n 1      # CPU usage

# Check service connectivity
curl -I http://localhost:32400  # Plex
curl -I http://localhost:8181   # Tautulli
curl -I http://localhost:8080   # uTorrent
curl -I http://localhost:8081   # ruTorrent

# Check database
sqlite3 beta_seedbox.db ".tables"
sqlite3 beta_seedbox.db "SELECT COUNT(*) FROM audit_log;"

# Check running processes
ps aux | grep python
ps aux | grep seedbox

# Check ports
netstat -tulpn | grep -E "5000|32400|8181|8080|8081"
```

---

## 🚨 Known Issues & Limitations

### Potential Issues to Watch For
```markdown
## Known Limitations in Beta

1. **Service Dependency**
   - If Plex goes down, Plex tab will show error
   - *Workaround*: Implement circuit breaker pattern

2. **Rate Limiting Not Fully Tested**
   - May need tuning based on real usage
   - *Action*: Monitor and adjust in config.py

3. **WebSocket Stability**
   - Real-time updates may disconnect
   - *Action*: Implement reconnection logic

4. **Database Scaling**
   - SQLite may struggle with millions of audit logs
   - *Action*: Migrate to PostgreSQL for production

5. **Service API Compatibility**
   - May break with service updates
   - *Action*: Version-pin service APIs in wrappers

6. **CORS Whitelist**
   - Currently set to localhost
   - *Action*: Update for your actual domain
```

---

## ✅ Go/No-Go Decision Checklist

### Before Moving to Production

**Functionality** (Must Pass)
- [ ] All 4 services working reliably
- [ ] No data loss after restarts
- [ ] All audit logs recording correctly
- [ ] Authentication working consistently
- [ ] Error handling is graceful

**Performance** (Must Pass)
- [ ] Response times < 2 seconds (99th percentile)
- [ ] No memory leaks over 24 hours
- [ ] Can handle 5+ concurrent users
- [ ] Database queries optimized
- [ ] Service API calls cached appropriately

**Security** (Must Pass)
- [ ] All critical security issues fixed
- [ ] Rate limiting working
- [ ] Default credentials changed
- [ ] CORS properly configured
- [ ] No sensitive data in logs

**Operations** (Must Pass)
- [ ] Backup/restore tested
- [ ] Monitoring alerts working
- [ ] Rollback procedure tested
- [ ] Documentation complete
- [ ] Team trained on operations

**Go/No-Go Vote**
```
Functionality: [ ] GO / [ ] NO-GO
Performance:   [ ] GO / [ ] NO-GO
Security:      [ ] GO / [ ] NO-GO
Operations:    [ ] GO / [ ] NO-GO

Overall:       [ ] PROCEED TO PRODUCTION / [ ] CONTINUE BETA
```

---

## 📅 Beta Timeline

### Recommended Schedule
```
Week 1: Functionality & Integration Testing
  Day 1-2: Service endpoint testing
  Day 3-4: UI/UX testing
  Day 5: Authentication & security testing
  
Week 2: Performance & Load Testing
  Day 1-2: Load testing
  Day 3-4: Database optimization
  Day 5: Network testing
  
Week 3: Stability & Reliability
  Day 1-3: 24+ hour stress tests
  Day 4-5: Failure scenario testing
  
Week 4: Security Hardening & Final Validation
  Day 1-2: Penetration testing
  Day 3: Security audit
  Day 4: Documentation review
  Day 5: Go/no-go decision

Post-Beta: Production Deployment
  Day 1-2: Production environment setup
  Day 3: Final security review
  Day 4: Staged rollout
  Day 5: Full production deployment
```

---

## 🎓 Beta Tester Responsibilities

If inviting others to test:

1. **Report Issues Clearly**
   - Use provided bug template
   - Include logs and screenshots
   - Be specific about steps to reproduce

2. **Test Thoroughly**
   - Don't just click around
   - Follow test cases provided
   - Document what worked and what didn't

3. **Respect Confidentiality**
   - Don't share source code
   - Don't discuss bugs publicly
   - Don't share credentials

4. **Communication**
   - Use dedicated channel (Slack, Discord, etc.)
   - Report daily findings
   - Ask questions about unclear features

---

## 📞 Support Plan for Beta

### Issue Response Times (Beta)
```
Critical (system down):     Response in 2 hours
High (feature broken):      Response in 4 hours
Medium (workaround exists): Response in 24 hours
Low (cosmetic):             Response in 2-3 days
```

### Communication Channels
```
Bugs:           GitHub Issues
Questions:      Email / Slack
Urgent:         Direct message
Feature Requests: GitHub Discussions
```

### Feedback Loops
```
Daily:    Review logs for errors
Weekly:   Send update to testers
Bi-weekly: Review feedback and plan fixes
```

---

## 🎯 Success Metrics for Beta

Beta is considered successful when:

✅ Zero critical bugs found in week 4  
✅ All features work as documented  
✅ Performance meets targets (< 2s response time)  
✅ Security review passes  
✅ 3+ independent testers approve  
✅ All test cases documented and pass  
✅ Documentation is complete and clear  
✅ Support team trained on system  
✅ Runbooks created for operations  
✅ Backup/recovery tested successfully  

---

## 📦 Beta to Production Transition

### Final Checklist Before Production
- [ ] All beta bugs resolved or documented as known issues
- [ ] Performance optimizations completed
- [ ] Security hardening finished
- [ ] Production `.env` configured
- [ ] PostgreSQL database migrated (if upgrading from SQLite)
- [ ] Production SSL certificates obtained
- [ ] Monitoring and alerting configured
- [ ] Incident response plan created
- [ ] Team trained and documented
- [ ] Rollback procedure tested

### Production Deployment Procedure
```bash
# 1. Create production branch
git checkout -b production
git merge main

# 2. Tag release
git tag -a v2.0.0 -m "Production release"

# 3. Switch configuration
mv .env.beta .env.beta.backup
cp .env.production .env

# 4. Stop beta service
systemctl stop seedbox-beta

# 5. Deploy production
systemctl start seedbox

# 6. Verify health
curl http://your-domain/api/health

# 7. Monitor logs
tail -f logs/production.log
```

---

**Status**: Beta v2.0.0 Ready  
**Duration**: 4 weeks recommended  
**Next Step**: Execute Phase 1 testing plan  
**Success Criteria**: See above checklist  
