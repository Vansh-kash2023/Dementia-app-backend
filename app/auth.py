from flask import request, jsonify
from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt_identity, verify_jwt_in_request # type: ignore
import datetime
from app import app
from app.models.models import db, User

bcrypt = Bcrypt(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    emergency_contact = data.get('emergency_contact')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password_hash=hashed_password,emergency_contact=emergency_contact,name=name)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id),expires_delta=datetime.timedelta(days=10))
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'User not found!'}), 401

@app.route('/profile', methods=['GET'])
def get_profile():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    print(user_id)
    user = User.query.get(user_id)
    return jsonify({
            "name": user.name,
            "email": user.email,
            "emergency_contact": user.emergency_contact,
        }), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome {current_user["username"]}!'}), 200


