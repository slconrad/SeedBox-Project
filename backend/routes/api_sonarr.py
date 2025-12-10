"""
Sonarr integration routes
Phase 5: 'RR' stack API integrations
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sonarr_service import SonarrService
from models import AppConfig, db
from utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('sonarr', __name__, url_prefix='/api/sonarr')

sonarr_service = None


def get_sonarr_service():
    """Get or create Sonarr service instance"""
    global sonarr_service
    if sonarr_service is None:
        sonarr_service = SonarrService(
            current_app.config.get('SONARR_URL'),
            current_app.config.get('SONARR_API_KEY')
        )
    return sonarr_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health():
    """Check Sonarr health"""
    sonarr = get_sonarr_service()
    is_connected = sonarr.is_connected()
    
    return jsonify({
        'connected': is_connected,
        'status': 'ok' if is_connected else 'error',
        'url': current_app.config.get('SONARR_URL')
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def status():
    """Get Sonarr status"""
    sonarr = get_sonarr_service()
    status_data = sonarr.get_status()
    return jsonify(status_data), 200


@bp.route('/series', methods=['GET'])
@handle_errors
def series():
    """Get series from library"""
    sonarr = get_sonarr_service()
    limit = request.args.get('limit', 100, type=int)
    series_list = sonarr.get_series(limit=limit)
    
    return jsonify({
        'series': series_list,
        'count': len(series_list)
    }), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def stats():
    """Get Sonarr statistics"""
    sonarr = get_sonarr_service()
    stats_data = sonarr.get_series_stats()
    return jsonify(stats_data), 200


@bp.route('/calendar', methods=['GET'])
@handle_errors
def calendar():
    """Get upcoming episodes"""
    sonarr = get_sonarr_service()
    days = request.args.get('days', 7, type=int)
    calendar_list = sonarr.get_calendar(days=days)
    
    return jsonify({
        'calendar': calendar_list,
        'count': len(calendar_list)
    }), 200


@bp.route('/queue', methods=['GET'])
@handle_errors
def queue():
    """Get download queue"""
    sonarr = get_sonarr_service()
    queue_list = sonarr.get_queue()
    
    return jsonify({
        'queue': queue_list,
        'count': len(queue_list)
    }), 200


@bp.route('/wanted', methods=['GET'])
@handle_errors
def wanted():
    """Get wanted episodes"""
    sonarr = get_sonarr_service()
    wanted_list = sonarr.get_wanted()
    
    return jsonify({
        'wanted': wanted_list,
        'count': len(wanted_list)
    }), 200


@bp.route('/history', methods=['GET'])
@handle_errors
def history():
    """Get recent history"""
    sonarr = get_sonarr_service()
    limit = request.args.get('limit', 50, type=int)
    history_list = sonarr.get_history(limit=limit)
    
    return jsonify({
        'history': history_list,
        'count': len(history_list)
    }), 200


@bp.route('/search/<int:series_id>', methods=['POST'])
@handle_errors
def search(series_id):
    """Trigger search for a series"""
    user_id = get_jwt_identity()
    
    sonarr = get_sonarr_service()
    result = sonarr.trigger_search([series_id])
    
    if result:
        log_audit(user_id, 'sonarr_search_triggered', request.remote_addr, 'success', 
                 target=f'series_{series_id}')
        return jsonify({'message': 'Search triggered'}), 200
    else:
        log_audit(user_id, 'sonarr_search_failed', request.remote_addr, 'failure', 
                 target=f'series_{series_id}')
        return jsonify({'error': 'Failed to trigger search'}), 500


@bp.route('/config', methods=['GET'])
@handle_errors
def config():
    """Get Sonarr configuration"""
    sonarr = get_sonarr_service()
    config_data = sonarr.get_config()
    return jsonify(config_data), 200
