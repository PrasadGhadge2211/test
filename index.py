from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "")
client = MongoClient(MONGO_URI)
db = client["test_db"]
collection = db["test_collection"]

@app.route("/")
def home():
    return jsonify({"message": "MongoDB + Flask + Vercel is working!"})

@app.route("/add/<name>")
def add_name(name):
    collection.insert_one({"name": name})
    return jsonify({"status": "success", "name_added": name})

@app.route("/list")
def list_names():
    names = list(collection.find({}, {"_id": 0}))
    return jsonify(names)

if __name__ == "__main__":
    app.run(debug=True)
