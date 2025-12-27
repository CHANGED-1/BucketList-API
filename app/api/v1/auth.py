"""Authentication endpoints."""
from flask import request, jsonify
from app import db
from app.models import User
from app.auth.token_handler import generate_token
from app.api.v1 import api_v1


@api_v1.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - username
            - password
          properties:
            email:
              type: string
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or user already exists
    """
    data = request.get_json()
    
    # Validate input
    if not data or not all(k in data for k in ['email', 'username', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 400
    
    # Create user
    user = User(
        email=data['email'],
        username=data['username'],
        password=data['password']
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201


@api_v1.route('/auth/login', methods=['POST'])
def login():
    """
    Login user.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    
    # Validate input
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200