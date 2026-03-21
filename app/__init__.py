import os
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key' 

from app.main import *
from app.auth import *
from app.memories import *
from app.ai import *
from app.reminders import *
from app.familiar import *
from app.assessment import *