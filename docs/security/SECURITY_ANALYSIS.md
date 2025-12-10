# Security Analysis & Recommendations - SeedBox Control Panel

## 🔒 Current Security Implementation

### ✅ What's Currently Secured

#### 1. Authentication
- ✅ JWT tokens with secure signing
- ✅ Password hashing with Werkzeug
- ✅ Refresh token mechanism
- ✅ Token expiration (24 hours access, 30 days refresh)
- ✅ Inactive user detection

#### 2. Authorization
- ✅ Role-based access control (admin, moderator, user)
- ✅ JWT verification on all API endpoints
- ✅ Admin-only decorators
- ✅ User activity tracking

#### 3. Audit Logging
- ✅ All admin actions logged with timestamp, IP, user
- ✅ Failed login attempts recorded
- ✅ Action targets and details captured
- ✅ Error messages logged for debugging

#### 4. Input Validation
- ✅ Required field checking
- ✅ Duplicate user prevention
- ✅ Error message sanitization
- ✅ JSON parsing with error handling

#### 5. Data Protection
- ✅ Database query parameterization (SQLAlchemy ORM)
- ✅ Sensitive data not logged
- ✅ Password hashing with salt
- ✅ API keys in environment variables only

---

## ⚠️ Security Issues Found

### CRITICAL Issues

#### 1. **CORS Configuration (CRITICAL)**
```python
# Current - DANGEROUS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```
**Risk**: Allows any website to access your API endpoints
**Impact**: Cross-site attacks, unauthorized API calls from any domain

#### 2. **API Keys in Service Wrappers (CRITICAL)**
Service wrappers pass credentials directly:
```python
# Example from plex_service.py
self.headers = {'X-Plex-Token': token}
```
**Risk**: Tokens visible in logs, error messages
**Impact**: Token exposure in debug output

#### 3. **Rate Limiting Not Applied (HIGH)**
Rate limit decorator exists but not used on auth endpoints
```python
# Defined but NOT applied
@bp.route('/login', methods=['POST'])
def login():  # No rate limiting!
```
**Risk**: Brute force attacks on login endpoint
**Impact**: Password guessing attacks possible

#### 4. **Default Admin Credentials (HIGH)**
```python
# In app.py - DEFAULT CREDENTIALS
admin.set_password('admin')  # CHANGE THIS IN PRODUCTION
```
**Risk**: Anyone knows default password
**Impact**: Immediate unauthorized access

#### 5. **Missing HTTPS Enforcement (HIGH)**
No SSL/TLS enforcement in development mode
**Risk**: Credentials sent in plaintext
**Impact**: Network sniffing on HTTP

#### 6. **Overly Broad Error Messages (MEDIUM)**
Some endpoints return detailed error information
**Risk**: Information disclosure about system
**Impact**: Helps attackers map system

#### 7. **Missing CSRF Protection (MEDIUM)**
No CSRF tokens on state-changing operations
**Risk**: Cross-site request forgery attacks
**Impact**: Unauthorized actions via browser

---

## 🔐 Security Recommendations

### IMMEDIATE ACTIONS (Do Before Production)

#### 1. **Fix CORS Configuration**
```python
# Update backend/app.py
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://your-domain.com",
        "https://admin.your-domain.com"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type"],
    "supports_credentials": True,
    "max_age": 3600
}})
```

#### 2. **Enable HTTPS Everywhere**
```bash
# Use Let's Encrypt with Nginx
certbot certonly --nginx -d your-domain.com

# In Nginx config
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
}
```

#### 3. **Change Default Admin Password**
Update during first login or:
```bash
# Via API
curl -X POST http://localhost:5000/api/auth/change-password \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"old_password":"admin","new_password":"STRONG_PASSWORD"}'
```

#### 4. **Add Rate Limiting to Auth**
Update `backend/routes/api_auth.py`:
```python
from utils import rate_limit

@bp.route('/login', methods=['POST'])
@rate_limit(limit=5, window=60)  # 5 attempts per minute
def login():
    # ... existing code
```

#### 5. **Fix CORS for Environment Variables**
```python
# In backend/config.py
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
# .env
CORS_ORIGINS=https://your-domain.com,https://admin.your-domain.com
```

#### 6. **Add CSRF Protection**
```bash
pip install flask-wtf
```

Update `backend/app.py`:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)
```

#### 7. **Implement Secrets Management**
```python
# backend/config.py - Generate strong keys
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set in .env")
```

---

### SHORT-TERM ACTIONS (Within 1 week)

#### 1. **Add Request Validation**
```python
# Create backend/validators.py
from wtforms import ValidationError
import re

