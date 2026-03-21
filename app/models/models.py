from datetime import datetime
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    emergency_contact = db.Column(db.String(120), unique=False, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    
    
class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class MemorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memory

memory_schema = MemorySchema()
memories_schema = MemorySchema(many=True)
    
    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    repeat = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class ReminderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reminder

reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)

class FamiliarFace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)  
    image_url = db.Column(db.String(255), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class FamiliarFaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FamiliarFace

face_schema = FamiliarFaceSchema()
faces_schema = FamiliarFaceSchema(many=True)
 

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    answer_text = db.Column(db.Text, nullable=True)
    question = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    scored = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer

answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)

with app.app_context():
    db.create_all()
