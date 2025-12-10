// Service Worker for SeedBox Control Panel PWA
const CACHE_NAME = 'seedbox-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
];

// Install event - cache essential assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching app shell');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .catch(err => console.log('Cache addAll error:', err))
  );
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;

  // Skip cross-origin requests
  if (!request.url.startsWith(self.location.origin)) {
    return;
  }

  // For HTML requests, use network-first strategy
  if (request.headers.get('Accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response && response.status === 200) {
            const clonedResponse = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, clonedResponse);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(request)
            .then(response => response || caches.match('./index.html'));
        })
    );
  } else {
    // For other assets, use cache-first strategy
    event.respondWith(
      caches.match(request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(request)
            .then(response => {
              // Cache successful responses
              if (response && response.status === 200 && request.method === 'GET') {
                const clonedResponse = response.clone();
                caches.open(CACHE_NAME).then(cache => {
                  cache.put(request, clonedResponse);
                });
              }
              return response;
            })
            .catch(() => {
              // Return offline page or fallback
              return new Response('Offline - Resource not available', {
                status: 503,
                statusText: 'Service Unavailable',
                headers: new Headers({
                  'Content-Type': 'text/plain'
                })
              });
            });
        })
    );
  }
});

// Background Sync for offline app control
self.addEventListener('sync', event => {
  if (event.tag === 'sync-apps') {
    event.waitUntil(syncApps());
  }
});

async function syncApps() {
  try {
    // Sync any pending app actions
    const response = await fetch('/api/apps');
    return response.json();
  } catch (error) {
    console.log('Background sync failed:', error);
  }
}

// Push notifications support
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'SeedBox notification',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect fill="%230f3460" width="192" height="192"/><rect fill="%233B82F6" x="40" y="40" width="112" height="112" rx="8"/><text x="96" y="120" font-size="80" fill="%23ffffff" font-family="Arial" text-anchor="middle" font-weight="bold">SB</text></svg>',
    badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect fill="%233B82F6" width="96" height="96"/><text x="48" y="65" font-size="48" fill="%23ffffff" font-family="Arial" text-anchor="middle" font-weight="bold">SB</text></svg>',
    tag: 'seedbox-notification',
    requireInteraction: false
  };

  event.waitUntil(
    self.registration.showNotification('SeedBox Control Panel', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' })
      .then(clientList => {
        for (let i = 0; i < clientList.length; i++) {
          const client = clientList[i];
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('./');
        }
      })
  );
});

// Message handler for client communication
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
