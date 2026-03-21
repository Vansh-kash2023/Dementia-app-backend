import base64
import os
import uuid
from app import UPLOAD_FOLDER, app
from flask import request, jsonify, url_for
from app import app
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
    file_ext = 'png' if 'png' in mime_type else 'jpg'
    
    try:
        image_bytes = base64.b64decode(image_data)
    except Exception as e:
        return jsonify({'message': 'Invalid base64 encoding', 'error': str(e)}), 400
    filename = f"memory_{user_id}_{uuid.uuid4().hex}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(file_path, 'wb') as img_file:
            img_file.write(image_bytes)
    except IOError as e:
        return jsonify({'message': 'Failed to save image', 'error': str(e)}), 500
    image_url = url_for('uploaded_file', filename=filename, _external=True)
        
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
    face = FamiliarFace.query.get_or_404(id)
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['PUT'])
def update_familiar_face(id):
    face = FamiliarFace.query.get_or_404(id)
    data = request.get_json()

    face.name = data.get('name', face.name)
    face.relationship = data.get('relationship', face.relationship)
    face.photo_url = data.get('photo_url', face.photo_url)
    face.voice_note_url = data.get('voice_note_url', face.voice_note_url)

    db.session.commit()
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['DELETE'])
def delete_familiar_face(id):
    face = FamiliarFace.query.get_or_404(id)
    db.session.delete(face)
    db.session.commit()
    return jsonify({'message': 'Familiar face deleted successfully'})