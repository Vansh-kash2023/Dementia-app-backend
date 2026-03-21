from flask import request, jsonify
from app import app
from app.models.models import Reminder, db, reminder_schema, reminders_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request


@app.route('/reminders', methods=['POST'])
def add_reminder():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    data = request.get_json()
    new_reminder = Reminder(
        title=data.get('title'),
        description=data.get('description', ''),
        time=data.get('time'),
        date=data.get('date', ''),
        repeat=data.get('repeat', ''),
        status=data.get('status', False),
        user_id=user_id
        
    )
    db.session.add(new_reminder)
    db.session.commit()
    return reminder_schema.jsonify(new_reminder), 201

@app.route('/reminders', methods=['GET'])
def get_reminders():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    all_reminders = Reminder.query.filter_by(user_id=user_id).all()
    return reminders_schema.jsonify(all_reminders)

@app.route('/reminders/<int:id>', methods=['GET'])
def get_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    return reminder_schema.jsonify(reminder)

@app.route('/reminders/<int:id>', methods=['PUT'])
def update_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    data = request.get_json()

    reminder.title = data.get('title', reminder.title)
    reminder.description = data.get('description', reminder.description)
    reminder.time = data.get('time', reminder.time)
    reminder.date = data.get('date', reminder.date)
    reminder.repeat = data.get('repeat', reminder.repeat)
    reminder.status = data.get('status', reminder.status)

    db.session.commit()
    return reminder_schema.jsonify(reminder)

@app.route('/reminders/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'message': 'Reminder deleted successfully'})
