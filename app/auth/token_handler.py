"""JWT token handling utilities."""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User


def generate_token(user_id):
    """Generate JWT token for user."""
    try:
        payload = {
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        return token
    except Exception as e:
        return str(e)


def decode_token(token):
    """Decode JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please login again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please login again.'


def token_required(f):
    """Decorator to protect routes with token authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        user_id = decode_token(token)
        
        if isinstance(user_id, str):
            return jsonify({'message': user_id}), 401
        
        # Get user from database
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function