from flask import request, jsonify, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model import *

auth = Blueprint("auth",__name__)

@auth.route('/login',methods = ['POST'])
def login():
    data = request.json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error":"Enter Username or password"}), 400
    
    
    user = Users.query.filter_by(email = username).first()

    if user.check_password(password):
        jwt_payload = {
            "user_id": user.user_id,
            "email": user.email,
            "exp": str(datetime.datetime.utcnow() + datetime.timedelta(hour=1))
        }

        token = jwt.encode(jwt_payload, current_app.config['SECRET_KEY'],algorithm='HS256')

        return jsonify({"token":token}), 200


@auth.route('/signup',methods = ['POST'])
def signup():
    pass

@auth.route('/logout',methods = ['POST'])
def logout():
    pass