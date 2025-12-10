"""
Plex Media Server routes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..services.plex_service import PlexService
from ..utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('plex', __name__, url_prefix='/api/plex')

plex_service = None


def get_plex_service():
    """Get or create Plex service instance"""
    global plex_service
    if plex_service is None:
        plex_service = PlexService(
            current_app.config.get('PLEX_URL'),
            current_app.config.get('PLEX_TOKEN')
        )
    return plex_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all plex routes"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Check Plex server health"""
    plex = get_plex_service()
    is_connected = plex.is_connected()
    
    return jsonify({
        'status': 'ok' if is_connected else 'error',
        'connected': is_connected
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Get Plex server status"""
    plex = get_plex_service()
    status = plex.get_server_status()
    
    return jsonify(status), 200


@bp.route('/libraries', methods=['GET'])
@handle_errors
def list_libraries():
    """Get all libraries"""
    plex = get_plex_service()
    libraries = plex.get_libraries()
    
    return jsonify({
        'libraries': libraries,
        'count': len(libraries)
    }), 200


@bp.route('/libraries/<lib_key>/stats', methods=['GET'])
@handle_errors
def library_stats(lib_key):
    """Get library statistics"""
    plex = get_plex_service()
    stats = plex.get_library_stats(lib_key)
    
    return jsonify(stats), 200


@bp.route('/sessions', methods=['GET'])
@handle_errors
def active_sessions():
    """Get active streaming sessions"""
    plex = get_plex_service()
    sessions = plex.get_active_sessions()
    
    return jsonify({
        'sessions': sessions,
        'count': len(sessions)
    }), 200


@bp.route('/streams', methods=['GET'])
@handle_errors
def recent_streams():
    """Get recent stream history"""
    count = request.args.get('count', 10, type=int)
    plex = get_plex_service()
    streams = plex.get_recent_streams(count)
    
    return jsonify({
        'streams': streams,
        'count': len(streams)
    }), 200


@bp.route('/restart', methods=['POST'])
@handle_errors
def restart_server():
    """Restart Plex server"""
    plex = get_plex_service()
    success = plex.restart_server()
    
    log_audit('restart_plex', 'Plex Server', 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Plex server restart initiated' if success else 'Failed to restart Plex server'
    }), 200 if success else 400


@bp.route('/optimize', methods=['POST'])
@handle_errors
def optimize_database():
    """Optimize Plex database"""
    plex = get_plex_service()
    success = plex.optimize_database()
    
    log_audit('optimize_plex', 'Plex Database', 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Database optimization started' if success else 'Failed to optimize database'
    }), 200 if success else 400


@bp.route('/libraries/<lib_key>/scan', methods=['POST'])
@handle_errors
def scan_library(lib_key):
    """Trigger library scan"""
    plex = get_plex_service()
    success = plex.perform_library_scan(lib_key)
    
    log_audit('scan_plex_library', f'Library {lib_key}', 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': f'Library scan started' if success else 'Failed to start library scan'
    }), 200 if success else 400
