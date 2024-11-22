from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
