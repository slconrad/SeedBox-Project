/**
 * Main application logic
 */

let resourceChart = null;
let containers = [];

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const msg = document.getElementById('toastMessage');
    
    const icons = {
        success: 'fa-check-circle text-green-400',
        error: 'fa-exclamation-circle text-red-400',
        info: 'fa-info-circle text-blue-400'
    };
    
    icon.className = `fas ${icons[type]} text-xl`;
    msg.textContent = message;
    
    toast.classList.remove('translate-y-20', 'opacity-0');
    
    setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
    }, 3000);
}

// Load system statistics
async function loadSystemStats() {
    try {
        const stats = await api.getSystemStats();
        
        document.getElementById('uptime').textContent = stats.uptime.formatted;
        document.getElementById('cpuUsage').textContent = `${Math.round(stats.cpu.percent)}%`;
        document.getElementById('cpuBar').style.width = `${Math.round(stats.cpu.percent)}%`;
        
        document.getElementById('memoryUsage').textContent = `${stats.memory.used_gb} / ${stats.memory.total_gb} GB`;
        document.getElementById('memoryBar').style.width = `${stats.memory.percent}%`;
        
        document.getElementById('diskUsage').textContent = `${stats.disk.free_gb} TB Free`;
        document.getElementById('diskBar').style.width = `${stats.disk.percent}%`;
        
        // Update chart
        updateResourceChart(stats);
    } catch (error) {
        console.error('Error loading system stats:', error);
    }
}

// Load containers
async function loadContainers() {
    try {
        const data = await api.getContainers();
        containers = data.containers;
        renderContainers();
        renderQuickStatus();
    } catch (error) {
        console.error('Error loading containers:', error);
        showToast('Failed to load containers', 'error');
    }
}

