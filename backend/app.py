from flask import Flask
from flask_cors import CORS
from model import db
from routes.admin import admin_routes
from routes.auth import auth
from routes.student import student_route
from routes.company import company_route

app = Flask(__name__)

CORS(app,supports_credentials=True)

app.config['SECRET_KEY'] = 'gLqw7i_L_NLS08kSHtTeJMGz3HVRN6l8T2kPeLFWNe8'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"

db.init_app(app)
app.register_blueprint(admin_routes)
app.register_blueprint(auth)
app.register_blueprint(student_route)
app.register_blueprint(company_route)

if __name__ == "__main__":
    app.run(debug=True)
