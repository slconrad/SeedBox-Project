"""
Docker service wrapper for container management
"""
import docker
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class DockerService:
    """Wrapper around Docker client for container management"""
    
    def __init__(self, docker_host: str = None):
        """Initialize Docker client"""
        try:
            if docker_host:
                self.client = docker.DockerClient(base_url=docker_host)
            else:
                self.client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if Docker daemon is accessible"""
        try:
            self.client.ping()
            return True
        except Exception as e:
            logger.error(f"Docker connection failed: {e}")
            return False
    
    def get_containers(self, all: bool = True) -> List[Dict]:
        """Get all containers with detailed info"""
        try:
            containers = self.client.containers.list(all=all)
            result = []
            
            for container in containers:
                try:
                    stats = container.stats(stream=False)
                    result.append(self._format_container(container, stats))
                except Exception as e:
                    logger.warning(f"Could not get stats for {container.name}: {e}")
                    result.append(self._format_container(container, None))
            
            return result
        except Exception as e:
            logger.error(f"Error getting containers: {e}")
            return []
    
    def get_container(self, container_id: str) -> Optional[Dict]:
        """Get specific container details"""
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            return self._format_container(container, stats)
        except Exception as e:
            logger.error(f"Error getting container {container_id}: {e}")
            return None
    
    def _format_container(self, container, stats=None) -> Dict:
        """Format container data for API response"""
        memory_stats = stats.get('memory_stats', {}) if stats else {}
        cpu_stats = stats.get('cpu_stats', {}) if stats else {}
        
        # Calculate CPU percentage
        cpu_percent = self._calculate_cpu_percent(stats) if stats else 0
        
        # Calculate memory percentage
        memory_limit = memory_stats.get('limit', 1)
        memory_usage = memory_stats.get('usage', 0)
        memory_percent = (memory_usage / memory_limit * 100) if memory_limit > 0 else 0
        
        return {
            'id': container.id[:12],
            'full_id': container.id,
            'name': container.name,
            'image': container.image.short_id if container.image else 'unknown',
            'status': container.status,
            'state': container.attrs.get('State', {}),
            'created': container.attrs.get('Created'),
            'started_at': container.attrs.get('State', {}).get('StartedAt'),
            'ports': self._format_ports(container.ports),
            'cpu_percent': round(cpu_percent, 2),
            'memory_usage': memory_usage,
            'memory_limit': memory_limit,
            'memory_percent': round(memory_percent, 2),
            'networks': list(container.attrs.get('NetworkSettings', {}).get('Networks', {}).keys()),
            'mounts': [{'Source': m['Source'], 'Destination': m['Destination']} for m in container.attrs.get('Mounts', [])],
            'labels': container.labels or {},
            'env_vars': self._parse_env_vars(container.attrs.get('Config', {}).get('Env', []))
        }
    
    def _calculate_cpu_percent(self, stats: Dict) -> float:
        """Calculate CPU usage percentage"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpus']) * 100
            return cpu_percent
        except (KeyError, ZeroDivisionError):
            return 0
    
    def _format_ports(self, ports: Dict) -> List[Dict]:
        """Format port mappings"""
        result = []
        if ports:
            for internal, external in ports.items():
                if external:
                    for ext in external:
                        result.append({
                            'internal': internal,
                            'external': f"{ext['HostIp']}:{ext['HostPort']}" if ext.get('HostPort') else 'not mapped'
                        })
        return result
    
    def _parse_env_vars(self, env_list: List[str]) -> Dict:
        """Parse environment variables into dict"""
        result = {}
        for env in env_list:
            if '=' in env:
                key, value = env.split('=', 1)
                result[key] = value
        return result
    
    def start_container(self, container_id: str) -> bool:
        """Start a container"""
        try:
            container = self.client.containers.get(container_id)
            container.start()
            logger.info(f"Started container: {container.name}")
            return True
        except Exception as e:
            logger.error(f"Error starting container {container_id}: {e}")
            raise
    
    def stop_container(self, container_id: str, timeout: int = 10) -> bool:
        """Stop a container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=timeout)
            logger.info(f"Stopped container: {container.name}")
            return True
        except Exception as e:
            logger.error(f"Error stopping container {container_id}: {e}")
            raise
    
    def restart_container(self, container_id: str, timeout: int = 10) -> bool:
        """Restart a container"""
        try:
            container = self.client.containers.get(container_id)
            container.restart(timeout=timeout)
            logger.info(f"Restarted container: {container.name}")
            return True
        except Exception as e:
            logger.error(f"Error restarting container {container_id}: {e}")
            raise
    
    def get_container_logs(self, container_id: str, tail: int = 100, timestamps: bool = True) -> str:
        """Get container logs"""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail, timestamps=timestamps, stderr=True, stdout=True)
            return logs.decode('utf-8')
        except Exception as e:
            logger.error(f"Error getting logs for {container_id}: {e}")
            return f"Error retrieving logs: {str(e)}"
    
    def get_container_stats_stream(self, container_id: str):
        """Stream container stats"""
        try:
            container = self.client.containers.get(container_id)
            for stat in container.stats(stream=True):
                yield self._format_stat(stat)
        except Exception as e:
            logger.error(f"Error streaming stats for {container_id}: {e}")
    
    def _format_stat(self, stat: Dict) -> Dict:
        """Format stat for streaming"""
        return {
            'read': stat.get('read'),
            'cpu_percent': self._calculate_cpu_percent(stat),
            'memory_usage': stat['memory_stats'].get('usage', 0),
            'memory_limit': stat['memory_stats'].get('limit', 0)
        }
    
    def pull_image(self, image: str) -> bool:
        """Pull Docker image"""
        try:
            self.client.images.pull(image)
            logger.info(f"Pulled image: {image}")
            return True
        except Exception as e:
            logger.error(f"Error pulling image {image}: {e}")
            raise
    
    def create_container(self, image: str, name: str, ports: Dict = None, 
                        volumes: Dict = None, environment: Dict = None,
                        network: str = None) -> str:
        """Create a new container"""
        try:
            port_bindings = {}
            if ports:
                for internal, external in ports.items():
                    port_bindings[internal] = external
            
            volume_mounts = {}
            if volumes:
                for host_path, container_path in volumes.items():
                    volume_mounts[host_path] = {'bind': container_path, 'mode': 'rw'}
            
            env_list = []
            if environment:
                env_list = [f"{k}={v}" for k, v in environment.items()]
            
            container = self.client.containers.run(
                image,
                name=name,
                ports=port_bindings,
                volumes=volume_mounts,
                environment=env_list,
                network=network,
                detach=True,
                restart_policy={'Name': 'unless-stopped'},
                stdin_open=True,
                tty=True
            )
            logger.info(f"Created container: {name}")
            return container.id
        except Exception as e:
            logger.error(f"Error creating container {name}: {e}")
            raise
    
    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """Remove a container"""
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            logger.info(f"Removed container: {container.name}")
            return True
        except Exception as e:
            logger.error(f"Error removing container {container_id}: {e}")
            raise
    
    def exec_in_container(self, container_id: str, cmd: str) -> str:
        """Execute command inside container"""
        try:
            container = self.client.containers.get(container_id)
            result = container.exec_run(cmd)
            return result.output.decode('utf-8')
        except Exception as e:
            logger.error(f"Error executing command in {container_id}: {e}")
            raise
    
    def get_networks(self) -> List[Dict]:
        """Get all Docker networks"""
        try:
            networks = self.client.networks.list()
            return [{'name': n.name, 'id': n.id[:12], 'driver': n.driver} for n in networks]
        except Exception as e:
            logger.error(f"Error getting networks: {e}")
            return []
    
    def get_volumes(self) -> List[Dict]:
        """Get all Docker volumes"""
        try:
            volumes = self.client.volumes.list()
            return [{'name': v.name, 'driver': v.driver, 'mountpoint': v.attrs.get('Mountpoint')} for v in volumes]
        except Exception as e:
            logger.error(f"Error getting volumes: {e}")
            return []
