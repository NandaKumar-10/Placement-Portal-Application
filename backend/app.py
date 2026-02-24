from flask import Flask
from flask_cors import CORS
import os
from model import db
from routes.admin import admin_routes

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gLqw7i_L_NLS08kSHtTeJMGz3HVRN6l8T2kPeLFWNe8'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"

# 3. Initialize the database with the app <-- THIS FIXES YOUR ERROR
db.init_app(app)
app.register_blueprint(admin_routes)
if __name__ == "__main__":
    app.run(debug=True)

# app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-this")