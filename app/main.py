from flask import Flask, request, jsonify
from app import app, UPLOAD_FOLDER
from flask import send_from_directory

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    print(UPLOAD_FOLDER)
    print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Server up and running'}), 200