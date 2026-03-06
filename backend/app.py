from flask import Flask
from flask_cors import CORS
from model import db
from Cache import cache
from routes.admin import admin_routes
from routes.auth import auth
from routes.student import student_route
from routes.company import company_route
from flask_migrate import Migrate
app = Flask(__name__)

CORS(app,supports_credentials=True)

app.config['SECRET_KEY'] = 'gLqw7i_L_NLS08kSHtTeJMGz3HVRN6l8T2kPeLFWNe8'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['broker_url'] = 'redis://172.26.87.199:6379/0'
app.config['result_backend'] = 'redis://172.26.87.199:6379/0'

db.init_app(app)
migrate = Migrate(app, db)

cache.init_app(app)

# with app.app_context():
#     db.create_all()

app.register_blueprint(admin_routes)
app.register_blueprint(auth)
app.register_blueprint(student_route)
app.register_blueprint(company_route)

if __name__ == "__main__":
    app.run(debug=True)