"""
Plex Media Server service wrapper
Manages Plex server status, library statistics, and streaming
"""
import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PlexService:
    """Wrapper for Plex Media Server API"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.headers = {
            'X-Plex-Token': token,
            'Accept': 'application/json'
        }
    
    def is_connected(self) -> bool:
        """Check if Plex server is accessible"""
        try:
            response = self.session.get(
                f"{self.base_url}/identity",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Plex connection error: {e}")
            return False
    
    def get_server_status(self) -> Dict:
        """Get Plex server status and basic info"""
        try:
            response = self.session.get(
                f"{self.base_url}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json() if 'application/json' in response.headers.get('content-type', '') else {}
            
            return {
                'status': 'ok',
                'name': data.get('name', 'Plex Server'),
                'version': data.get('version', 'Unknown'),
                'machine_id': data.get('machineIdentifier', 'Unknown'),
                'uptime': data.get('uptime', 0)
            }
        except Exception as e:
            logger.error(f"Error getting Plex server status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_libraries(self) -> List[Dict]:
        """Get list of all media libraries"""
        try:
            response = self.session.get(
                f"{self.base_url}/library/sections",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            # Parse XML response (Plex returns XML by default)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            libraries = []
            for directory in root.findall('Directory'):
                libraries.append({
                    'key': directory.get('key'),
                    'title': directory.get('title'),
                    'type': directory.get('type'),
                    'agent': directory.get('agent'),
                    'thumb': directory.get('thumb'),
                    'art': directory.get('art'),
                    'scanner': directory.get('scanner'),
                    'composite': directory.get('composite')
                })
            return libraries
        except Exception as e:
            logger.error(f"Error getting Plex libraries: {e}")
            return []
    
    def get_library_stats(self, library_key: str) -> Dict:
        """Get statistics for a specific library"""
        try:
            response = self.session.get(
                f"{self.base_url}/library/sections/{library_key}/all",
                headers=self.headers,
                params={'X-Plex-Token': self.token},
                timeout=10
            )
            response.raise_for_status()
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            total = root.get('totalSize', 0)
            viewed = root.get('viewedLeafCount', 0)
            
            return {
                'total_items': int(total),
                'viewed_items': int(viewed),
                'unwatched_items': int(total) - int(viewed) if total else 0,
                'size_bytes': 0
            }
        except Exception as e:
            logger.error(f"Error getting library stats: {e}")
            return {'total_items': 0, 'viewed_items': 0, 'unwatched_items': 0}
    
    def get_recent_streams(self, count: int = 10) -> List[Dict]:
        """Get recent stream history"""
        try:
            response = self.session.get(
                f"{self.base_url}/status/sessions",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            streams = []
            for session in root.findall('Video') + root.findall('Track'):
                streams.append({
                    'title': session.get('title'),
                    'user': session.find('User').get('title') if session.find('User') is not None else 'Unknown',
                    'player': session.find('Player').get('title') if session.find('Player') is not None else 'Unknown',
                    'state': session.find('TranscodeSession').get('progress') if session.find('TranscodeSession') is not None else 'direct'
                })
            return streams[:count]
        except Exception as e:
            logger.error(f"Error getting recent streams: {e}")
            return []
    
    def get_active_sessions(self) -> List[Dict]:
        """Get currently active streaming sessions"""
        try:
            response = self.session.get(
                f"{self.base_url}/status/sessions",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            sessions = []
            for video in root.findall('.//Video'):
                user_elem = video.find('User')
                player_elem = video.find('Player')
                
                sessions.append({
                    'id': video.get('sessionKey'),
                    'title': video.get('title'),
                    'user': user_elem.get('title') if user_elem is not None else 'Unknown',
                    'player': player_elem.get('title') if player_elem is not None else 'Unknown',
                    'progress': video.get('viewOffset', 0),
                    'duration': video.get('duration', 0)
                })
            
            return sessions
        except Exception as e:
            logger.error(f"Error getting active sessions: {e}")
            return []
    
    def restart_server(self) -> bool:
        """Restart Plex Media Server"""
        try:
            self.session.get(
                f"{self.base_url}/system/restart",
                headers=self.headers,
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Error restarting Plex server: {e}")
            return False
    
    def optimize_database(self) -> bool:
        """Optimize Plex database"""
        try:
            self.session.get(
                f"{self.base_url}/library/optimize",
                headers=self.headers,
                timeout=30
            )
            return True
        except Exception as e:
            logger.error(f"Error optimizing Plex database: {e}")
            return False
    
    def perform_library_scan(self, library_key: str) -> bool:
        """Trigger library scan"""
        try:
            self.session.get(
                f"{self.base_url}/library/sections/{library_key}/refresh",
                headers=self.headers,
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Error scanning library: {e}")
            return False
