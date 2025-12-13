🎛️ Seedbox Control Panel (Beta)
This is a lightweight, unified dashboard to manage your media stack. Start, stop, and monitor Sonarr, Radarr, and your Torrent Client (qBittorrent/Transmission) from a single interface.

⚠️ Beta Warning: This project is currently in early development. Features may be unstable. Please report any bugs in the Issues tab.

🚀 Key Features
Unified Service Control: Restart or shutdown services directly from the dashboard.

Live Status Monitoring: Real-time health checks for Sonarr, Radarr, and download clients.

Queue Management: View active downloads and pause/resume torrents.

System Stats: Simple resource usage display (CPU/RAM).

🛠️ Quick Start
Prerequisites
Python 3.9+ or Node.js 16+ (depending on your backend)

API Keys for Sonarr, Radarr, and your Torrent Client

Installation
Clone the repository

bash
git clone https://github.com/yourusername/seedbox-control-panel.git
cd seedbox-control-panel
Install dependencies

bash
pip install -r requirements.txt
# OR for Node:
# npm install
Configure Environment
Create a .env file in the root directory:

text
SONARR_URL=http://localhost:8989
SONARR_API_KEY=your_sonarr_api_key

RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_radarr_api_key

TORRENT_CLIENT=qbittorrent
TORRENT_URL=http://localhost:8080
TORRENT_USER=admin
TORRENT_PASS=adminadmin
Run the Application

bash
python app.py
# OR for Node:
# npm start
🤝 Contributing
Feedback is vital during this beta phase!

Found a bug? Open an Issue.

Want to fix it? Submit a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.
