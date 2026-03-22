from app import app
from flask import request, jsonify
from app.models.models import Answer, db, answers_schema
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request # type: ignore

@app.route('/answers', methods=['POST'])
def add_answer():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        data = request.get_json()

        # Ensure data is a list
        if not isinstance(data, list):
            return jsonify({"message": "Input should be an array of answer objects!"}), 400

        new_answers = []

        for answer_data in data:
            new_answer = Answer(
                answer_text=answer_data["answer_text"],
                question=answer_data["question"],
                user_id=user_id,
                scored=answer_data.get("scored", 0),
            )
            new_answers.append(new_answer)

        db.session.add_all(new_answers)
        db.session.commit()

        return answers_schema.jsonify(new_answers), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error saving answers", "error": str(e)}), 500

    
@app.route('/answers', methods=['GET'])
def get_answers():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    all_answers = Answer.query.filter_by(user_id=user_id).all()
    return answers_schema.jsonify(all_answers)