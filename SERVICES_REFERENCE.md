# New Services Quick Reference

## Service URLs & Configuration

### Plex Media Server
```
Web UI: http://localhost:32400/web/
API: http://localhost:32400/
Token: X-Plex-Token header
Doc: https://www.plex.tv/en/
```

**Config in SeedBox Panel:**
```
PLEX_URL=http://localhost:32400
PLEX_TOKEN=your_token_here
```

---

### Tautulli (Plex Monitoring)
```
Web UI: http://localhost:8181/
API: http://localhost:8181/api/v2
Port: 8181 (default)
Doc: https://tautulli.com/
```

**Config in SeedBox Panel:**
```
TAUTULLI_URL=http://localhost:8181
TAUTULLI_API_KEY=your_key_here
```

---

### uTorrent
```
Web UI: http://localhost:8080/
API: RPC API
Port: 8080 (default)
Doc: https://www.bittorrent.com/
```

**Config in SeedBox Panel:**
```
UTORRENT_URL=http://localhost:8080
UTORRENT_USERNAME=admin
UTORRENT_PASSWORD=your_password
```

---

### ruTorrent (rtorrent Web Interface)
```
Web UI: http://localhost:8081/
API: HTTP/XMLRPC
Port: 8081 (default)
Daemon: rtorrent
Doc: https://github.com/rakshasa/rtorrent/
```

**Config in SeedBox Panel:**
```
RUTORRENT_URL=http://localhost:8081
RUTORRENT_USERNAME=your_username
RUTORRENT_PASSWORD=your_password
```

---

## API Endpoints at a Glance

### Plex `/api/plex`
```
GET  /health                    → Check connection
GET  /status                    → Server info
GET  /libraries                 → List all libraries
GET  /sessions                  → Active streams
GET  /streams                   → Stream history
POST /restart                   → Restart server
POST /optimize                  → Optimize DB
POST /libraries/{key}/scan      → Scan library
```

### Tautulli `/api/tautulli`
```
GET  /health                    → Check connection
GET  /status                    → Server info
GET  /activity                  → Current activity
GET  /stats                     → Statistics
GET  /users                     → User list
GET  /libraries                 → Library stats
GET  /history                   → Play history
GET  /server-info               → Plex server info
POST /restart                   → Restart service
```

### uTorrent `/api/utorrent`
```
GET  /health                    → Check connection
GET  /status                    → Server status
GET  /torrents                  → List torrents
GET  /stats                     → Torrent stats
GET  /bandwidth                 → Bandwidth stats
POST /torrents/{hash}/start     → Start torrent
POST /torrents/{hash}/stop      → Stop torrent
POST /torrents/{hash}/pause     → Pause torrent
POST /torrents/{hash}/resume    → Resume torrent
POST /torrents/{hash}/remove    → Remove torrent
POST /torrents/add-url          → Add torrent
```

### ruTorrent `/api/rutorrent`
```
GET  /health                    → Check connection
GET  /status                    → Server status
GET  /torrents                  → List torrents
GET  /stats                     → Torrent stats
GET  /bandwidth                 → Bandwidth stats
POST /torrents/{hash}/start     → Start torrent
POST /torrents/{hash}/stop      → Stop torrent
POST /torrents/{hash}/pause     → Pause torrent
POST /torrents/{hash}/resume    → Resume torrent
POST /torrents/{hash}/remove    → Remove torrent
POST /restart                   → Restart rtorrent
```

---

## Getting Tokens & API Keys

### Plex Token
1. Go to http://localhost:32400/web/
2. Login to your Plex account
3. Settings → Remote Access → Verify Server
4. Check browser developer tools (Network tab) for X-Plex-Token header
5. Or use: `curl http://localhost:32400/identity -H "Accept: application/json"`

### Tautulli API Key
1. Go to http://localhost:8181/
2. Click Settings (top right)
3. Click API
4. Copy API Key

### uTorrent Credentials
- Set in uTorrent WebUI settings
- Default usually: admin/password
- Verify in http://localhost:8080/

### ruTorrent Credentials
- Set in ruTorrent/rtorrent configuration
- Check .rtorrent.rc for settings
- Test access: http://localhost:8081/

---

## Common Commands

### Test Connectivity
```bash
# Plex
curl -H "X-Plex-Token: YOUR_TOKEN" http://localhost:32400/

# Tautulli
curl "http://localhost:8181/api/v2?apikey=YOUR_KEY&cmd=get_tautulli_info"

# uTorrent
curl -u admin:password http://localhost:8080/gui/?list=1

# ruTorrent
curl http://localhost:8081/php/getglobalstat.php
```

### Using SeedBox Panel API

```bash
# Get auth token
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' | jq -r .access_token)

# Get Plex status
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/plex/status

# Get Tautulli activity
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/tautulli/activity

# Get uTorrent torrents
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/utorrent/torrents

# Start ruTorrent torrent
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/rutorrent/torrents/HASH/start
```

---

## Troubleshooting

### Service Not Showing Data
1. Check `.env` configuration is correct
2. Verify service is running: `curl http://service:port`
3. Check credentials are valid
4. Review application logs: `tail -f seedbox.log`
5. Check audit logs in database

### Connection Refused
1. Verify service port is correct in `.env`
2. Check service is actually running: `docker ps`
3. Check firewall allows connection
4. Verify network connectivity: `ping hostname`

### API Key Issues
1. Re-generate key in service settings
2. Update `.env` with new key
3. Restart SeedBox panel
4. Test connectivity again

### Authentication Fails
1. Verify credentials in `.env`
2. Check service's access control settings
3. Ensure API is enabled in service settings
4. Try connecting directly to service

---

## Docker Compose Example

```yaml
version: '3.8'
services:
  plex:
    image: plexinc/pms-docker:latest
    ports:
      - "32400:32400"
    environment:
      - PLEX_CLAIM=your_claim_token
  
  tautulli:
    image: tautulli/tautulli:latest
    ports:
      - "8181:8181"
  
  utorrent:
    image: binhex/arch-utserver:latest
    ports:
      - "8080:8080"
  
  rutorrent:
    image: easypi/rtorrent-rutorrent:latest
    ports:
      - "8081:8081"
```

---

## Performance Tips

1. **Plex**: Reduce library size for faster scans
2. **Tautulli**: Enable caching in settings
3. **Torrents**: Limit concurrent connections
4. **uTorrent**: Use bandwidth limits to prevent throttling
5. **ruTorrent**: Monitor ratio to prevent issues

---

## Security Best Practices

1. Use strong API keys and passwords
2. Store credentials in `.env`, never in code
3. Use HTTPS in production
4. Restrict firewall rules to admin users only
5. Change default admin password
6. Monitor audit logs regularly
7. Enable 2FA where available
8. Backup database regularly

---

## File Locations

### Service Files
```
Plex config: ~/.plex/Library/
Tautulli config: ~/.tautulli/
uTorrent config: ~/.utorrent/
ruTorrent config: ~/.rtorrent.rc
```

### SeedBox Panel
```
Backend: ./backend/
Frontend: ./frontend/
Logs: ./seedbox.log
Database: ./seedbox.db
Config: ./.env
```

---

## Useful Links

- **Plex**: https://www.plex.tv/
- **Tautulli**: https://tautulli.com/
- **uTorrent**: https://www.bittorrent.com/
- **ruTorrent**: https://github.com/rakshasa/rtorrent/
- **rtorrent**: https://rakshasa.github.io/rtorrent/
- **SeedBox**: https://github.com/slconrad/SeedBox-Project

---

**Last Updated**: December 2025
**Version**: 2.0.0
