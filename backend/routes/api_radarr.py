"""
Radarr integration routes
Phase 5: 'RR' stack API integrations
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..services.radarr_service import RadarrService
from ..models import AppConfig, MediaLibrary, db
from ..utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('radarr', __name__, url_prefix='/api/radarr')

radarr_service = None


def get_radarr_service():
    """Get or create Radarr service instance"""
    global radarr_service
    if radarr_service is None:
        radarr_service = RadarrService(
            current_app.config.get('RADARR_URL'),
            current_app.config.get('RADARR_API_KEY')
        )
    return radarr_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health():
    """Check Radarr health"""
    radarr = get_radarr_service()
    is_connected = radarr.is_connected()
    
    return jsonify({
        'connected': is_connected,
        'status': 'ok' if is_connected else 'error',
        'url': current_app.config.get('RADARR_URL')
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def status():
    """Get Radarr status"""
    radarr = get_radarr_service()
    status_data = radarr.get_status()
    return jsonify(status_data), 200


@bp.route('/movies', methods=['GET'])
@handle_errors
def movies():
    """Get movies from library"""
    radarr = get_radarr_service()
    limit = request.args.get('limit', 100, type=int)
    movies_list = radarr.get_movies(limit=limit)
    
    return jsonify({
        'movies': movies_list,
        'count': len(movies_list)
    }), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def stats():
    """Get Radarr statistics"""
    radarr = get_radarr_service()
    stats_data = radarr.get_movie_stats()
    return jsonify(stats_data), 200


@bp.route('/upcoming', methods=['GET'])
@handle_errors
def upcoming():
    """Get upcoming releases"""
    radarr = get_radarr_service()
    days = request.args.get('days', 7, type=int)
    upcoming_list = radarr.get_upcoming(days=days)
    
    return jsonify({
        'upcoming': upcoming_list,
        'count': len(upcoming_list)
    }), 200


@bp.route('/queue', methods=['GET'])
@handle_errors
def queue():
    """Get download queue"""
    radarr = get_radarr_service()
    queue_list = radarr.get_queue()
    
    return jsonify({
        'queue': queue_list,
        'count': len(queue_list)
    }), 200


@bp.route('/history', methods=['GET'])
@handle_errors
def history():
    """Get recent history"""
    radarr = get_radarr_service()
    limit = request.args.get('limit', 50, type=int)
    history_list = radarr.get_history(limit=limit)
    
    return jsonify({
        'history': history_list,
        'count': len(history_list)
    }), 200


@bp.route('/search/<int:movie_id>', methods=['POST'])
@handle_errors
def search(movie_id):
    """Trigger search for a movie"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    radarr = get_radarr_service()
    result = radarr.trigger_search([movie_id])
    
    if result:
        log_audit(user_id, 'radarr_search_triggered', request.remote_addr, 'success', 
                 target=f'movie_{movie_id}')
        return jsonify({'message': 'Search triggered'}), 200
    else:
        log_audit(user_id, 'radarr_search_failed', request.remote_addr, 'failure', 
                 target=f'movie_{movie_id}')
        return jsonify({'error': 'Failed to trigger search'}), 500


@bp.route('/config', methods=['GET'])
@handle_errors
def config():
    """Get Radarr configuration"""
    radarr = get_radarr_service()
    config_data = radarr.get_config()
    return jsonify(config_data), 200
