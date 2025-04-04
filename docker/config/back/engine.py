from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

JSON_FILE_PATH = 'data/remates.json'
PDF_DIRECTORY = 'pdf/'  # Directory where PDFs are stored


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

    # Find the remate to update
    updated_existing = False
    for i, remate in enumerate(remates):
        if remate.get('id') == data.get('id'):
            remates[i] = data  # Override
            updated_existing = True
            break

    # If the remate was not found, add it.
    if not updated_existing:
        remates.append(data)

    # Save back to file
    save_remates(remates)

    return jsonify({"message": "Remate updated/created successfully", "remate": data}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # <--- Ensure host='0.0.0.0'
