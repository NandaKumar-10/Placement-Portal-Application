from flask import Flask
from flask_cors import CORS
from model import db, Users
from Cache import cache
from routes.admin import admin_routes
from routes.auth import auth
from routes.student import student_route
from routes.company import company_route
app = Flask(__name__)

CORS(app,supports_credentials=True)

app.config['SECRET_KEY'] = 'gLqw7i_L_NLS08kSHtTeJMGz3HVRN6l8T2kPeLFWNe8'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

db.init_app(app)

cache.init_app(app)

with app.app_context():
    db.create_all()
    admin = Users.query.filter_by(role = "admin").first()

    if not admin:
        new_admin = Users(email="admin@placement.com", name="Admin", 
                          password="password", role="admin")

        db.session.add(new_admin)
        db.session.commit()

app.register_blueprint(admin_routes)
app.register_blueprint(auth)
app.register_blueprint(student_route)
app.register_blueprint(company_route)

if __name__ == "__main__":
    app.run(debug=True)