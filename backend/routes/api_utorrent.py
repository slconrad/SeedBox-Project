"""
uTorrent routes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..services.utorrent_service import UTorrentService
from ..utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('utorrent', __name__, url_prefix='/api/utorrent')

utorrent_service = None


def get_utorrent_service():
    """Get or create uTorrent service instance"""
    global utorrent_service
    if utorrent_service is None:
        utorrent_service = UTorrentService(
            current_app.config.get('UTORRENT_URL'),
            current_app.config.get('UTORRENT_USERNAME'),
            current_app.config.get('UTORRENT_PASSWORD')
        )
    return utorrent_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all utorrent routes"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Check uTorrent health"""
    utorrent = get_utorrent_service()
    is_connected = utorrent.is_connected()
    
    return jsonify({
        'status': 'ok' if is_connected else 'error',
        'connected': is_connected
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Get uTorrent server status"""
    utorrent = get_utorrent_service()
    status = utorrent.get_server_status()
    
    return jsonify(status), 200


@bp.route('/torrents', methods=['GET'])
@handle_errors
def list_torrents():
    """Get all torrents"""
    utorrent = get_utorrent_service()
    torrents = utorrent.get_torrents()
    
    return jsonify({
        'torrents': torrents,
        'count': len(torrents)
    }), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def get_stats():
    """Get torrent statistics"""
    utorrent = get_utorrent_service()
    stats = utorrent.get_torrent_stats()
    
    return jsonify(stats), 200


@bp.route('/bandwidth', methods=['GET'])
@handle_errors
def bandwidth_stats():
    """Get bandwidth statistics"""
    utorrent = get_utorrent_service()
    bandwidth = utorrent.get_bandwidth_stats()
    
    return jsonify(bandwidth), 200


@bp.route('/torrents/<hash_id>/start', methods=['POST'])
@handle_errors
def start_torrent(hash_id):
    """Start a torrent"""
    utorrent = get_utorrent_service()
    success = utorrent.start_torrent(hash_id)
    
    log_audit('start_utorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent started' if success else 'Failed to start torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/stop', methods=['POST'])
@handle_errors
def stop_torrent(hash_id):
    """Stop a torrent"""
    utorrent = get_utorrent_service()
    success = utorrent.stop_torrent(hash_id)
    
    log_audit('stop_utorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent stopped' if success else 'Failed to stop torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/pause', methods=['POST'])
@handle_errors
def pause_torrent(hash_id):
    """Pause a torrent"""
    utorrent = get_utorrent_service()
    success = utorrent.pause_torrent(hash_id)
    
    log_audit('pause_utorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent paused' if success else 'Failed to pause torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/resume', methods=['POST'])
@handle_errors
def resume_torrent(hash_id):
    """Resume a torrent"""
    utorrent = get_utorrent_service()
    success = utorrent.resume_torrent(hash_id)
    
    log_audit('resume_utorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent resumed' if success else 'Failed to resume torrent'
    }), 200 if success else 400


@bp.route('/torrents/<hash_id>/remove', methods=['POST'])
@handle_errors
def remove_torrent(hash_id):
    """Remove a torrent"""
    delete_files = request.json.get('delete_files', False) if request.json else False
    utorrent = get_utorrent_service()
    success = utorrent.remove_torrent(hash_id, delete_files)
    
    log_audit('remove_utorrent_torrent', hash_id, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent removed' if success else 'Failed to remove torrent'
    }), 200 if success else 400


@bp.route('/torrents/add-url', methods=['POST'])
@handle_errors
def add_torrent_url():
    """Add torrent from URL"""
    data = request.get_json() or {}
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    utorrent = get_utorrent_service()
    success = utorrent.add_torrent_url(url)
    
    log_audit('add_utorrent_torrent', url, 'success' if success else 'failure')
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Torrent added' if success else 'Failed to add torrent'
    }), 200 if success else 400
