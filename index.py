from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Flask + Vercel is working!"})

@app.route("/add/<name>")
def add_name(name):
    return jsonify({"status": "success", "name_added": name})

@app.route("/list")
def list_names():

    return jsonify({"status": "success", "type": "list"})

if __name__ == "__main__":
    app.run(debug=True)
