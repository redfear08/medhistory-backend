from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from models import db, Document
from utils.generate_qr import generate_qr_code
import os
from datetime import datetime

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# Endpoint: Upload Document
@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    upload_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{upload_date}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save the file
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(filepath)

    # Register in database
    document = Document(upload_date=upload_date, image_url=filepath)
    db.session.add(document)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "filename": filename})


# Endpoint: Get Medical History
@app.route('/get-medical-history', methods=['GET'])
def get_medical_history():
    documents = Document.query.order_by(Document.upload_date.desc()).all()
    history = [{"id": doc.id, "upload_date": doc.upload_date, "image_url": doc.image_url} for doc in documents]
    return jsonify({"medical_history": history})


# Endpoint: Share Medical History
@app.route('/share-history', methods=['GET'])
def share_history():
    documents = Document.query.order_by(Document.upload_date.desc()).all()
    image_urls = [doc.image_url for doc in documents]

    qr_code_path = generate_qr_code(image_urls)
    return send_file(qr_code_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
