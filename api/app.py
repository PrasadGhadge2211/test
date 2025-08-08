from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from pymongo import MongoClient
import os

load_dotenv()
app = Flask(__name__)
MONGO_URI = os.environ.get("MONGODB_URI", "")
client = MongoClient(MONGO_URI)
db = client['pharmacy_db']

@app.route('/')
def dashboard():
    return jsonify({"message":"working"})
if __name__ == '__main__':
    app.run(debug=True)
