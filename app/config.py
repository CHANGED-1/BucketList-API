"""Application configuration settings."""
import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all domains


class Config:
    """Base configuration class."""
    
    # Secret key for sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Pagination
    DEFAULT_PAGE_LIMIT = 20
    MAX_PAGE_LIMIT = 100
    
    # CORS
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///bucketlist_dev.db'
    )
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bucketlist_test.db'
    # Use shorter token expiry for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/bucketlist'
    )
    # In production, ensure these are set via environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}