"""BucketList Item endpoints."""
from flask import request, jsonify
from app import db
from app.models import BucketList, Item
from app.auth.token_handler import token_required
from app.api.v1 import api_v1


@api_v1.route('/bucketlists/<int:id>/items', methods=['POST'])
@token_required
def create_item(current_user, id):
    """
    Create a new item in bucket list.
    ---
    tags:
      - Items
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
          required:
            - name
          properties:
            name:
              type: string
            done:
              type: boolean
    responses:
      201:
        description: Item created successfully
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
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Item name is required'}), 400
    
    item = Item(
        name=data['name'],
        bucketlist_id=bucketlist.id,
        done=data.get('done', False)
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'message': 'Item created successfully',
        'item': item.to_dict()
    }), 201


@api_v1.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@token_required
def update_item(current_user, id, item_id):
    """
    Update a bucket list item.
    ---
    tags:
      - Items
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
      - name: item_id
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
            done:
              type: boolean
    responses:
      200:
        description: Item updated successfully
      404:
        description: Item or bucket list not found
    """
    bucketlist = BucketList.query.filter_by(
        id=id,
        created_by=current_user.id
    ).first()
    
    if not bucketlist:
        return jsonify({'message': 'Bucket list not found'}), 404
    
    item = Item.query.filter_by(
        id=item_id,
        bucketlist_id=bucketlist.id
    ).first()
    
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        item.name = data['name']
    if 'done' in data:
        item.done = data['done']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Item updated successfully',
        'item': item.to_dict()
    }), 200


@api_v1.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, id, item_id):
    """
    Delete an item in bucket list.
    ---
    tags:
      - Items
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
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Item deleted successfully
      404:
        description: Item or bucket list not found
    """
    bucketlist = BucketList.query.filter_by(
        id=id,
        created_by=current_user.id
    ).first()
    
    if not bucketlist:
        return jsonify({'message': 'Bucket list not found'}), 404
    
    item = Item.query.filter_by(
        id=item_id,
        bucketlist_id=bucketlist.id
    ).first()
    
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item deleted successfully'}), 200