def validate_password_strength(password):
    """Enforce strong passwords"""
    if len(password) < 12:
        raise ValidationError("Password must be at least 12 characters")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain uppercase letter")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain number")
    if not any(char in "!@#$%^&*" for char in password):
        raise ValidationError("Password must contain special character")
    return True
```

#### 2. **Implement API Key Rotation**
```python
# Add to models.py
class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    key_hash = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
```

#### 3. **Add Security Headers**
```python
# Update backend/app.py
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

#### 4. **Implement IP Whitelisting**
```python
# backend/config.py
ADMIN_IP_WHITELIST = os.getenv('ADMIN_IP_WHITELIST', '').split(',')

# backend/utils.py
def ip_whitelist_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.remote_addr not in current_app.config.get('ADMIN_IP_WHITELIST', []):
            log_audit(None, 'unauthorized_ip_access', request.remote_addr, 'failure')
            return jsonify({'error': 'Access denied'}), 403
        return fn(*args, **kwargs)
    return wrapper
```

#### 5. **Add 2FA Support**
```bash
pip install pyotp qrcode
```

```python
# Update models.py
class User(db.Model):
    # ... existing fields ...
    two_fa_enabled = db.Column(db.Boolean, default=False)
    two_fa_secret = db.Column(db.String(32))
```

#### 6. **Implement Session Management**
```python
# Update config.py
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
```

#### 7. **Add Intrusion Detection**
```python
# backend/security.py
def check_suspicious_activity(user_id, action, ip_address):
    """Check for suspicious patterns"""
    # Check for multiple failed logins
    failed_logins = AuditLog.query.filter(
        AuditLog.user_id == user_id,
        AuditLog.action == 'login_failed',
        AuditLog.timestamp > datetime.utcnow() - timedelta(minutes=15)
    ).count()
    
    if failed_logins > 5:
        # Lock account
        user = User.query.get(user_id)
        user.is_active = False
        db.session.commit()
        # Alert admin
        logger.warning(f"User {user_id} locked due to suspicious activity")
```

---

### LONG-TERM ACTIONS (1-3 months)

#### 1. **Implement Web Application Firewall (WAF)**
```bash
# Install ModSecurity
apt-get install libmodsecurity3 libmodsecurity-dev

# Configure in Nginx
location /api {
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/modsecurity.conf;
}
```

#### 2. **Setup Security Monitoring**
```bash
pip install python-json-logger

# In logging config
json_handler = logging.FileHandler('security.json')
json_handler.setFormatter(JsonFormatter())
security_logger.addHandler(json_handler)
```

#### 3. **Database Encryption**
```python
# For PostgreSQL in production
CREATE EXTENSION pgcrypto;

# Encrypt sensitive fields
ALTER TABLE audit_logs ADD COLUMN encrypted_details 
    bytea DEFAULT pgp_sym_encrypt('', 'your-key');
```

#### 4. **Implement Vault for Secrets**
```bash
# Use HashiCorp Vault
vault kv put secret/seedbox/plex \
  url="http://localhost:32400" \
  token="your_token"

# In Python
from hvac import Client
client = Client(url='http://vault:8200')
secrets = client.secrets.kv.read_secret_version('seedbox/plex')
```

#### 5. **Security Scanning in CI/CD**
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Bandit
        run: pip install bandit && bandit -r backend/
      - name: Run Safety
        run: pip install safety && safety check
      - name: SAST with Semgrep
        run: semgrep --config=p/security-audit backend/
```

#### 6. **Regular Penetration Testing**
- Schedule quarterly pen tests
- Test for OWASP Top 10 vulnerabilities
- Review third-party component vulnerabilities

#### 7. **Implement OAuth 2.0/OpenID Connect**
```bash
pip install authlib

