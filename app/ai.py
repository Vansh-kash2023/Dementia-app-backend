from app.models.models import User, Memory, Reminder, FamiliarFace, Answer
from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from google import genai
import datetime


@app.route("/gen_ai", methods=["POST"])
def gen_ai():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    
    data = request.get_json()
    user_message = data.get("message", "")

    user = User.query.get(user_id)
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    memories = Memory.query.filter_by(user_id=user_id).all()
    familiar_faces = FamiliarFace.query.filter_by(user_id=user_id).all()
    answers = Answer.query.filter_by(user_id=user_id).all()
    current_time = datetime.datetime.now()
    context = {
        "current_time": current_time,
        "purpose":"we want answer to given question in very few lines probably 3-4 lines no more and there will be no mention of context and any technical jargons direct text output for dementia patients",
        "user_id": user.id,
        "user_info": {
            "name": user.name,
            "email": user.email,
            "emergency_contact": user.emergency_contact,
 
        },
        "context": {
            "active_reminders": [
                {
                    "id": reminder.id,
                    "title": reminder.title,
                    "time": reminder.time,
                    "date": reminder.date,
                    "description": reminder.description,
                    "status": reminder.status
                }
                for reminder in reminders
            ],
            "memories": [
                {
                    "id": memory.id,
                    "title": memory.title,
                    "description": memory.description,
                    "image_url": memory.image_url,
                    "date": memory.date
                }
                for memory in memories
            ],
            "familiar_faces": [
                {
                    "id": face.id,
                    "name": face.name,
                    "relationship": face.relationship,
                    "image_url": face.image_url
                }
                for face in familiar_faces
            ],
         
        },
 
  
    }

    client = genai.Client(api_key="AIzaSyCYAQMATgLJY0dcTV9wBNKarrGzxFSg_Ek")

    input_contents = [
        user_message,  
        str(context)   
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_contents
    )

    return jsonify({"message": response.text})


@app.route("/generate_report", methods=["GET"])
def generate_report():
    verify_jwt_in_request()
    user_id = get_jwt_identity()

    answers = Answer.query.filter_by(user_id=user_id).all()

    if not answers:
        return jsonify({"error": "No answers found for this user"}), 404

    report = {
        "user_id": user_id,
        "total_answers": len(answers),
        "correct_answers": sum(1 for answer in answers if answer.scored == 1),
        "incorrect_answers": sum(1 for answer in answers if answer.scored == 0),
        "answers": [
            {
                "id": answer.id,
                "question": answer.question,
                "answer_text": answer.answer_text,
                "scored": bool(answer.scored),
                "created_at": answer.created_at.isoformat()
            }
            for answer in answers
        ],
        "summary": {
            "accuracy": f"{(sum(1 for answer in answers if answer.scored == 1) / len(answers)) * 100:.2f}%",
            "most_common_question": max(
                set(answer.question for answer in answers),
                key=lambda q: sum(1 for answer in answers if answer.question == q)
            ),
            "last_answer_date": max(answer.created_at for answer in answers).isoformat()
        }
    }

    return jsonify(report)
