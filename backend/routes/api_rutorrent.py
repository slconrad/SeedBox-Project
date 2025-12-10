"""
ruTorrent routes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..services.rutorrent_service import RuTorrentService
from ..utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('rutorrent', __name__, url_prefix='/api/rutorrent')

rutorrent_service = None


def get_rutorrent_service():
    """Get or create ruTorrent service instance"""
    global rutorrent_service
    if rutorrent_service is None:
        rutorrent_service = RuTorrentService(
            current_app.config.get('RUTORRENT_URL'),
            current_app.config.get('RUTORRENT_USERNAME'),
            current_app.config.get('RUTORRENT_PASSWORD')
        )
    return rutorrent_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all rutorrent routes"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Check ruTorrent health"""
    rutorrent = get_rutorrent_service()
    is_connected = rutorrent.is_connected()
    
    return jsonify({
        'status': 'ok' if is_connected else 'error',
        'connected': is_connected
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Get ruTorrent server status"""
    rutorrent = get_rutorrent_service()
    status = rutorrent.get_server_status()
    
    return jsonify(status), 200


@bp.route('/torrents', methods=['GET'])
@handle_errors
def list_torrents():
    """Get all torrents"""
    rutorrent = get_rutorrent_service()
    torrents = rutorrent.get_torrents()
    
    return jsonify({
        'torrents': torrents,
        'count': len(torrents)
    }), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def get_stats():
    """Get torrent statistics"""
    rutorrent = get_rutorrent_service()
    stats = rutorrent.get_torrent_stats()
    
    return jsonify(stats), 200


@bp.route('/bandwidth', methods=['GET'])
@handle_errors
def bandwidth_stats():
    """Get bandwidth statistics"""
    rutorrent = get_rutorrent_service()
    bandwidth = rutorrent.get_bandwidth_stats()
    
    return jsonify(bandwidth), 200


@bp.route('/torrents/<hash_id>/start', methods=['POST'])
@handle_errors
def start_torrent(hash_id):
    """Start a torrent"""
    rutorrent = get_rutorrent_service()
    success = rutorrent.start_torrent(hash_id)
    
    log_audit('start_rutorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent started' if success else 'Failed to start torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/stop', methods=['POST'])
@handle_errors
def stop_torrent(hash_id):
    """Stop a torrent"""
    rutorrent = get_rutorrent_service()
    success = rutorrent.stop_torrent(hash_id)
    
    log_audit('stop_rutorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent stopped' if success else 'Failed to stop torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/pause', methods=['POST'])
@handle_errors
def pause_torrent(hash_id):
    """Pause a torrent"""
    rutorrent = get_rutorrent_service()
    success = rutorrent.pause_torrent(hash_id)
    
    log_audit('pause_rutorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent paused' if success else 'Failed to pause torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/resume', methods=['POST'])
@handle_errors
def resume_torrent(hash_id):
    """Resume a torrent"""
    rutorrent = get_rutorrent_service()
    success = rutorrent.resume_torrent(hash_id)
    
    log_audit('resume_rutorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent resumed' if success else 'Failed to resume torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/remove', methods=['POST'])
@handle_errors
def remove_torrent(hash_id):
    """Remove a torrent"""
    delete_files = request.json.get('delete_files', False) if request.json else False
    rutorrent = get_rutorrent_service()
    success = rutorrent.remove_torrent(hash_id, delete_files)
    
    log_audit('remove_rutorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent removed' if success else 'Failed to remove torrent'
    }), 200 if success else 400


@bp.route('/restart', methods=['POST'])
@handle_errors
def restart_rtorrent():
    """Restart rtorrent daemon"""
    rutorrent = get_rutorrent_service()
    success = rutorrent.restart_rtorrent()
    
    log_audit('restart_rtorrent', 'rtorrent daemon', 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'rtorrent restart initiated' if success else 'Failed to restart rtorrent'
    }), 200 if success else 400
