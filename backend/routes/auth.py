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

def company_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        # Make sure the string matches exactly how you store it in the DB (e.g., 'Company' or 'company')
        if current_user.role != 'Company': 
            return jsonify({'message': 'Companies only!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def student_requried(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'Student':
            return jsonify({"message":'Students only!'}), 403
        return f(current_user, *args, **kwargs)
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

@auth.route('/register',methods = ['POST'])
def signup():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password:
        return jsonify({"message": "Missing username, email, or password"}), 400

    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 409
    
    if Users.query.filter_by(name=name).first():
        return jsonify({"message": "Username is already taken"}), 409
    
    if role == "Student":
        new_user = Users(name = name, email = email, password = password, role = role)
        db.session.add(new_user)
        db.session.flush()
        student_branch = data.get('branch')
        student_cgpa = data.get('cgpa')
        student_year = data.get('year')
        student_resume = data.get('resume')
        new_student = Students(user_id=new_user.user_id,branch=student_branch,cgpa=student_cgpa,
                               year=student_year,resume_url=student_resume)
        db.session.add(new_student)
    else:
        new_user = Users(name = name, email = email, password = password, role = role)
        db.session.add(new_user)
        db.session.flush()
        new_company_hr = data.get('hrContact')
        new_company_website = data.get('website')
        new_company = Company(user_id=new_user.user_id,company_name=name,hr_contact=new_company_hr,
                              website=new_company_website)
        db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201
