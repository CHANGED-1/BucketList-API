"""Application factory and initialization."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()


def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    swagger.init_app(app)
    
    # Register blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # Import models to ensure they're registered
    from app.models import User, BucketList, Item
    
    @app.route('/')
    def index():
        """Root endpoint."""
        return {
            'message': 'Welcome to BucketList API',
            'version': 'v1',
            'endpoints': {
                'auth': '/api/v1/auth',
                'bucketlists': '/api/v1/bucketlists',
                'docs': '/apidocs'
            }
        }
    
    return app