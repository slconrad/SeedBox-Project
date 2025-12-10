"""
Tautulli (Plex Monitoring) routes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from tautulli_service import TautulliService
from utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('tautulli', __name__, url_prefix='/api/tautulli')

tautulli_service = None


def get_tautulli_service():
    """Get or create Tautulli service instance"""
    global tautulli_service
    if tautulli_service is None:
        tautulli_service = TautulliService(
            current_app.config.get('TAUTULLI_URL'),
            current_app.config.get('TAUTULLI_API_KEY')
        )
    return tautulli_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all tautulli routes"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Check Tautulli health"""
    tautulli = get_tautulli_service()
    is_connected = tautulli.is_connected()
    
    return jsonify({
        'status': 'ok' if is_connected else 'error',
        'connected': is_connected
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Get Tautulli and Plex server status"""
    tautulli = get_tautulli_service()
    status = tautulli.get_server_status()
    
    return jsonify(status), 200


@bp.route('/activity', methods=['GET'])
@handle_errors
def get_activity():
    """Get current Plex activity"""
    tautulli = get_tautulli_service()
    activity = tautulli.get_activity()
    
    return jsonify(activity), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def get_stats():
    """Get Tautulli statistics"""
    tautulli = get_tautulli_service()
    stats = tautulli.get_stats()
    
    return jsonify(stats), 200


@bp.route('/users', methods=['GET'])
@handle_errors
def list_users():
    """Get Plex users"""
    tautulli = get_tautulli_service()
    users = tautulli.get_users()
    
    return jsonify({
        'users': users,
        'count': len(users)
    }), 200


@bp.route('/libraries', methods=['GET'])
@handle_errors
def library_stats():
    """Get library statistics from Tautulli"""
    tautulli = get_tautulli_service()
    libraries = tautulli.get_library_stats()
    
    return jsonify({
        'libraries': libraries,
        'count': len(libraries)
    }), 200


@bp.route('/history', methods=['GET'])
@handle_errors
def get_history():
    """Get playback history"""
    count = request.args.get('count', 50, type=int)
    tautulli = get_tautulli_service()
    history = tautulli.get_history(count)
    
    return jsonify({
        'history': history,
        'count': len(history)
    }), 200


@bp.route('/server-info', methods=['GET'])
@handle_errors
def server_info():
    """Get Plex server information"""
    tautulli = get_tautulli_service()
    info = tautulli.get_server_info()
    
    return jsonify(info), 200


@bp.route('/restart', methods=['POST'])
@handle_errors
def restart_tautulli():
    """Restart Tautulli service"""
    tautulli = get_tautulli_service()
    success = tautulli.restart_tautulli()
    
    log_audit('restart_tautulli', 'Tautulli', 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Tautulli restart initiated' if success else 'Failed to restart Tautulli'
    }), 200 if success else 400