// Render containers
function renderContainers() {
    const grid = document.getElementById('appGrid');
    
    if (containers.length === 0) {
        grid.innerHTML = '<p class="text-gray-400">No containers found</p>';
        return;
    }
    
    grid.innerHTML = containers.map(container => {
        const isRunning = container.status === 'running';
        return `
            <div class="app-card card-gradient rounded-2xl border border-gray-700/50 overflow-hidden transition-all duration-300">
                <div class="bg-gradient-to-r from-blue-500/30 to-purple-600/30 p-5">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="font-bold text-xl text-white">${container.name}</h3>
                            <p class="text-sm text-gray-300">${container.image}</p>
                        </div>
                        <div class="flex items-center space-x-2 bg-black/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
                            <span class="w-2.5 h-2.5 rounded-full ${isRunning ? 'bg-green-400 status-online' : 'bg-red-400'}"></span>
                            <span class="text-sm font-medium text-white">${isRunning ? 'Running' : 'Stopped'}</span>
                        </div>
                    </div>
                </div>
                <div class="p-5">
                    <div class="grid grid-cols-3 gap-2 mb-4 text-xs">
                        <div class="bg-gray-700/30 rounded p-2">
                            <span class="text-gray-400">CPU</span>
                            <p class="font-bold">${container.cpu_percent.toFixed(1)}%</p>
                        </div>
                        <div class="bg-gray-700/30 rounded p-2">
                            <span class="text-gray-400">Memory</span>
                            <p class="font-bold">${(container.memory_usage / 1024 / 1024).toFixed(0)}MB</p>
                        </div>
                        <div class="bg-gray-700/30 rounded p-2">
                            <span class="text-gray-400">Status</span>
                            <p class="font-bold text-blue-400">${container.status}</p>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        ${isRunning ? `
                            <button onclick="stopContainer('${container.full_id}')" class="flex-1 bg-red-600 hover:bg-red-700 py-2 rounded-lg text-sm transition">
                                <i class="fas fa-stop mr-1"></i>Stop
                            </button>
                        ` : `
                            <button onclick="startContainer('${container.full_id}')" class="flex-1 bg-green-600 hover:bg-green-700 py-2 rounded-lg text-sm transition">
                                <i class="fas fa-play mr-1"></i>Start
                            </button>
                        `}
                        <button onclick="restartContainer('${container.full_id}')" class="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded-lg text-sm transition">
                            <i class="fas fa-redo mr-1"></i>Restart
                        </button>
                        <button onclick="viewLogs('${container.full_id}')" class="flex-1 bg-gray-700 hover:bg-gray-600 py-2 rounded-lg text-sm transition">
                            <i class="fas fa-file-alt mr-1"></i>Logs
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Render quick status
function renderQuickStatus() {
    const container = document.getElementById('quickStatus');
    container.innerHTML = containers.map(c => {
        const isRunning = c.status === 'running';
        return `
            <div class="bg-gray-800/50 rounded-xl p-4 text-center">
                <div class="w-12 h-12 mx-auto mb-2 rounded-xl flex items-center justify-center ${isRunning ? 'bg-green-900/30 ring-2 ring-green-500/30' : 'bg-red-900/30 ring-2 ring-red-500/30'}">
                    <i class="fas fa-box text-2xl ${isRunning ? 'text-green-400' : 'text-red-400'}"></i>
                </div>
                <p class="font-medium text-sm truncate">${c.name}</p>
                <div class="flex items-center justify-center space-x-1 mt-1">
                    <span class="w-2 h-2 rounded-full ${isRunning ? 'bg-green-400 status-online' : 'bg-red-400'}"></span>
                    <p class="text-xs ${isRunning ? 'text-green-400' : 'text-red-400'}">${isRunning ? 'Online' : 'Offline'}</p>
                </div>
            </div>
        `;
    }).join('');
}

// Container control functions
async function startContainer(id) {
    try {
        await api.startContainer(id);
        showToast('Container started', 'success');
        await loadContainers();
    } catch (error) {
        showToast('Failed to start container', 'error');
    }
}

async function stopContainer(id) {
    try {
        await api.stopContainer(id);
        showToast('Container stopped', 'success');
        await loadContainers();
    } catch (error) {
        showToast('Failed to stop container', 'error');
    }
}

async function restartContainer(id) {
    try {
        await api.restartContainer(id);
        showToast('Container restarted', 'success');
        await loadContainers();
    } catch (error) {
        showToast('Failed to restart container', 'error');
    }
}

async function viewLogs(id) {
    try {
        const data = await api.getContainerLogs(id, 100);
        const logContainer = document.getElementById('logContainer');
        logContainer.innerHTML = data.logs.map(log => 
            `<div class="text-gray-300">${escapeHtml(log)}</div>`
        ).join('');
        showTab('logs');
    } catch (error) {
        showToast('Failed to load logs', 'error');
    }
}

// Load media data
async function loadMediaData() {
    try {
        // Load Radarr
        const radarrStats = await api.getRadarrStats();
        const radarrQueue = await api.getRadarrQueue();
        
        document.getElementById('radarr-stats').innerHTML = `
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Movies:</span>
                    <span class="font-bold">${radarrStats.total_movies}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">With Files:</span>
                    <span class="font-bold">${radarrStats.with_files}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Missing:</span>
                    <span class="font-bold text-orange-400">${radarrStats.missing}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Size:</span>
                    <span class="font-bold">${radarrStats.total_size_gb} GB</span>
                </div>
            </div>
        `;
        
        document.getElementById('radarr-queue').innerHTML = radarrQueue.queue.slice(0, 5).map(item => `
            <div class="bg-gray-700/30 rounded p-3 text-sm">
                <p class="font-medium truncate">${item.title}</p>
                <p class="text-gray-400 text-xs">${item.progress}</p>
            </div>
        `).join('');
        
        // Load Sonarr
        const sonarrStats = await api.getSonarrStats();
        const sonarrQueue = await api.getSonarrQueue();
        
        document.getElementById('sonarr-stats').innerHTML = `
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Series:</span>
                    <span class="font-bold">${sonarrStats.total_series}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Active:</span>
                    <span class="font-bold">${sonarrStats.active}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Episodes:</span>
                    <span class="font-bold">${sonarrStats.total_episodes}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-400">Total Size:</span>
                    <span class="font-bold">${sonarrStats.total_size_gb} GB</span>
                </div>
            </div>
        `;
        
        document.getElementById('sonarr-queue').innerHTML = sonarrQueue.queue.slice(0, 5).map(item => `
            <div class="bg-gray-700/30 rounded p-3 text-sm">
                <p class="font-medium truncate">${item.title} S${item.season}E${item.episode}</p>
                <p class="text-gray-400 text-xs">${item.progress}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading media data:', error);
    }
}

// Load requests
async function loadRequests() {
    try {
        const status = document.getElementById('requestFilter')?.value || 'all';
        const data = await api.getOverseerrRequests(status);
        
        document.getElementById('requestsContainer').innerHTML = data.requests.map(req => `
            <div class="card-gradient rounded-2xl p-4 border border-gray-700/50 flex justify-between items-center">
                <div>
                    <h4 class="font-bold">${req.title}</h4>
                    <p class="text-sm text-gray-400">By ${req.requested_by} - ${req.status}</p>
                </div>
                <div class="space-x-2">
                    ${req.status === 'pending' ? `
                        <button onclick="approveRequest(${req.id})" class="bg-green-600 hover:bg-green-700 px-3 py-1 rounded text-sm">
                            <i class="fas fa-check mr-1"></i>Approve
                        </button>
                        <button onclick="declineRequest(${req.id})" class="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm">
                            <i class="fas fa-times mr-1"></i>Decline
                        </button>
                    ` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading requests:', error);
    }
}

// Update resource chart
function updateResourceChart(stats) {
    if (!document.getElementById('resourceChart')) return;
    
    if (!resourceChart) {
        const ctx = document.getElementById('resourceChart').getContext('2d');
        resourceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                datasets: [
                    {
                        label: 'CPU %',
                        data: Array(24).fill(stats.cpu.percent),
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Memory %',
                        data: Array(24).fill(stats.memory.percent),
                        borderColor: '#A855F7',
                        backgroundColor: 'rgba(168, 85, 247, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#9CA3AF' } }
                },
                scales: {
                    x: { ticks: { color: '#6B7280' }, grid: { color: 'rgba(75, 85, 99, 0.3)' } },
                    y: { ticks: { color: '#6B7280' }, grid: { color: 'rgba(75, 85, 99, 0.3)' }, max: 100 }
                }
            }
        });
    } else {
        resourceChart.data.datasets[0].data.shift();
        resourceChart.data.datasets[0].data.push(stats.cpu.percent);
        resourceChart.data.datasets[1].data.shift();
        resourceChart.data.datasets[1].data.push(stats.memory.percent);
        resourceChart.update('none');
    }
}

// Approve/decline requests
async function approveRequest(requestId) {
    try {
        await api.approveRequest(requestId);
        showToast('Request approved', 'success');
        await loadRequests();
    } catch (error) {
        showToast('Failed to approve request', 'error');
    }
}

async function declineRequest(requestId) {
    try {
        await api.declineRequest(requestId);
        showToast('Request declined', 'success');
        await loadRequests();
    } catch (error) {
        showToast('Failed to decline request', 'error');
    }
}

// Filter functions
function filterLogs() {
    // Implement log filtering
}

function filterRequests() {
    loadRequests();
}

// Logout
async function logout() {
    try {
        await api.logout();
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/login';
    }
}

// Utility function
function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/[&<>"']/g, char => {
        const escapeChars = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };
        return escapeChars[char];
    });
}

// Load user info
async function loadUserInfo() {
    try {
        const user = await api.getCurrentUser();
        document.getElementById('currentUser').textContent = user.username;
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

// Load torrent data (uTorrent & ruTorrent)
async function loadTorrentData() {
    try {
        // Load uTorrent
        const uStats = await api.getUTorrentStats();
        const uTorrents = await api.getUTorrentTorrents();
        
        document.getElementById('utorrent-stats').innerHTML = `
            <div class="space-y-2 text-sm">
                <div class="flex justify-between"><span class="text-gray-400">Active:</span><span>${uStats.downloading}</span></div>
                <div class="flex justify-between"><span class="text-gray-400">Seeding:</span><span>${uStats.seeding}</span></div>
                <div class="flex justify-between"><span class="text-gray-400">Total Size:</span><span>${(uStats.total_size / 1024 / 1024 / 1024).toFixed(2)} GB</span></div>
                <div class="flex justify-between"><span class="text-gray-400">Uploaded:</span><span>${(uStats.total_uploaded / 1024 / 1024 / 1024).toFixed(2)} GB</span></div>
            </div>
        `;
        
        document.getElementById('utorrent-torrents').innerHTML = uTorrents.slice(0, 5).map(t => `
            <div class="bg-gray-700/20 rounded p-3">
                <div class="flex justify-between items-start mb-2">
                    <span class="font-medium truncate">${t.name}</span>
                    <span class="text-xs text-green-400">${t.progress}%</span>
                </div>
                <div class="w-full bg-gray-700 rounded-full h-1.5">
                    <div class="bg-green-500 h-1.5 rounded-full" style="width: ${t.progress}%"></div>
                </div>
            </div>
        `).join('');
        
        // Load ruTorrent
        const rStats = await api.getRuTorrentStats();
        const rTorrents = await api.getRuTorrentTorrents();
        
        document.getElementById('rutorrent-stats').innerHTML = `
            <div class="space-y-2 text-sm">
                <div class="flex justify-between"><span class="text-gray-400">Total:</span><span>${rStats.total_torrents}</span></div>
                <div class="flex justify-between"><span class="text-gray-400">Total Size:</span><span>${(rStats.total_size / 1024 / 1024 / 1024).toFixed(2)} GB</span></div>
                <div class="flex justify-between"><span class="text-gray-400">Avg Ratio:</span><span>${rStats.average_ratio?.toFixed(2)}</span></div>
            </div>
        `;
        
        document.getElementById('rutorrent-torrents').innerHTML = rTorrents.slice(0, 5).map(t => `
            <div class="bg-gray-700/20 rounded p-3">
                <div class="flex justify-between items-start mb-2">
                    <span class="font-medium truncate">${t.name}</span>
                    <span class="text-xs text-yellow-400">${(t.downloaded / t.size * 100).toFixed(0)}%</span>
                </div>
                <div class="text-xs text-gray-400">Ratio: ${t.ratio.toFixed(2)}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading torrent data:', error);
        showToast('Failed to load torrent data', 'error');
    }
}

// Load Plex data
async function loadPlexData() {
    try {
        // Plex Status
        const plexStatus = await api.getPlexStatus();
        document.getElementById('plex-status').innerHTML = `
            <div class="space-y-2 text-sm">
                <div><span class="text-gray-400">Server:</span> <span>${plexStatus.name}</span></div>
                <div><span class="text-gray-400">Version:</span> <span>${plexStatus.version}</span></div>
                <div><span class="text-gray-400">Uptime:</span> <span>${(plexStatus.uptime / 3600).toFixed(1)}h</span></div>
            </div>
        `;
        
        // Tautulli Status
        const tautulliStatus = await api.getTautulliStatus();
        document.getElementById('tautulli-status').innerHTML = `
            <div class="space-y-2 text-sm">
                <div><span class="text-gray-400">Version:</span> <span>${tautulliStatus.version}</span></div>
                <div><span class="text-gray-400">Server:</span> <span>${tautulliStatus.plex_server}</span></div>
                <div><span class="text-gray-400">Plex Ver:</span> <span>${tautulliStatus.plex_version}</span></div>
            </div>
        `;
        
        // Active Sessions
        const sessions = await api.getPlexSessions();
        document.getElementById('plex-sessions').innerHTML = sessions.count > 0 ? sessions.sessions.map(s => `
            <div class="text-xs bg-gray-700/20 rounded p-2">
                <div class="font-medium">${s.title}</div>
                <div class="text-gray-400">User: ${s.user}</div>
                <div class="text-gray-400">Player: ${s.player}</div>
            </div>
        `).join('') : '<p class="text-gray-500">No active sessions</p>';
        
        // Libraries
        const libs = await api.getPlexLibraries();
        document.getElementById('plex-libraries').innerHTML = libs.libraries.map(lib => `
            <div class="bg-gray-700/30 rounded p-4">
                <div class="font-medium mb-2">${lib.title}</div>
                <div class="text-xs text-gray-400 mb-3">${lib.type}</div>
                <button onclick="scanPlexLibrary('${lib.key}')" class="bg-blue-600 hover:bg-blue-700 px-2 py-1 rounded text-xs w-full transition">
                    Scan
                </button>
            </div>
        `).join('');
        
        // Tautulli Users
        const users = await api.getTautulliUsers();
        document.getElementById('tautulli-users').innerHTML = users.users.map(u => `
            <div class="bg-gray-700/20 rounded p-3">
                <div class="font-medium">${u.username}</div>
                <div class="text-xs text-gray-400">Plays: ${u.plays} | ${(u.duration / 3600).toFixed(1)}h</div>
            </div>
        `).join('');
        
        // Recent Streams
        const history = await api.getTautulliHistory(10);
        document.getElementById('plex-history').innerHTML = history.history.map(h => `
            <div class="bg-gray-700/20 rounded p-3">
                <div class="text-sm font-medium truncate">${h.title}</div>
                <div class="text-xs text-gray-400">${h.user}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading Plex data:', error);
        showToast('Failed to load Plex data', 'error');
    }
}

// Restart service
async function restartService(service) {
    try {
        let promise;
        switch (service) {
            case 'plex':
                promise = api.restartPlexServer();
                break;
            case 'tautulli':
                promise = api.restartTautulli();
                break;
            case 'utorrent':
                // uTorrent restart through Docker
                promise = Promise.resolve();
                showToast('Use Docker controls to restart uTorrent', 'info');
                return;
            case 'rutorrent':
                promise = api.restartRuTorrent();
                break;
            default:
                return;
        }
        
        await promise;
        showToast(`${service} restart initiated`, 'success');
        setTimeout(() => loadPlexData(), 2000);
    } catch (error) {
        showToast('Failed to restart service', 'error');
    }
}

// Scan Plex library
async function scanPlexLibrary(libKey) {
    try {
        await api.scanPlexLibrary(libKey);
        showToast('Library scan started', 'success');
    } catch (error) {
        showToast('Failed to start library scan', 'error');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserInfo();
    await loadSystemStats();
    await loadContainers();
    
    // Update stats every 5 seconds
    setInterval(loadSystemStats, 5000);
    setInterval(loadContainers, 10000);
});
