"""
Tautulli (Plex Monitoring) service wrapper
Monitors and reports on Plex Media Server activity
"""
import requests
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class TautulliService:
    """Wrapper for Tautulli API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
    
    def _make_request(self, cmd: str, params: Dict = None) -> Dict:
        """Make API request to Tautulli"""
        try:
            if params is None:
                params = {}
            params['cmd'] = cmd
            params['apikey'] = self.api_key
            
            response = self.session.get(
                f"{self.base_url}/api/v2",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Tautulli API error: {e}")
            return {'response': {'result': 'error', 'message': str(e)}}
    
    def is_connected(self) -> bool:
        """Check if Tautulli is accessible"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v2",
                params={'cmd': 'get_tautulli_info', 'apikey': self.api_key},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Tautulli connection error: {e}")
            return False
    
    def get_server_status(self) -> Dict:
        """Get Tautulli and Plex server status"""
        try:
            result = self._make_request('get_tautulli_info')
            data = result.get('response', {}).get('data', {})
            
            return {
                'status': 'ok',
                'version': data.get('tautulli_version', 'Unknown'),
                'plex_server': data.get('plex_server', 'Unknown'),
                'plex_version': data.get('plex_version', 'Unknown'),
                'uptime': data.get('uptime', 0)
            }
        except Exception as e:
            logger.error(f"Error getting Tautulli status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_activity(self) -> Dict:
        """Get current activity (streams, users, etc)"""
        try:
            result = self._make_request('get_activity')
            data = result.get('response', {}).get('data', {})
            
            return {
                'total_streams': int(data.get('total_streams', 0)),
                'total_bandwidth': data.get('total_bandwidth', '0 Kbps'),
                'lan_bandwidth': data.get('lan_bandwidth', '0 Kbps'),
                'wan_bandwidth': data.get('wan_bandwidth', '0 Kbps'),
                'sessions': data.get('sessions', [])
            }
        except Exception as e:
            logger.error(f"Error getting activity: {e}")
            return {'total_streams': 0, 'total_bandwidth': '0 Kbps', 'sessions': []}
    
    def get_stats(self) -> Dict:
        """Get Tautulli statistics"""
        try:
            result = self._make_request('get_stats')
            data = result.get('response', {}).get('data', {})
            
            return {
                'total_plays': int(data.get('total_plays', 0)) if data else 0,
                'total_time': data.get('total_time', 0) if data else 0,
                'total_users': int(data.get('total_users', 0)) if data else 0,
                'total_libraries': int(data.get('total_libraries', 0)) if data else 0
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'total_plays': 0, 'total_time': 0, 'total_users': 0}
    
    def get_users(self) -> List[Dict]:
        """Get list of Plex users"""
        try:
            result = self._make_request('get_users')
            users = result.get('response', {}).get('data', [])
            
            return [
                {
                    'user_id': user.get('user_id'),
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'thumb': user.get('thumb'),
                    'last_seen': user.get('last_seen'),
                    'plays': user.get('plays'),
                    'duration': user.get('duration')
                }
                for user in users
            ]
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    def get_library_stats(self) -> List[Dict]:
        """Get statistics for all libraries"""
        try:
            result = self._make_request('get_libraries')
            libraries = result.get('response', {}).get('data', [])
            
            stats = []
            for lib in libraries:
                stats.append({
                    'library_id': lib.get('section_id'),
                    'library_name': lib.get('section_name'),
                    'library_type': lib.get('section_type'),
                    'count': lib.get('count'),
                    'plays': lib.get('plays'),
                    'duration': lib.get('duration')
                })
            return stats
        except Exception as e:
            logger.error(f"Error getting library stats: {e}")
            return []
    
    def get_history(self, count: int = 50) -> List[Dict]:
        """Get playback history"""
        try:
            result = self._make_request('get_history', {'length': count})
            history = result.get('response', {}).get('data', [])
            
            return [
                {
                    'user': entry.get('user'),
                    'title': entry.get('full_title'),
                    'started': entry.get('started'),
                    'stopped': entry.get('stopped'),
                    'duration': entry.get('duration'),
                    'watched': entry.get('watched_status')
                }
                for entry in history
            ]
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []
    
    def get_server_info(self) -> Dict:
        """Get Plex server information"""
        try:
            result = self._make_request('get_server_info')
            data = result.get('response', {}).get('data', {})
            
            return {
                'name': data.get('name'),
                'machine_id': data.get('machine_id'),
                'version': data.get('version'),
                'platform': data.get('platform'),
                'locations': data.get('locations'),
                'library_count': data.get('library_count')
            }
        except Exception as e:
            logger.error(f"Error getting server info: {e}")
            return {}
    
    def restart_tautulli(self) -> bool:
        """Restart Tautulli service"""
        try:
            self._make_request('restart_tautulli')
            return True
        except Exception as e:
            logger.error(f"Error restarting Tautulli: {e}")
            return False
