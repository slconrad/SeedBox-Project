"""
System monitoring service
"""
import psutil
import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class SystemService:
    """Monitor system resources"""
    
    @staticmethod
    def get_system_stats() -> Dict:
        """Get current system statistics"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return {
                'cpu': {
                    'percent': cpu,
                    'count_logical': psutil.cpu_count(logical=True),
                    'count_physical': psutil.cpu_count(logical=False)
                },
                'memory': {
                    'used': memory.used,
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used_gb': round(memory.used / (1024**3), 2),
                    'total_gb': round(memory.total / (1024**3), 2)
                },
                'disk': {
                    'used': disk.used,
                    'total': disk.total,
                    'free': disk.free,
                    'percent': disk.percent,
                    'used_gb': round(disk.used / (1024**3), 2),
                    'total_gb': round(disk.total / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2)
                },
                'uptime': {
                    'seconds': int(uptime.total_seconds()),
                    'days': uptime.days,
                    'hours': uptime.seconds // 3600,
                    'minutes': (uptime.seconds % 3600) // 60,
                    'formatted': f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m"
                }
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}
    
    @staticmethod
    def get_cpu_stats() -> Dict:
        """Get detailed CPU statistics"""
        try:
            return {
                'percent': psutil.cpu_percent(interval=1),
                'count_logical': psutil.cpu_count(logical=True),
                'count_physical': psutil.cpu_count(logical=False),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
            }
        except Exception as e:
            logger.error(f"Error getting CPU stats: {e}")
            return {}
    
    @staticmethod
    def get_memory_stats() -> Dict:
        """Get detailed memory statistics"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'memory': {
                    'used': memory.used,
                    'available': memory.available,
                    'total': memory.total,
                    'percent': memory.percent,
                    'active': memory.active if hasattr(memory, 'active') else None,
                    'inactive': memory.inactive if hasattr(memory, 'inactive') else None,
                    'buffers': memory.buffers if hasattr(memory, 'buffers') else None,
                    'cached': memory.cached if hasattr(memory, 'cached') else None
                },
                'swap': {
                    'used': swap.used,
                    'total': swap.total,
                    'free': swap.free,
                    'percent': swap.percent
                }
            }
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {}
    
    @staticmethod
    def get_disk_stats(path: str = '/') -> Dict:
        """Get disk statistics for a path"""
        try:
            disk = psutil.disk_usage(path)
            disk_io = psutil.disk_io_counters()
            
            return {
                'path': path,
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'io': {
                    'read_count': disk_io.read_count,
                    'write_count': disk_io.write_count,
                    'read_bytes': disk_io.read_bytes,
                    'write_bytes': disk_io.write_bytes
                }
            }
        except Exception as e:
            logger.error(f"Error getting disk stats: {e}")
            return {}
    
    @staticmethod
    def get_network_stats() -> Dict:
        """Get network interface statistics"""
        try:
            net_io = psutil.net_io_counters()
            interfaces = psutil.net_if_stats()
            
            result = {
                'total': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv,
                    'errin': net_io.errin,
                    'errout': net_io.errout,
                    'dropin': net_io.dropin,
                    'dropout': net_io.dropout
                },
                'interfaces': {}
            }
            
            for name, stats in interfaces.items():
                result['interfaces'][name] = {
                    'isup': stats.isup,
                    'mtu': stats.mtu,
                    'speed': stats.speed,
                    'duplex': stats.duplex
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting network stats: {e}")
            return {}
    
    @staticmethod
    def get_process_list(limit: int = 10) -> list:
        """Get top processes by memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info', 'status']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_percent': proc.info['memory_percent'],
                        'memory_mb': round(proc.info['memory_info'].rss / (1024**2), 2),
                        'status': proc.info['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:limit]
        except Exception as e:
            logger.error(f"Error getting process list: {e}")
            return []
    
    @staticmethod
    def get_sensor_stats() -> Dict:
        """Get system sensor information (temperature, etc)"""
        try:
            result = {}
            
            # CPU temperature
            try:
                temps = psutil.sensors_temperatures()
                result['temperatures'] = {}
                for name, entries in temps.items():
                    result['temperatures'][name] = [{'label': e.label, 'current': e.current} for e in entries]
            except Exception:
                result['temperatures'] = {}
            
            # Fan speeds
            try:
                fans = psutil.sensors_fans()
                result['fans'] = {}
                for name, entries in fans.items():
                    result['fans'][name] = [{'label': e.label, 'current': e.current} for e in entries]
            except Exception:
                result['fans'] = {}
            
            return result
        except Exception as e:
            logger.error(f"Error getting sensor stats: {e}")
            return {}
