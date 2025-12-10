"""
Backend package initialization
"""
from models import db
from config import config

__version__ = '1.0.0'
__all__ = ['db', 'config']
