"""BucketList endpoints."""
from flask import request, jsonify
from app import db
from app.models import BucketList
from app.auth.token_handler import token_required
from app.api.v1 import api_v1


@api_v1.route('/bucketlists', methods=['POST'])
@token_required
def create_bucketlist(current_user):
    """
    Create a new bucket list.
    ---
    tags:
      - BucketLists
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    responses:
      201:
        description: Bucket list created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Bucket list name is required'}), 400
    
    bucketlist = BucketList(
        name=data['name'],
        created_by=current_user.id
    )
    
    db.session.add(bucketlist)
    db.session.commit()
    
    return jsonify({
        'message': 'Bucket list created successfully',
        'bucketlist': bucketlist.to_dict()
    }), 201


@api_v1.route('/bucketlists', methods=['GET'])
@token_required
def get_bucketlists(current_user):
    """
    Get all bucket lists for the current user.
    ---
    tags:
      - BucketLists
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: limit
        in: query
        type: integer
        description: Number of results per page (default 20, max 100)
      - name: page
        in: query
        type: integer
        description: Page number (default 1)
      - name: q
        in: query
        type: string
        description: Search query for bucket list name
    responses:
      200:
        description: List of bucket lists
    """
    # Get pagination parameters
    limit = request.args.get('limit', 20, type=int)
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str)
    
    # Validate limit
    from flask import current_app
    max_limit = current_app.config['MAX_PAGE_LIMIT']
    limit = min(limit, max_limit)
    
    # Build query
    query = BucketList.query.filter_by(created_by=current_user.id)
    
    # Apply search filter
    if search_query:
        query = query.filter(BucketList.name.ilike(f'%{search_query}%'))
    
    # Paginate
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    bucketlists = [bl.to_dict() for bl in pagination.items]
    
    return jsonify({
        'bucketlists': bucketlists,
        'total': pagination.total,
        'page': page,
        'per_page': limit,
        'pages': pagination.pages
    }), 200


@api_v1.route('/bucketlists/<int:id>', methods=['GET'])
@token_required
def get_bucketlist(current_user, id):
    """
    Get a single bucket list.
    ---
    tags:
      - BucketLists
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Bucket list details
      404:
        description: Bucket list not found
    """
    bucketlist = BucketList.query.filter_by(
        id=id,
        created_by=current_user.id
    ).first()
    
    if not bucketlist:
        return jsonify({'message': 'Bucket list not found'}), 404
    
    return jsonify(bucketlist.to_dict()), 200


@api_v1.route('/bucketlists/<int:id>', methods=['PUT'])
@token_required
def update_bucketlist(current_user, id):
    """
    Update a bucket list.
    ---
    tags:
      - BucketLists
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
    responses:
      200:
        description: Bucket list updated successfully
      404:
        description: Bucket list not found
    """
    bucketlist = BucketList.query.filter_by(
        id=id,
        created_by=current_user.id
    ).first()
    
    if not bucketlist:
        return jsonify({'message': 'Bucket list not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        bucketlist.name = data['name']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Bucket list updated successfully',
        'bucketlist': bucketlist.to_dict()
    }), 200


@api_v1.route('/bucketlists/<int:id>', methods=['DELETE'])
@token_required
def delete_bucketlist(current_user, id):
    """
    Delete a bucket list.
    ---
    tags:
      - BucketLists
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Bucket list deleted successfully
      404:
        description: Bucket list not found
    """
    bucketlist = BucketList.query.filter_by(
        id=id,
        created_by=current_user.id
    ).first()
    
    if not bucketlist:
        return jsonify({'message': 'Bucket list not found'}), 404
    
    db.session.delete(bucketlist)
    db.session.commit()
    
    return jsonify({'message': 'Bucket list deleted successfully'}), 200