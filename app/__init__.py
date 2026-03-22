import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
import cloudinary


def _required_env(name):
	value = os.getenv(name)
	if value is None or value.strip() == "":
		raise RuntimeError(f"Missing required environment variable: {name}")
	return value


def _parse_bool(value, name):
	normalized = value.strip().lower()
	if normalized in {"1", "true", "yes", "on"}:
		return True
	if normalized in {"0", "false", "no", "off"}:
		return False
	raise RuntimeError(f"Invalid boolean value for {name}: {value}")


def _optional_env(name, default_value):
	value = os.getenv(name)
	if value is None or value.strip() == "":
		return default_value
	return value


def _parse_csv(value):
	return [item.strip() for item in value.split(',') if item.strip()]

app = Flask(__name__)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))

app.config['JWT_SECRET_KEY'] = _required_env('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = _required_env('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = _parse_bool(_required_env('SQLALCHEMY_TRACK_MODIFICATIONS'), 'SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['GEMINI_API_KEY'] = _required_env('GEMINI_API_KEY')
app.config['HOST'] = _required_env('HOST')
app.config['PORT'] = int(_required_env('PORT'))
app.config['DEBUG'] = _parse_bool(_required_env('FLASK_DEBUG'), 'FLASK_DEBUG')
app.config['ENV'] = _optional_env('FLASK_ENV', 'development')
app.config['CLOUDINARY_CLOUD_NAME'] = _required_env('CLOUDINARY_CLOUD_NAME')
app.config['CLOUDINARY_API_KEY'] = _required_env('CLOUDINARY_API_KEY')
app.config['CLOUDINARY_API_SECRET'] = _required_env('CLOUDINARY_API_SECRET')
app.config['CLOUDINARY_FOLDER'] = _optional_env('CLOUDINARY_FOLDER', 'dementia-app')

cors_allowed_origins = _optional_env('CORS_ALLOWED_ORIGINS', '')
if app.config['ENV'].lower() == 'production':
	if not cors_allowed_origins.strip():
		raise RuntimeError('Missing required environment variable: CORS_ALLOWED_ORIGINS in production')
	cors_origins = _parse_csv(cors_allowed_origins)
else:
	cors_origins = _parse_csv(cors_allowed_origins)
	if not cors_origins:
		cors_origins = ['*']

CORS(app, resources={r"/*": {"origins": cors_origins}})

cloudinary.config(
	cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
	api_key=app.config['CLOUDINARY_API_KEY'],
	api_secret=app.config['CLOUDINARY_API_SECRET'],
	secure=True
)
jwt = JWTManager(app)

# Explicit migrations replace implicit db.create_all for safer schema changes.
from app.models.models import db
migrate = Migrate(app, db)

from app.main import *
from app.auth import *
from app.memories import *
from app.ai import *
from app.reminders import *
from app.familiar import *
from app.assessment import *