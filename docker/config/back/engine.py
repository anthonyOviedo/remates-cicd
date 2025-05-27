from flask import Flask, jsonify, request, send_from_directory
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import json

app = Flask(__name__)

JSON_FILE_PATH = 'data/remates.json'
PDF_DIRECTORY = 'pdf/'  # Directory where PDFs are stored

REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Request latency',
    ['endpoint']
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    start_time = getattr(request, 'start_time', None)
    if start_time:
        request_latency = time.time() - start_time
        # Normalize path to avoid high cardinality if needed
        endpoint = request.path
        REQUEST_LATENCY.labels(endpoint).observe(request_latency)
        REQUEST_COUNT.labels(request.method, endpoint, str(response.status_code)).inc()
    return response

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def load_remates():
    """Load remates.json if it exists, otherwise return an empty list."""
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_remates(remates):
    """Save remates list to remates.json."""
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(remates, file, indent=2, ensure_ascii=False)

@app.route('/download/<filename>', methods=['GET'])
def download_pdf(filename): 
    """Serve a PDF file from the pdfs directory."""
    if os.path.exists(os.path.join(PDF_DIRECTORY, filename)):
        return send_from_directory(directory=PDF_DIRECTORY, path=filename, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route('/remates', methods=['GET'])
def get_remates():
    if os.path.exists(JSON_FILE_PATH):
        return send_from_directory(directory=os.getcwd(), path=JSON_FILE_PATH, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404
    

@app.route('/remates', methods=['POST'])
def add_remate():
    """Receive a new remate and add it to remates.json.
    Ensures the remate exists; updates if found, creates if not.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Load existing remates
    remates = load_remates()
    new_remate = data.get('data', data)
    updated_existing = False  # Initialize updated_existing here

    for i, remate in enumerate(remates):
        if remate.get('id') == new_remate.get('id'):
            remates[i] = new_remate  # Override the entire existing remate
            updated_existing = True
            break

    # If the remate was not found, add it directly (without the 'data' layer).
    if not updated_existing:
        # Use .get('data', data) to handle cases with or without the nested 'data' key
        remates.append(new_remate)

    # Save back to file
    save_remates(remates)

    return jsonify({"message": "Remate updated/created successfully", "remate": data}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # <--- Ensure host='0.0.0.0'