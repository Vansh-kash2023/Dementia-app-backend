import uuid
from flask import request, jsonify
from app import app
import base64
import cloudinary.uploader
from app.models.models import db, Memory, memory_schema, memories_schema
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

@app.route('/memories', methods=['POST'])
def add_memory():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'message': 'Image data is required!'}), 400

        image_data = data['image']
        mime_type = 'image/jpeg'
        
        if ',' in image_data:
            header, image_data = image_data.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
        
        if mime_type not in ['image/jpeg', 'image/png']:
            return jsonify({'message': 'Unsupported image type. Only JPEG and PNG allowed!'}), 400
        
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'message': 'Invalid base64 encoding', 'error': str(e)}), 400

        try:
            upload_result = cloudinary.uploader.upload(
                image_bytes,
                folder=app.config['CLOUDINARY_FOLDER'],
                public_id=f"memory_{user_id}_{uuid.uuid4().hex}",
                resource_type='image'
            )
            image_url = upload_result['secure_url']
        except Exception as e:
            return jsonify({'message': 'Failed to upload image to cloud storage', 'error': str(e)}), 500
        
        new_memory = Memory(
            user_id=user_id,
            title=data.get('title', ''),
            description=data.get('description', ''),
            image_url=image_url,
            date=data.get('date', '')
        )

        try:
            db.session.add(new_memory)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': 'Database error', 'error': str(e)}), 500

        return jsonify({
            'message': 'Memory saved successfully!',
            'memory': {
                'id': new_memory.id,
                'title': new_memory.title,
                'description': new_memory.description,
                'image_url': new_memory.image_url,
                'date': new_memory.date
            }
        }), 201

    except Exception as e:
        app.logger.error(f'Error saving memory: {str(e)}')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@app.route('/memories', methods=['GET'])
def get_memories():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    
    user_memories = Memory.query.filter_by(user_id=user_id).all()
    
    return memories_schema.jsonify(user_memories)

@app.route('/memories/<int:id>', methods=['GET'])
def get_memory(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    memory = Memory.query.filter_by(id=id, user_id=user_id).first_or_404()
    return memory_schema.jsonify(memory)

@app.route('/memories/<int:id>', methods=['PUT'])
def update_memory(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    memory = Memory.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json() or {}

    memory.title = data.get('title', memory.title)
    memory.description = data.get('description', memory.description)
    memory.image_url = data.get('image_url', memory.image_url)
    memory.date = data.get('date', memory.date)

    db.session.commit()
    return memory_schema.jsonify(memory)

@app.route('/memories/<int:id>', methods=['DELETE'])
def delete_memory(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    memory = Memory.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(memory)
    db.session.commit()
    return jsonify({'message': 'Memory deleted successfully'})