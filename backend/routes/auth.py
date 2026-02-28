from flask import request, jsonify, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from model import *

auth = Blueprint("auth",__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
                
            except IndexError:
                return jsonify({'message': 'Token is invalid!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.get(data['user_id'])
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admins only!'}), 403
        return f(*args, **kwargs)
    return decorated

@auth.route('/login',methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error":"Enter Username or password"}), 400
    
    
    user = Users.query.filter_by(email = username).first()

    if user.check_password(password):
        jwt_payload = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(jwt_payload, current_app.config['SECRET_KEY'],algorithm='HS256')

        return jsonify({"token":token,"role":user.role}), 200
    else:
        return jsonify({"error" : "Invalid Username or Password"}), 200

@auth.route('/signup',methods = ['POST'])
def signup():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not username or not email or not password:
        return jsonify({"message": "Missing username, email, or password"}), 400

    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 409
    
    if Users.query.filter_by(name=username).first():
        return jsonify({"message": "Username is already taken"}), 409

    new_user = Users(name = username, email = email, password = password, role = role)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201
