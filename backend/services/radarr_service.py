"""
Radarr API integration service
"""
import requests
import logging
from typing import Dict, List, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class RadarrService:
    """Wrapper for Radarr API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': api_key})
        self.session.timeout = 10
    
    def is_connected(self) -> bool:
        """Check if Radarr is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Radarr connection failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get Radarr status"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/system/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Radarr status: {e}")
            return {}
    
    def get_movies(self, limit: int = 100) -> List[Dict]:
        """Get movies from library"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/movie",
                params={'pageSize': limit}
            )
            response.raise_for_status()
            movies = response.json()
            
            return [{
                'id': m.get('id'),
                'title': m.get('title'),
                'year': m.get('year'),
                'status': m.get('status'),
                'monitored': m.get('monitored'),
                'fileQuality': m.get('movieFile', {}).get('quality', {}).get('quality', {}).get('name'),
                'sizeOnDisk': m.get('movieFile', {}).get('size', 0),
                'releaseDate': m.get('digitalRelease'),
                'hasFile': m.get('hasFile')
            } for m in movies]
        except Exception as e:
            logger.error(f"Error getting Radarr movies: {e}")
            return []
    
    def get_movie_stats(self) -> Dict:
        """Get movie statistics"""
        try:
            movies = self.get_movies(limit=1000)
            
            total_size = sum(m.get('sizeOnDisk', 0) for m in movies)
            
            return {
                'total_movies': len(movies),
                'monitored': sum(1 for m in movies if m.get('monitored')),
                'unmonitored': sum(1 for m in movies if not m.get('monitored')),
                'with_files': sum(1 for m in movies if m.get('hasFile')),
                'missing': sum(1 for m in movies if not m.get('hasFile') and m.get('monitored')),
                'total_size_gb': round(total_size / (1024**3), 2)
            }
        except Exception as e:
            logger.error(f"Error getting Radarr stats: {e}")
            return {}
    
    def get_upcoming(self, days: int = 7) -> List[Dict]:
        """Get upcoming movie releases"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/calendar",
                params={'start': '-30d', 'end': f'+{days}d'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Radarr calendar: {e}")
            return []
    
    def get_queue(self) -> List[Dict]:
        """Get download queue"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/queue")
            response.raise_for_status()
            
            queue = response.json()
            return [{
                'id': item.get('id'),
                'title': item.get('movie', {}).get('title'),
                'status': item.get('status'),
                'progress': f"{item.get('size', 0) - item.get('sizeleft', 0)}/{item.get('size', 0)}",
                'eta': item.get('estimatedCompletionTime'),
                'protocol': item.get('protocol'),
                'indexer': item.get('indexer')
            } for item in queue]
        except Exception as e:
            logger.error(f"Error getting Radarr queue: {e}")
            return []
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Get recent history"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/history",
                params={'pageSize': limit, 'sortKey': 'date', 'sortDirection': 'descending'}
            )
            response.raise_for_status()
            
            history = response.json()
            return history.get('records', []) if isinstance(history, dict) else history
        except Exception as e:
            logger.error(f"Error getting Radarr history: {e}")
            return []
    
    def get_config(self) -> Dict:
        """Get Radarr configuration"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/config/ui")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Radarr config: {e}")
            return {}
    
    def trigger_search(self, movie_ids: List[int]) -> bool:
        """Trigger search for movies"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v3/command",
                json={'name': 'MovieSearch', 'movieIds': movie_ids}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error triggering Radarr search: {e}")
            return False
    
    def update_movie(self, movie_id: int, **kwargs) -> bool:
        """Update movie settings"""
        try:
            # First get current movie
            response = self.session.get(f"{self.base_url}/api/v3/movie/{movie_id}")
            response.raise_for_status()
            movie = response.json()
            
            # Update with new values
            movie.update(kwargs)
            
            # Put updated movie
            response = self.session.put(
                f"{self.base_url}/api/v3/movie/{movie_id}",
                json=movie
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error updating Radarr movie: {e}")
            return False
