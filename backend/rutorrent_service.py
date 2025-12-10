"""
ruTorrent service wrapper
Manages torrent downloads via ruTorrent (web interface)
"""
import requests
import logging
from typing import Dict, List
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class RuTorrentService:
    """Wrapper for ruTorrent API via XMLRPC/HTTP"""
    
    def __init__(self, base_url: str, username: str = None, password: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Setup auth if provided
        if username and password:
            self.session.auth = (username, password)
    
    def is_connected(self) -> bool:
        """Check if ruTorrent is accessible"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"ruTorrent connection error: {e}")
            return False
    
    def get_server_status(self) -> Dict:
        """Get ruTorrent server status"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/php/getglobalstat.php'),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json() if response.text else {}
            
            return {
                'status': 'ok',
                'upload_speed': data.get('uprate', 0) if data else 0,
                'download_speed': data.get('dnrate', 0) if data else 0,
                'active_torrents': data.get('activeCount', 0) if data else 0
            }
        except Exception as e:
            logger.error(f"Error getting ruTorrent status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_torrents(self) -> List[Dict]:
        """Get list of all torrents"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/php/getbtlist.php'),
                timeout=10
            )
            response.raise_for_status()
            
            torrents = []
            lines = response.text.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 8:
                        torrents.append({
                            'hash': parts[0],
                            'name': parts[1],
                            'type': parts[2],
                            'size': int(parts[3]) if parts[3].isdigit() else 0,
                            'downloaded': int(parts[4]) if parts[4].isdigit() else 0,
                            'ratio': float(parts[5]) if parts[5] else 0,
                            'upload_speed': int(parts[6]) if parts[6].isdigit() else 0,
                            'download_speed': int(parts[7]) if parts[7].isdigit() else 0,
                            'status': parts[9] if len(parts) > 9 else 'unknown'
                        })
            return torrents
        except Exception as e:
            logger.error(f"Error getting torrents: {e}")
            return []
    
    def get_torrent_stats(self) -> Dict:
        """Get torrent statistics"""
        try:
            torrents = self.get_torrents()
            
            total_size = sum(t['size'] for t in torrents)
            total_downloaded = sum(t['downloaded'] for t in torrents)
            total_uploaded = sum(int(t['downloaded'] * t['ratio']) for t in torrents)
            
            return {
                'total_torrents': len(torrents),
                'total_size': total_size,
                'total_downloaded': total_downloaded,
                'total_uploaded': total_uploaded,
                'average_ratio': sum(t['ratio'] for t in torrents) / len(torrents) if torrents else 0
            }
        except Exception as e:
            logger.error(f"Error getting torrent stats: {e}")
            return {}
    
    def start_torrent(self, hash_id: str) -> bool:
        """Start a torrent"""
        try:
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': 'start', 'hash': hash_id},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error starting torrent: {e}")
            return False
    
    def stop_torrent(self, hash_id: str) -> bool:
        """Stop a torrent"""
        try:
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': 'stop', 'hash': hash_id},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error stopping torrent: {e}")
            return False
    
    def pause_torrent(self, hash_id: str) -> bool:
        """Pause a torrent"""
        try:
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': 'pause', 'hash': hash_id},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pausing torrent: {e}")
            return False
    
    def resume_torrent(self, hash_id: str) -> bool:
        """Resume a torrent"""
        try:
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': 'resume', 'hash': hash_id},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error resuming torrent: {e}")
            return False
    
    def remove_torrent(self, hash_id: str, delete_files: bool = False) -> bool:
        """Remove a torrent"""
        try:
            action = 'remove-all' if delete_files else 'remove'
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': action, 'hash': hash_id},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error removing torrent: {e}")
            return False
    
    def get_bandwidth_stats(self) -> Dict:
        """Get bandwidth statistics"""
        try:
            status = self.get_server_status()
            
            return {
                'upload_speed': status.get('upload_speed', 0),
                'download_speed': status.get('download_speed', 0),
                'active_torrents': status.get('active_torrents', 0)
            }
        except Exception as e:
            logger.error(f"Error getting bandwidth stats: {e}")
            return {}
    
    def restart_rtorrent(self) -> bool:
        """Restart rtorrent daemon"""
        try:
            response = self.session.post(
                urljoin(self.base_url, '/php/action.php'),
                data={'action': 'restart'},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error restarting rtorrent: {e}")
            return False
