"""
Database models for SeedBox Control Panel
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, moderator, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class UserPreference(db.Model):
    """User preferences storage"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'key', name='uq_user_preference'),)


class AppConfig(db.Model):
    """Application configuration storage"""
    __tablename__ = 'app_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(50), unique=True, nullable=False)  # radarr, sonarr, etc
    app_name = db.Column(db.String(100), nullable=False)
    config = db.Column(JSON)  # Store complex config as JSON
    is_enabled = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'app_id': self.app_id,
            'app_name': self.app_name,
            'config': self.config,
            'is_enabled': self.is_enabled,
            'last_updated': self.last_updated.isoformat()
        }


class ContainerMetric(db.Model):
    """Store container performance metrics"""
    __tablename__ = 'container_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String(100), nullable=False)
    container_name = db.Column(db.String(100), nullable=False)
    cpu_percent = db.Column(db.Float)  # 0-100
    memory_usage = db.Column(db.Integer)  # bytes
    memory_limit = db.Column(db.Integer)  # bytes
    network_in = db.Column(db.Integer)  # bytes
    network_out = db.Column(db.Integer)  # bytes
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'container_id': self.container_id,
            'container_name': self.container_name,
            'cpu_percent': self.cpu_percent,
            'memory_usage': self.memory_usage,
            'memory_limit': self.memory_limit,
            'network_in': self.network_in,
            'network_out': self.network_out,
            'timestamp': self.timestamp.isoformat()
        }


class SystemMetric(db.Model):
    """Store system-wide performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float)
    memory_percent = db.Column(db.Float)
    memory_used = db.Column(db.Integer)  # bytes
    memory_total = db.Column(db.Integer)  # bytes
    disk_percent = db.Column(db.Float)
    disk_used = db.Column(db.Integer)  # bytes
    disk_total = db.Column(db.Integer)  # bytes
    uptime_seconds = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_used': self.memory_used,
            'memory_total': self.memory_total,
            'disk_percent': self.disk_percent,
            'disk_used': self.disk_used,
            'disk_total': self.disk_total,
            'uptime_seconds': self.uptime_seconds,
            'timestamp': self.timestamp.isoformat()
        }


class AuditLog(db.Model):
    """Audit trail for admin actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # start_container, stop_container, etc
    target = db.Column(db.String(200))  # container name, user id, etc
    details = db.Column(JSON)  # Store additional context
    status = db.Column(db.String(20), default='success')  # success, failure
    error_message = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username if self.user else 'system',
            'action': self.action,
            'target': self.target,
            'details': self.details,
            'status': self.status,
            'error_message': self.error_message,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat()
        }


class MediaLibrary(db.Model):
    """Track media library information from Radarr/Sonarr"""
    __tablename__ = 'media_libraries'
    
    id = db.Column(db.Integer, primary_key=True)
    app_type = db.Column(db.String(20), nullable=False)  # radarr, sonarr
    remote_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer)
    status = db.Column(db.String(50))  # wanted, monitored, unmonitored, etc
    file_size = db.Column(db.Integer)  # bytes
    date_added = db.Column(db.DateTime)
    last_sync = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSON)  # Store additional info
    
    def to_dict(self):
        return {
            'id': self.id,
            'app_type': self.app_type,
            'title': self.title,
            'year': self.year,
            'status': self.status,
            'file_size': self.file_size,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'metadata': self.metadata
        }
