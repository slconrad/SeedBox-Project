"""
Main Flask application factory and configuration
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from models import db, User
from config import config
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    socketio = SocketIO(app, cors_allowed_origins="*") if app.config.get('ENABLE_WEBSOCKET') else None
    
    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE', 'seedbox.log'),
            maxBytes=10240000, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    # Register blueprints
    from routes import (api_docker, api_system, api_auth, api_radarr, api_sonarr, 
                        api_overseerr, api_plex, api_tautulli, api_utorrent, api_rutorrent)
    app.register_blueprint(api_auth.bp)
    app.register_blueprint(api_docker.bp)
    app.register_blueprint(api_system.bp)
    app.register_blueprint(api_radarr.bp)
    app.register_blueprint(api_sonarr.bp)
    app.register_blueprint(api_overseerr.bp)
    app.register_blueprint(api_plex.bp)
    app.register_blueprint(api_tautulli.bp)
    app.register_blueprint(api_utorrent.bp)
    app.register_blueprint(api_rutorrent.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # JWT error handlers
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Missing authorization token'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({'error': 'Token has expired'}), 401
    
    # Frontend routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    # Create tables and add default admin user
    with app.app_context():
        db.create_all()
        
        # Create default admin if doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@seedbox.local',
                role='admin',
                is_active=True
            )
            admin.set_password('admin')  # CHANGE THIS IN PRODUCTION
            db.session.add(admin)
            db.session.commit()
            logger.info("Default admin user created. Username: admin, Password: admin")
    
    logger.info(f"SeedBox Control Panel initialized with config: {config_name}")
    return app, socketio if socketio else None


if __name__ == '__main__':
    app, socketio = create_app()
    
    if socketio:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
