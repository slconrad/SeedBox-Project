"""
Service wrappers for external integrations

This module contains wrapper classes for all external services:
- Docker integration
- System monitoring
- Media servers (Plex, Radarr, Sonarr, Overseerr, Tautulli)
- Torrent clients (uTorrent, ruTorrent)
"""

from .docker_service import DockerService
from .system_service import SystemService
from .radarr_service import RadarrService
from .sonarr_service import SonarrService
from .overseerr_service import OverseerrService
from .plex_service import PlexService
from .tautulli_service import TautulliService
from .utorrent_service import UTorrentService
from .rutorrent_service import RuTorrentService

__all__ = [
    'DockerService',
    'SystemService',
    'RadarrService',
    'SonarrService',
    'OverseerrService',
    'PlexService',
    'TautulliService',
    'UTorrentService',
    'RuTorrentService',
]
