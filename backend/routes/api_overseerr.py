"""
Overseerr integration routes
Phase 5: 'RR' stack API integrations
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from overseerr_service import OverseerrService
from utils import handle_errors, log_audit
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('overseerr', __name__, url_prefix='/api/overseerr')

overseerr_service = None


def get_overseerr_service():
    """Get or create Overseerr service instance"""
    global overseerr_service
    if overseerr_service is None:
        overseerr_service = OverseerrService(
            current_app.config.get('OVERSEERR_URL'),
            current_app.config.get('OVERSEERR_API_KEY')
        )
    return overseerr_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication"""
    pass


@bp.route('/health', methods=['GET'])
@handle_errors
def health():
    """Check Overseerr health"""
    overseerr = get_overseerr_service()
    is_connected = overseerr.is_connected()
    
    return jsonify({
        'connected': is_connected,
        'status': 'ok' if is_connected else 'error',
        'url': current_app.config.get('OVERSEERR_URL')
    }), 200


@bp.route('/status', methods=['GET'])
@handle_errors
def status():
    """Get Overseerr status"""
    overseerr = get_overseerr_service()
    status_data = overseerr.get_status()
    return jsonify(status_data), 200


@bp.route('/requests', methods=['GET'])
@handle_errors
def requests_list():
    """Get media requests"""
    overseerr = get_overseerr_service()
    status = request.args.get('status', 'all')
    limit = request.args.get('limit', 50, type=int)
    
    requests = overseerr.get_requests(status=status, limit=limit)
    
    return jsonify({
        'requests': requests,
        'count': len(requests),
        'status_filter': status
    }), 200


@bp.route('/stats', methods=['GET'])
@handle_errors
def stats():
    """Get Overseerr statistics"""
    overseerr = get_overseerr_service()
    stats_data = overseerr.get_request_stats()
    return jsonify(stats_data), 200


@bp.route('/users', methods=['GET'])
@handle_errors
def users():
    """Get Overseerr users"""
    overseerr = get_overseerr_service()
    limit = request.args.get('limit', 100, type=int)
    
    users_list = overseerr.get_users(limit=limit)
    
    return jsonify({
        'users': users_list,
        'count': len(users_list)
    }), 200


@bp.route('/requests/<int:request_id>/approve', methods=['POST'])
@handle_errors
def approve_request(request_id):
    """Approve a request"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    is_4k = data.get('is_4k', False)
    
    overseerr = get_overseerr_service()
    result = overseerr.approve_request(request_id, is_4k=is_4k)
    
    if result:
        log_audit(user_id, 'request_approved', request.remote_addr, 'success', 
                 target=f'overseerr_request_{request_id}')
        return jsonify({'message': 'Request approved'}), 200
    else:
        log_audit(user_id, 'request_approval_failed', request.remote_addr, 'failure', 
                 target=f'overseerr_request_{request_id}')
        return jsonify({'error': 'Failed to approve request'}), 500


@bp.route('/requests/<int:request_id>/decline', methods=['POST'])
@handle_errors
def decline_request(request_id):
    """Decline a request"""
    user_id = get_jwt_identity()
    
    overseerr = get_overseerr_service()
    result = overseerr.decline_request(request_id)
    
    if result:
        log_audit(user_id, 'request_declined', request.remote_addr, 'success', 
                 target=f'overseerr_request_{request_id}')
        return jsonify({'message': 'Request declined'}), 200
    else:
        log_audit(user_id, 'request_decline_failed', request.remote_addr, 'failure', 
                 target=f'overseerr_request_{request_id}')
        return jsonify({'error': 'Failed to decline request'}), 500


@bp.route('/settings', methods=['GET'])
@handle_errors
def settings():
    """Get Overseerr settings"""
    overseerr = get_overseerr_service()
    settings_data = overseerr.get_settings()
    return jsonify(settings_data), 200
