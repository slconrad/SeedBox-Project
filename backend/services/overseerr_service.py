"""
Overseerr API integration service
"""
import requests
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class OverseerrService:
    """Wrapper for Overseerr API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': api_key})
        self.session.timeout = 10
    
    def is_connected(self) -> bool:
        """Check if Overseerr is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/status")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Overseerr connection failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get Overseerr status"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Overseerr status: {e}")
            return {}
    
    def get_requests(self, status: str = 'all', limit: int = 50) -> List[Dict]:
        """Get media requests"""
        try:
            params = {'pageSize': limit, 'sort': 'added', 'page': 1}
            if status != 'all':
                params['filter'] = status
            
            response = self.session.get(f"{self.base_url}/api/v1/request", params=params)
            response.raise_for_status()
            
            data = response.json()
            requests_list = data.get('results', []) if isinstance(data, dict) else data
            
            return [{
                'id': r.get('id'),
                'media_type': r.get('media', {}).get('mediaType'),
                'title': r.get('media', {}).get('title'),
                'requested_by': r.get('requestedBy', {}).get('username'),
                'status': r.get('status'),
                'created_at': r.get('createdAt'),
                'updated_at': r.get('updatedAt'),
                'is_4k': r.get('is4k')
            } for r in requests_list]
        except Exception as e:
            logger.error(f"Error getting Overseerr requests: {e}")
            return []
    
    def get_request_stats(self) -> Dict:
        """Get request statistics"""
        try:
            pending = self.get_requests(status='pending', limit=1)
            approved = self.get_requests(status='approved', limit=1)
            available = self.get_requests(status='available', limit=1)
            
            return {
                'pending_count': len(pending),
                'approved_count': len(approved),
                'available_count': len(available)
            }
        except Exception as e:
            logger.error(f"Error getting Overseerr stats: {e}")
            return {}
    
    def get_users(self, limit: int = 100) -> List[Dict]:
        """Get Overseerr users"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/user",
                params={'pageSize': limit}
            )
            response.raise_for_status()
            
            data = response.json()
            users = data.get('results', []) if isinstance(data, dict) else data
            
            return [{
                'id': u.get('id'),
                'username': u.get('username'),
                'email': u.get('email'),
                'display_name': u.get('displayName'),
                'created_at': u.get('createdAt'),
                'requests_count': u.get('requestCount', 0)
            } for u in users]
        except Exception as e:
            logger.error(f"Error getting Overseerr users: {e}")
            return []
    
    def approve_request(self, request_id: int, is_4k: bool = False) -> bool:
        """Approve a media request"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/request/{request_id}/approve",
                json={'is4k': is_4k}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error approving request {request_id}: {e}")
            return False
    
    def decline_request(self, request_id: int) -> bool:
        """Decline a media request"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/request/{request_id}/decline"
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error declining request {request_id}: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Get Overseerr settings"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/settings")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Overseerr settings: {e}")
            return {}
