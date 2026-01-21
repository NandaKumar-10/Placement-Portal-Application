from flask import Flask
from model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"

with app.app_context():
    db.init_app(app)
    db.create_all()

