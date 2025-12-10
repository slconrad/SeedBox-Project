"""
System monitoring routes
Phase 1 & 4: System stats and WebSocket real-time updates
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..services.system_service import SystemService
from ..models import SystemMetric, ContainerMetric, db
from ..utils import handle_errors
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('system', __name__, url_prefix='/api/system')


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all system routes"""
    pass


@bp.route('/stats', methods=['GET'])
@handle_errors
def get_stats():
    """Get current system statistics"""
    stats = SystemService.get_system_stats()
    
    # Store metric in database for historical tracking
    try:
        metric = SystemMetric(
            cpu_percent=stats['cpu']['percent'],
            memory_percent=stats['memory']['percent'],
            memory_used=stats['memory']['used'],
            memory_total=stats['memory']['total'],
            disk_percent=stats['disk']['percent'],
            disk_used=stats['disk']['used'],
            disk_total=stats['disk']['total'],
            uptime_seconds=stats['uptime']['seconds']
        )
        db.session.add(metric)
        db.session.commit()
    except Exception as e:
        logger.warning(f"Could not store metric: {e}")
    
    return jsonify(stats), 200


@bp.route('/cpu', methods=['GET'])
@handle_errors
def get_cpu():
    """Get detailed CPU information"""
    cpu_stats = SystemService.get_cpu_stats()
    return jsonify(cpu_stats), 200


@bp.route('/memory', methods=['GET'])
@handle_errors
def get_memory():
    """Get detailed memory information"""
    memory_stats = SystemService.get_memory_stats()
    return jsonify(memory_stats), 200


@bp.route('/disk', methods=['GET'])
@handle_errors
def get_disk():
    """Get disk statistics"""
    path = request.args.get('path', '/')
    disk_stats = SystemService.get_disk_stats(path)
    return jsonify(disk_stats), 200


@bp.route('/network', methods=['GET'])
@handle_errors
def get_network():
    """Get network statistics"""
    network_stats = SystemService.get_network_stats()
    return jsonify(network_stats), 200


@bp.route('/processes', methods=['GET'])
@handle_errors
def get_processes():
    """Get top processes by memory"""
    limit = request.args.get('limit', 10, type=int)
    processes = SystemService.get_process_list(limit)
    return jsonify({'processes': processes}), 200


@bp.route('/sensors', methods=['GET'])
@handle_errors
def get_sensors():
    """Get sensor information (temperature, fans)"""
    sensors = SystemService.get_sensor_stats()
    return jsonify(sensors), 200


@bp.route('/history', methods=['GET'])
@handle_errors
def get_history():
    """Get historical metrics"""
    hours = request.args.get('hours', 24, type=int)
    limit = request.args.get('limit', 288, type=int)
    
    from datetime import datetime, timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    metrics = SystemMetric.query.filter(
        SystemMetric.timestamp >= cutoff_time
    ).order_by(SystemMetric.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'metrics': [m.to_dict() for m in reversed(metrics)]
    }), 200
