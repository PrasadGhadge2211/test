from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify

app = Flask(__name__)

@app.route('/')
def dashboard():
    return jsonify({"message":"working"})
if __name__ == '__main__':
    app.run(debug=True)
