"""
uTorrent service wrapper
Manages torrent downloads via uTorrent RPC API
"""
import requests
import base64
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class UTorrentService:
    """Wrapper for uTorrent RPC API"""
    
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        
        # Setup basic auth
        auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.session.headers.update({'Authorization': f'Basic {auth_string}'})
    
    def is_connected(self) -> bool:
        """Check if uTorrent is accessible"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/gui/?list=1'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"uTorrent connection error: {e}")
            return False
    
    def get_server_status(self) -> Dict:
        """Get uTorrent server status"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/gui/?list=1'),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            server_info = data.get('server-info', [])
            if server_info:
                info = server_info[0]
                return {
                    'status': 'ok',
                    'version': info[1] if len(info) > 1 else 'Unknown',
                    'server_state': info[0] if len(info) > 0 else 'unknown'
                }
            return {'status': 'ok'}
        except Exception as e:
            logger.error(f"Error getting uTorrent status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_torrents(self) -> List[Dict]:
        """Get list of all torrents"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/gui/?list=1'),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            torrents = []
            for torrent in data.get('torrents', []):
                torrents.append({
                    'hash': torrent[0],
                    'status': torrent[1],
                    'name': torrent[2],
                    'size': torrent[3],
                    'progress': torrent[4],
                    'downloaded': torrent[5],
                    'uploaded': torrent[6],
                    'ratio': torrent[7],
                    'upload_speed': torrent[8],
                    'download_speed': torrent[9],
                    'eta': torrent[10],
                    'label': torrent[11],
                    'peers': torrent[12],
                    'seeds': torrent[13],
                    'availability': torrent[14],
                    'torrent_queue_order': torrent[15],
                    'remaining': torrent[16]
                })
            return torrents
        except Exception as e:
            logger.error(f"Error getting torrents: {e}")
            return []
    
    def get_torrent_stats(self) -> Dict:
        """Get torrent statistics"""
        try:
            torrents = self.get_torrents()
            
            downloading = sum(1 for t in torrents if t['status'] in [200, 201])
            seeding = sum(1 for t in torrents if t['status'] in [136])
            total_size = sum(t['size'] for t in torrents)
            total_uploaded = sum(t['uploaded'] for t in torrents)
            total_downloaded = sum(t['downloaded'] for t in torrents)
            
            return {
                'total_torrents': len(torrents),
                'downloading': downloading,
                'seeding': seeding,
                'total_size': total_size,
                'total_uploaded': total_uploaded,
                'total_downloaded': total_downloaded
            }
        except Exception as e:
            logger.error(f"Error getting torrent stats: {e}")
            return {}
    
    def start_torrent(self, hash_id: str) -> bool:
        """Start a torrent"""
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action=start&hash={hash_id}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error starting torrent: {e}")
            return False
    
    def stop_torrent(self, hash_id: str) -> bool:
        """Stop a torrent"""
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action=stop&hash={hash_id}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error stopping torrent: {e}")
            return False
    
    def pause_torrent(self, hash_id: str) -> bool:
        """Pause a torrent"""
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action=pause&hash={hash_id}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pausing torrent: {e}")
            return False
    
    def resume_torrent(self, hash_id: str) -> bool:
        """Resume a torrent"""
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action=resume&hash={hash_id}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error resuming torrent: {e}")
            return False
    
    def remove_torrent(self, hash_id: str, delete_files: bool = False) -> bool:
        """Remove a torrent"""
        try:
            action = 'removedata' if delete_files else 'remove'
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action={action}&hash={hash_id}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error removing torrent: {e}")
            return False
    
    def add_torrent_url(self, url: str) -> bool:
        """Add torrent from URL"""
        try:
            response = self.session.get(
                urljoin(self.base_url, f'/gui/?action=add-url&s={url}'),
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error adding torrent: {e}")
            return False
    
    def get_bandwidth_stats(self) -> Dict:
        """Get bandwidth statistics"""
        try:
            torrents = self.get_torrents()
            
            upload_speed = sum(t['upload_speed'] for t in torrents)
            download_speed = sum(t['download_speed'] for t in torrents)
            
            return {
                'upload_speed': upload_speed,
                'download_speed': download_speed,
                'active_connections': len([t for t in torrents if t['status'] != 0])
            }
        except Exception as e:
            logger.error(f"Error getting bandwidth stats: {e}")
            return {}
