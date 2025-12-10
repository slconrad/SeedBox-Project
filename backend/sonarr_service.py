"""
Sonarr API integration service
"""
import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SonarrService:
    """Wrapper for Sonarr API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': api_key})
        self.session.timeout = 10
    
    def is_connected(self) -> bool:
        """Check if Sonarr is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Sonarr connection failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get Sonarr status"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/system/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Sonarr status: {e}")
            return {}
    
    def get_series(self, limit: int = 100) -> List[Dict]:
        """Get series from library"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/series",
                params={'pageSize': limit}
            )
            response.raise_for_status()
            series = response.json()
            
            return [{
                'id': s.get('id'),
                'title': s.get('title'),
                'status': s.get('status'),
                'monitored': s.get('monitored'),
                'seasonCount': s.get('seasonCount'),
                'episodeCount': s.get('episodeFileCount'),
                'episodesToDownload': s.get('episodsToAir'),
                'sizeOnDisk': s.get('statistics', {}).get('sizeOnDisk', 0),
                'episodeProgress': s.get('statistics', {}).get('episodeFileCount')
            } for s in series]
        except Exception as e:
            logger.error(f"Error getting Sonarr series: {e}")
            return []
    
    def get_series_stats(self) -> Dict:
        """Get series statistics"""
        try:
            series = self.get_series(limit=1000)
            
            total_size = sum(s.get('sizeOnDisk', 0) for s in series)
            
            return {
                'total_series': len(series),
                'monitored': sum(1 for s in series if s.get('monitored')),
                'unmonitored': sum(1 for s in series if not s.get('monitored')),
                'total_episodes': sum(s.get('episodeProgress', 0) for s in series),
                'total_size_gb': round(total_size / (1024**3), 2),
                'active': sum(1 for s in series if s.get('status') == 'continuing')
            }
        except Exception as e:
            logger.error(f"Error getting Sonarr stats: {e}")
            return {}
    
    def get_calendar(self, days: int = 7) -> List[Dict]:
        """Get upcoming episodes"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/calendar",
                params={'start': '-30d', 'end': f'+{days}d'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Sonarr calendar: {e}")
            return []
    
    def get_queue(self) -> List[Dict]:
        """Get download queue"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/queue")
            response.raise_for_status()
            
            queue = response.json()
            return [{
                'id': item.get('id'),
                'title': item.get('series', {}).get('title'),
                'episode': item.get('episode', {}).get('episodeNumber'),
                'season': item.get('episode', {}).get('seasonNumber'),
                'status': item.get('status'),
                'progress': f"{item.get('size', 0) - item.get('sizeleft', 0)}/{item.get('size', 0)}",
                'eta': item.get('estimatedCompletionTime')
            } for item in queue]
        except Exception as e:
            logger.error(f"Error getting Sonarr queue: {e}")
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
            logger.error(f"Error getting Sonarr history: {e}")
            return []
    
    def get_wanted(self) -> List[Dict]:
        """Get wanted episodes"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v3/wanted/missing",
                params={'pageSize': 100}
            )
            response.raise_for_status()
            
            wanted = response.json()
            return wanted.get('records', []) if isinstance(wanted, dict) else wanted
        except Exception as e:
            logger.error(f"Error getting Sonarr wanted: {e}")
            return []
    
    def get_config(self) -> Dict:
        """Get Sonarr configuration"""
        try:
            response = self.session.get(f"{self.base_url}/api/v3/config/ui")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Sonarr config: {e}")
            return {}
    
    def trigger_search(self, series_ids: List[int]) -> bool:
        """Trigger search for series"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v3/command",
                json={'name': 'SeriesSearch', 'seriesIds': series_ids}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error triggering Sonarr search: {e}")
            return False
