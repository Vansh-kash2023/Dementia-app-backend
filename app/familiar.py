import base64
import uuid
from app import app
from flask import request, jsonify
import cloudinary.uploader
from app.models.models import FamiliarFace, db, face_schema, faces_schema
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

@app.route('/faces', methods=['POST'])
def add_familiar_face():
    data = request.get_json()
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    
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
            public_id=f"face_{user_id}_{uuid.uuid4().hex}",
            resource_type='image'
        )
        image_url = upload_result['secure_url']
    except Exception as e:
        return jsonify({'message': 'Failed to upload image to cloud storage', 'error': str(e)}), 500
        
    new_face = FamiliarFace(
        user_id=user_id,
        name=data.get('name'),
        relationship=data.get('relationship'),
        image_url=image_url,
    )
    db.session.add(new_face)
    db.session.commit()
    return face_schema.jsonify(new_face), 201

@app.route('/faces', methods=['GET'])
def get_familiar_faces():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    all_faces = FamiliarFace.query.filter_by(user_id=user_id).all()
    return faces_schema.jsonify(all_faces)

@app.route('/faces/<int:id>', methods=['GET'])
def get_familiar_face(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    face = FamiliarFace.query.filter_by(id=id, user_id=user_id).first_or_404()
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['PUT'])
def update_familiar_face(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    face = FamiliarFace.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json() or {}

    face.name = data.get('name', face.name)
    face.relationship = data.get('relationship', face.relationship)
    face.image_url = data.get('image_url', face.image_url)

    db.session.commit()
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['DELETE'])
def delete_familiar_face(id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    face = FamiliarFace.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(face)
    db.session.commit()
    return jsonify({'message': 'Familiar face deleted successfully'})