from flask import Flask, request, jsonify, session, send_file, redirect, url_for
import requests
import os

app = Flask(__name__, static_folder="public", static_url_path="/public")
app.secret_key = "your_secret_key"  # Required for session management

BACK_SERVER = 'http://report-engine:5001'

# Dummy user database (replace with a real database)
USERS = {"minor@oviedo": "88137504", "estiven@oviedo": "87530890", "antony@oviedo": "87898967"}

# Middleware to check login
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_page'))  # Redirect to login page
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
@login_required
def index():
    return send_file("public/index.html")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return send_file("public/login.html")
    
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        session['user'] = username
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

@app.route('/data', methods=['GET'])
@login_required
def get_data():
    try:
        response = requests.get(f"{BACK_SERVER}/remates")
        response.raise_for_status()
        return jsonify(response.json())  # just return it
    except requests.RequestException as error:
        return jsonify({"error": "Failed to fetch data from backend", "details": str(error)}), 500

@app.route('/getPDF', methods=['GET'])
@login_required
def get_pdf():
    matricula = request.args.get("matricula")
    if not matricula:
        return jsonify({"error": "Matricula parameter is missing"}), 400

    try:
        response = requests.get(f"{BACK_SERVER}/download/{matricula}pdf")
        response.raise_for_status()
        return send_file(io.BytesIO(response.content), mimetype="application/pdf", as_attachment=True, download_name=f"{matricula}.pdf")
    except requests.RequestException as error:
        return jsonify({"error": "Failed to fetch PDF", "details": str(error)}), 500

@app.route('/update-property', methods=['POST'])
@login_required
def update_property():
    payload = request.json
    if not payload:
        return jsonify({"error": "No data provided"}), 400

    try:
        response = requests.post(f"{BACK_SERVER}/remates", json=payload)
        response.raise_for_status()
        return jsonify({"response": "Data SAVED on server", "details": response.json()})
    except requests.RequestException as error:
        return jsonify({"error": "Failed to send data", "details": str(error)}), 500

@app.route('/detalle', methods=['GET'])
@login_required
def detalle():
    item_id = request.args.get('item')
    if not item_id:
        return "Item ID is required", 400
    return send_file("public/detalle.html")

@app.route('/ia', methods=['POST'])
@login_required
def ia():
    payload = request.json
    if not payload or 'prompt' not in payload:
        return jsonify({"error": "Invalid request"}), 400

    request_payload = {
        "model": "deepseek-r1:14b",
        "prompt": payload["prompt"],
        "stream": False,
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=request_payload)
        response.raise_for_status()
        cleaned_response = response.json().get("response", "").replace("<think>", "").replace("</think>", "").strip()
        return jsonify({"response": cleaned_response})
    except requests.RequestException as error:
        return jsonify({"error": "AI processing failed", "details": str(error)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