# Allow SSO via providers (Google, GitHub, etc)
```

---

## 🛡️ Security Hardening Checklist

### Before Deployment
- [ ] Change all default credentials
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY (32+ characters)
- [ ] Set CORS to specific domains only
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall rules
- [ ] Set strong database password
- [ ] Enable database backups with encryption
- [ ] Review all environment variables
- [ ] Disable debug mode in production
- [ ] Setup log aggregation

### After Deployment
- [ ] Monitor audit logs daily
- [ ] Review failed login attempts
- [ ] Check for unauthorized API access
- [ ] Monitor resource usage
- [ ] Track database growth
- [ ] Test backup restoration
- [ ] Review security headers
- [ ] Check SSL certificate expiry

### Ongoing (Monthly)
- [ ] Update dependencies
- [ ] Review access logs
- [ ] Audit user permissions
- [ ] Check for inactive accounts
- [ ] Review password age
- [ ] Test incident response
- [ ] Security awareness training
- [ ] Vulnerability scanning

---

## 🔐 Network Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Internet                            │
└──────────────────────────┬──────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Cloudflare  │ (DDoS Protection)
                    │    WAF      │
                    └──────┬──────┘
                           │
                    ┌──────▼──────────────────┐
                    │   Nginx Reverse Proxy   │
                    │  (SSL/TLS Termination)  │
                    │  (Rate Limiting)        │
                    │  (IP Filtering)         │
                    └──────┬──────────────────┘
                           │
                    ┌──────▼──────────────────┐
                    │  Flask Application      │
                    │  (JWT Auth)             │
                    │  (CORS Limited)         │
                    │  (Security Headers)     │
                    └──────┬──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐    ┌────────▼────────┐   ┌────▼────┐
   │ Database │    │ Service APIs    │   │ Logging │
   │(Encrypted)   │ (HTTPS Calls)   │   │(Secured)│
   └──────────┘    └─────────────────┘   └─────────┘
```

---

## 🚨 Incident Response Plan

### If Credentials Compromised
1. Immediately invalidate compromised tokens
2. Force password reset for affected users
3. Review audit logs for unauthorized access
4. Rotate API keys for all services
5. Enable enhanced monitoring
6. Notify all users
7. Review and patch vulnerability

### If Database Breached
1. Take system offline
2. Preserve forensic evidence
3. Restore from clean backup
4. Audit all data
5. Notify affected users
6. Review incident logs
7. Implement additional controls

### If API Key Leaked
1. Revoke compromised key immediately
2. Generate new key
3. Update configuration
4. Restart services
5. Monitor for misuse
6. Review logs for unauthorized access
7. Consider IP-based restrictions

---

## 📋 Compliance Considerations

### GDPR (Europe)
- ✅ Audit logging (6+ months retention)
- ✅ Data encryption
- ❌ User data export (NOT implemented)
- ❌ Right to deletion (NOT implemented)
- ⚠️ Consent management (consider implementing)

### HIPAA (Healthcare)
- ✅ Access controls
- ✅ Audit logs
- ❌ Encryption at rest (NOT implemented)
- ❌ Disaster recovery (OPTIONAL)

### SOC 2 Type II
- ✅ User access controls
- ✅ Audit trail
- ✅ Error handling
- ❌ Incident response (NEEDS policy)
- ⚠️ Change management (NEEDS process)

---

## 🔍 Security Testing

### Manual Testing
```bash
# Test CORS
curl -H "Origin: http://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  http://localhost:5000/api/system/stats

# Test HTTPS enforcement
curl -i http://localhost:5000/api/auth/login

# Test rate limiting
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"wrong"}'
done

# Test SQL injection
curl "http://localhost:5000/api/auth/login?username=admin' OR '1'='1"

# Test XSS
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"<script>alert(1)</script>","password":"test","email":"test@test.com"}'
```

### Automated Testing Tools
```bash
# OWASP ZAP
owasp-zap-full-scan.py -t http://localhost:5000 -r zap-report.html

# Bandit (Python security linter)
bandit -r backend/ -f json -o bandit-report.json

# Safety (Dependency checker)
safety check --json

# Semgrep (Static analysis)
semgrep --config=p/security-audit backend/
```

---

## 📞 Security Resources

### Key Tools
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Flask-Talisman**: https://github.com/alisaifee/flask-talisman
- **Flask-Limiter**: https://flask-limiter.readthedocs.io/
- **pytest-flask**: https://pytest-flask.readthedocs.io/

### Reading
- OWASP Flask Security: https://owasp.org/www-community/attacks/csrf
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- Python Security: https://python-patterns.guide/#security

---

## 🎯 Priority Fix Schedule

### Week 1 (CRITICAL)
- [ ] Fix CORS configuration
- [ ] Enable HTTPS
- [ ] Change default credentials
- [ ] Add rate limiting

### Week 2 (HIGH)
- [ ] Add security headers
- [ ] Implement CSRF protection
- [ ] Add input validation

### Week 3-4 (MEDIUM)
- [ ] Setup IP whitelisting
- [ ] Implement 2FA
- [ ] Add intrusion detection

### Month 2-3 (LONG-TERM)
- [ ] WAF implementation
- [ ] Security monitoring
- [ ] Database encryption
- [ ] Vault integration

---

**Current Status**: ✅ Moderately Secure (Development Ready)  
**Production Ready**: ❌ NOT YET (Requires fixes above)  
**Risk Level**: 🔴 MEDIUM-HIGH (Must address immediately before production)  

Implement at least the CRITICAL and HIGH priority items before deploying to production.
