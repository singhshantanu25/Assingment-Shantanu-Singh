from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection with authentication
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")

if MONGO_USER and MONGO_PASS:
    client = MongoClient(
        MONGODB_URI,
        username=MONGO_USER,
        password=MONGO_PASS,
        authSource='admin'
    )
else:
    client = MongoClient(MONGODB_URI)

db = client.flask_db
collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
