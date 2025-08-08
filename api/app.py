from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
import os
from dotenv import load_dotenv
import certifi
import pytz

load_dotenv()
ca = certifi.where()
app = Flask(__name__, static_folder='static')
MONGO_URI = os.environ.get("MONGODB_URI", "")
client = MongoClient(MONGO_URI, tlsCAFile=ca)
db = client['pharmacy_db']
LOCAL_TIMEZONE = pytz.timezone('Asia/Kolkata')

@app.template_filter('local_datetime')
def local_datetime_filter(dt):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(LOCAL_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def dashboard():
    return jsonify({"message":"working"})
if __name__ == '__main__':
    app.run(debug=True)
