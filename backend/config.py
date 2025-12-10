"""
Configuration management for SeedBox Control Panel
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///seedbox.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Docker
    DOCKER_HOST = os.getenv('DOCKER_HOST', 'unix:///var/run/docker.sock')
    DOCKER_TIMEOUT = int(os.getenv('DOCKER_TIMEOUT', 30))
    
    # API endpoints for 'RR' stack
    RADARR_URL = os.getenv('RADARR_URL', 'http://localhost:7878')
    RADARR_API_KEY = os.getenv('RADARR_API_KEY', '')
    
    SONARR_URL = os.getenv('SONARR_URL', 'http://localhost:8989')
    SONARR_API_KEY = os.getenv('SONARR_API_KEY', '')
    
    PLEX_URL = os.getenv('PLEX_URL', 'http://localhost:32400')
    PLEX_TOKEN = os.getenv('PLEX_TOKEN', '')
    
    OVERSEERR_URL = os.getenv('OVERSEERR_URL', 'http://localhost:5055')
    OVERSEERR_API_KEY = os.getenv('OVERSEERR_API_KEY', '')
    
    # Plex Media Server
    PLEX_URL = os.getenv('PLEX_URL', 'http://localhost:32400')
    PLEX_TOKEN = os.getenv('PLEX_TOKEN', '')
    
    # Tautulli (Plex Monitoring)
    TAUTULLI_URL = os.getenv('TAUTULLI_URL', 'http://localhost:8181')
    TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY', '')
    
    # uTorrent
    UTORRENT_URL = os.getenv('UTORRENT_URL', 'http://localhost:8080')
    UTORRENT_USERNAME = os.getenv('UTORRENT_USERNAME', 'admin')
    UTORRENT_PASSWORD = os.getenv('UTORRENT_PASSWORD', '')
    
    # ruTorrent (rtorrent web interface)
    RUTORRENT_URL = os.getenv('RUTORRENT_URL', 'http://localhost:8081')
    RUTORRENT_USERNAME = os.getenv('RUTORRENT_USERNAME', '')
    RUTORRENT_PASSWORD = os.getenv('RUTORRENT_PASSWORD', '')
    
    # Features
    ENABLE_WEBSOCKET = os.getenv('ENABLE_WEBSOCKET', 'true').lower() == 'true'
    METRICS_RETENTION_DAYS = int(os.getenv('METRICS_RETENTION_DAYS', 30))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'seedbox.log')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///seedbox_dev.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, use strong secrets and proper database URL
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
