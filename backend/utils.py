"""
Utility decorators and helpers
"""
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User, AuditLog, db
import logging

logger = logging.getLogger(__name__)


def jwt_required_custom(roles: list = None):
    """Custom JWT decorator with role checking"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            if roles and user.role not in roles:
                log_audit(user_id, f'unauthorized_access_{request.endpoint}', request.remote_addr, 'failure')
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    """Decorator for admin-only endpoints"""
    return jwt_required_custom(roles=['admin'])(fn)


def log_audit(user_id: int, action: str, ip_address: str, status: str = 'success', 
              target: str = None, details: dict = None, error_message: str = None):
    """Log an audit trail entry"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            target=target,
            details=details,
            status=status,
            error_message=error_message,
            ip_address=ip_address
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error logging audit: {e}")


def handle_errors(fn):
    """Decorator to handle common errors"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': f'Invalid input: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Error in {fn.__name__}: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper


def rate_limit(limit: int = 100, window: int = 60):
    """Simple rate limiting decorator"""
    def decorator(fn):
        requests_dict = {}
        
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            current_time = int(time.time() / window)
            key = f"{ip}:{current_time}"
            
            requests_dict[key] = requests_dict.get(key, 0) + 1
            
            if requests_dict[key] > limit:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
