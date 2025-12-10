/**
 * API Client for SeedBox Control Panel
 */

class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            // Token expired, try to refresh
            if (await this.refreshAccessToken()) {
                return this.request(endpoint, options);
            } else {
                // Redirect to login
                window.location.href = '/login';
                return null;
            }
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.error || `HTTP ${response.status}`);
        }

        return response.json();
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    setToken(accessToken, refreshToken) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
    }

    async refreshAccessToken() {
        if (!this.refreshToken) return false;

        try {
            const response = await this.request('/auth/refresh', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${this.refreshToken}` },
            });
            this.setToken(response.access_token, this.refreshToken);
            return true;
        } catch (error) {
            console.error('Token refresh failed:', error);
            return false;
        }
    }

    // Auth endpoints
    async login(username, password) {
        const data = await this.post('/auth/login', { username, password });
        this.setToken(data.access_token, data.refresh_token);
        return data;
    }

    async logout() {
        await this.post('/auth/logout', {});
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.accessToken = null;
        this.refreshToken = null;
    }

    async getCurrentUser() {
        return this.get('/auth/me');
    }

    // System endpoints
    async getSystemStats() {
        return this.get('/system/stats');
    }

    async getSystemHistory(hours = 24) {
        return this.get(`/system/history?hours=${hours}`);
    }

    // Docker endpoints
    async getDockerStatus() {
        return this.get('/docker/status');
    }

    async getContainers() {
        return this.get('/docker/containers');
    }

    async getContainer(id) {
        return this.get(`/docker/containers/${id}`);
    }

    async startContainer(id) {
        return this.post(`/docker/containers/${id}/start`, {});
    }

    async stopContainer(id) {
        return this.post(`/docker/containers/${id}/stop`, {});
    }

    async restartContainer(id) {
        return this.post(`/docker/containers/${id}/restart`, {});
    }

    async getContainerLogs(id, tail = 100) {
        return this.get(`/docker/containers/${id}/logs?tail=${tail}`);
    }

    // Radarr endpoints
    async getRadarrHealth() {
        return this.get('/radarr/health');
    }

    async getRadarrMovies() {
        return this.get('/radarr/movies');
    }

    async getRadarrStats() {
        return this.get('/radarr/stats');
    }

    async getRadarrQueue() {
        return this.get('/radarr/queue');
    }

    // Sonarr endpoints
    async getSonarrHealth() {
        return this.get('/sonarr/health');
    }

    async getSonarrSeries() {
        return this.get('/sonarr/series');
    }

    async getSonarrStats() {
        return this.get('/sonarr/stats');
    }

    async getSonarrQueue() {
        return this.get('/sonarr/queue');
    }

    // Overseerr endpoints
    async getOverseerrHealth() {
        return this.get('/overseerr/health');
    }

    async getOverseerrRequests(status = 'all') {
        return this.get(`/overseerr/requests?status=${status}`);
    }

    async approveRequest(requestId) {
        return this.post(`/overseerr/requests/${requestId}/approve`, {});
    }

    async declineRequest(requestId) {
        return this.post(`/overseerr/requests/${requestId}/decline`, {});
    }

    // Plex endpoints
    async getPlexHealth() {
        return this.get('/plex/health');
    }

    async getPlexStatus() {
        return this.get('/plex/status');
    }

    async getPlexLibraries() {
        return this.get('/plex/libraries');
    }

    async getPlexSessions() {
        return this.get('/plex/sessions');
    }

    async getPlexStreams(count = 10) {
        return this.get(`/plex/streams?count=${count}`);
    }

    async restartPlexServer() {
        return this.post('/plex/restart', {});
    }

    async optimizePlexDatabase() {
        return this.post('/plex/optimize', {});
    }

    async scanPlexLibrary(libKey) {
        return this.post(`/plex/libraries/${libKey}/scan`, {});
    }

    // Tautulli endpoints
    async getTautulliHealth() {
        return this.get('/tautulli/health');
    }

    async getTautulliStatus() {
        return this.get('/tautulli/status');
    }

    async getTautulliActivity() {
        return this.get('/tautulli/activity');
    }

    async getTautulliStats() {
        return this.get('/tautulli/stats');
    }

    async getTautulliUsers() {
        return this.get('/tautulli/users');
    }

    async getTautulliLibraries() {
        return this.get('/tautulli/libraries');
    }

    async getTautulliHistory(count = 50) {
        return this.get(`/tautulli/history?count=${count}`);
    }

    async getTautulliServerInfo() {
        return this.get('/tautulli/server-info');
    }

    async restartTautulli() {
        return this.post('/tautulli/restart', {});
    }

    // uTorrent endpoints
    async getUTorrentHealth() {
        return this.get('/utorrent/health');
    }

    async getUTorrentStatus() {
        return this.get('/utorrent/status');
    }

    async getUTorrentTorrents() {
        return this.get('/utorrent/torrents');
    }

    async getUTorrentStats() {
        return this.get('/utorrent/stats');
    }

    async getUTorrentBandwidth() {
        return this.get('/utorrent/bandwidth');
    }

    async startUTorrent(hash) {
        return this.post(`/utorrent/torrents/${hash}/start`, {});
    }

    async stopUTorrent(hash) {
        return this.post(`/utorrent/torrents/${hash}/stop`, {});
    }

    async pauseUTorrent(hash) {
        return this.post(`/utorrent/torrents/${hash}/pause`, {});
    }

    async resumeUTorrent(hash) {
        return this.post(`/utorrent/torrents/${hash}/resume`, {});
    }

    async removeUTorrent(hash, deleteFiles = false) {
        return this.post(`/utorrent/torrents/${hash}/remove`, { delete_files: deleteFiles });
    }

    async addUTorrentUrl(url) {
        return this.post('/utorrent/torrents/add-url', { url });
    }

    // ruTorrent endpoints
    async getRuTorrentHealth() {
        return this.get('/rutorrent/health');
    }

    async getRuTorrentStatus() {
        return this.get('/rutorrent/status');
    }

    async getRuTorrentTorrents() {
        return this.get('/rutorrent/torrents');
    }

    async getRuTorrentStats() {
        return this.get('/rutorrent/stats');
    }

    async getRuTorrentBandwidth() {
        return this.get('/rutorrent/bandwidth');
    }

    async startRuTorrent(hash) {
        return this.post(`/rutorrent/torrents/${hash}/start`, {});
    }

    async stopRuTorrent(hash) {
        return this.post(`/rutorrent/torrents/${hash}/stop`, {});
    }

    async pauseRuTorrent(hash) {
        return this.post(`/rutorrent/torrents/${hash}/pause`, {});
    }

    async resumeRuTorrent(hash) {
        return this.post(`/rutorrent/torrents/${hash}/resume`, {});
    }

    async removeRuTorrent(hash, deleteFiles = false) {
        return this.post(`/rutorrent/torrents/${hash}/remove`, { delete_files: deleteFiles });
    }

    async restartRuTorrent() {
        return this.post('/rutorrent/restart', {});
    }
}

// Create global API client instance
const api = new APIClient();
