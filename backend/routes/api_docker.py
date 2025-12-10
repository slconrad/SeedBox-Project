"""
Docker management routes
Phase 1: Docker integration
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from docker_service import DockerService
from models import AuditLog, db
from utils import log_audit, handle_errors
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('docker', __name__, url_prefix='/api/docker')

# Initialize Docker service
docker_service = None


def get_docker_service():
    """Get or create Docker service instance"""
    global docker_service
    if docker_service is None:
        docker_service = DockerService(current_app.config.get('DOCKER_HOST'))
    return docker_service


@bp.before_request
@jwt_required()
def require_auth():
    """Require authentication for all docker routes"""
    pass


@bp.route('/status', methods=['GET'])
@handle_errors
def docker_status():
    """Check Docker daemon status"""
    docker_svc = get_docker_service()
    is_connected = docker_svc.is_connected()
    
    return jsonify({
        'connected': is_connected,
        'status': 'ok' if is_connected else 'error'
    }), 200


@bp.route('/containers', methods=['GET'])
@handle_errors
def list_containers():
    """List all containers"""
    docker_svc = get_docker_service()
    all_containers = request.args.get('all', 'true').lower() == 'true'
    
    containers = docker_svc.get_containers(all=all_containers)
    
    return jsonify({
        'containers': containers,
        'count': len(containers)
    }), 200


@bp.route('/containers/<container_id>', methods=['GET'])
@handle_errors
def get_container(container_id):
    """Get specific container details"""
    docker_svc = get_docker_service()
    container = docker_svc.get_container(container_id)
    
    if not container:
        return jsonify({'error': 'Container not found'}), 404
    
    return jsonify(container), 200


@bp.route('/containers/<container_id>/start', methods=['POST'])
@handle_errors
def start_container(container_id):
    """Start a container"""
    user_id = get_jwt_identity()
    docker_svc = get_docker_service()
    
    try:
        docker_svc.start_container(container_id)
        log_audit(user_id, 'container_started', request.remote_addr, 'success', target=container_id)
        
        return jsonify({
            'message': f'Container {container_id} started',
            'container_id': container_id
        }), 200
    except Exception as e:
        log_audit(user_id, 'container_start_failed', request.remote_addr, 'failure', 
                 target=container_id, error_message=str(e))
        return jsonify({'error': str(e)}), 500


@bp.route('/containers/<container_id>/stop', methods=['POST'])
@handle_errors
def stop_container(container_id):
    """Stop a container"""
    user_id = get_jwt_identity()
    docker_svc = get_docker_service()
    data = request.get_json() or {}
    timeout = data.get('timeout', 10)
    
    try:
        docker_svc.stop_container(container_id, timeout=timeout)
        log_audit(user_id, 'container_stopped', request.remote_addr, 'success', target=container_id)
        
        return jsonify({
            'message': f'Container {container_id} stopped',
            'container_id': container_id
        }), 200
    except Exception as e:
        log_audit(user_id, 'container_stop_failed', request.remote_addr, 'failure', 
                 target=container_id, error_message=str(e))
        return jsonify({'error': str(e)}), 500


@bp.route('/containers/<container_id>/restart', methods=['POST'])
@handle_errors
def restart_container(container_id):
    """Restart a container"""
    user_id = get_jwt_identity()
    docker_svc = get_docker_service()
    data = request.get_json() or {}
    timeout = data.get('timeout', 10)
    
    try:
        docker_svc.restart_container(container_id, timeout=timeout)
        log_audit(user_id, 'container_restarted', request.remote_addr, 'success', target=container_id)
        
        return jsonify({
            'message': f'Container {container_id} restarted',
            'container_id': container_id
        }), 200
    except Exception as e:
        log_audit(user_id, 'container_restart_failed', request.remote_addr, 'failure', 
                 target=container_id, error_message=str(e))
        return jsonify({'error': str(e)}), 500


@bp.route('/containers/<container_id>/logs', methods=['GET'])
@handle_errors
def get_logs(container_id):
    """Get container logs"""
    docker_svc = get_docker_service()
    tail = request.args.get('tail', 100, type=int)
    timestamps = request.args.get('timestamps', 'true').lower() == 'true'
    
    logs = docker_svc.get_container_logs(container_id, tail=tail, timestamps=timestamps)
    
    return jsonify({
        'container_id': container_id,
        'logs': logs.split('\n') if logs else []
    }), 200


@bp.route('/networks', methods=['GET'])
@handle_errors
def list_networks():
    """List Docker networks"""
    docker_svc = get_docker_service()
    networks = docker_svc.get_networks()
    
    return jsonify({
        'networks': networks,
        'count': len(networks)
    }), 200


@bp.route('/volumes', methods=['GET'])
@handle_errors
def list_volumes():
    """List Docker volumes"""
    docker_svc = get_docker_service()
    volumes = docker_svc.get_volumes()
    
    return jsonify({
        'volumes': volumes,
        'count': len(volumes)
    }), 200
