from flask import request, jsonify, Blueprint, current_app
from model import *
from .auth import token_required
import datetime

student_route = Blueprint("student_routes",__name__)

@student_route.route("/student/register")
@token_required
def student_register():
    data = request.get_json()
    new_user = Users(
        name=data['name'],
        email=data['email'],
        password=data['password'], 
        role="Student"
    )
    db.session.add(new_user)
    db.session.flush()
    new_student = Students(
        user_id=new_user.user_id,
        branch=data['branch'],
        cgpa=data['cgpa'],
        year=data['year'],
        resume_url=data.get('resume_url', '')
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student registered successfully', 'student_id': new_student.student_id}), 201

@student_route.route('/student/drives', methods=['GET'])
@token_required
def get_drives():
    min_cgpa = request.args.get('cgpa', type=float)
    target_branch = request.args.get('branch')
    query = db.session.query(PlacementDrive, Company).join(Company).filter(PlacementDrive.status == 'Approved')
    if min_cgpa:
        query = query.filter(PlacementDrive.eligibility_cgpa <= min_cgpa)
        
    if target_branch:
        query = query.filter(PlacementDrive.eligibility_branch.ilike(f"%{target_branch}%"))

    drives = query.all()
        
    result = []
    for drive, company in drives:
        result.append({
            "drive_id": drive.drive_id,
            "company_name": company.company_name,
            "job_title": drive.job_title,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "eligibility_branch": drive.eligibility_branch,
            "deadline": str(drive.application_deadline),
            "website": company.website
        })
    return jsonify(result), 200

@student_route.route('/student/apply', methods=['POST'])
def apply_for_drive():
    data = request.get_json()
    student_id = data.get('student_id')
    drive_id = data.get('drive_id')
        
    existing_app = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
    if existing_app:
        return jsonify({'error': 'You have already applied for this drive'}), 400

    student = db.session.get(Students, student_id)
    drive = db.session.get(PlacementDrive, drive_id)

    if student.cgpa < drive.eligibility_cgpa:
        return jsonify({'error': 'You do not meet the CGPA criteria'}), 400

    new_app = Application(
        student_id=student_id,
        drive_id=drive_id,
        application_date=datetime.date.today(),
        status="Applied"
    )
    db.session.add(new_app)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 200

@student_route.route('/student/my-applications/<int:student_id>', methods=['GET'])
def get_my_applications(student_id):
    apps = db.session.query(Application, PlacementDrive, Company)\
        .join(PlacementDrive, Application.drive_id == PlacementDrive.drive_id)\
        .join(Company, PlacementDrive.company_id == Company.company_id)\
        .filter(Application.student_id == student_id).all()

    current_apps = []
    history = []

    for app, drive, company in apps:
        app_data = {
            "application_id": app.application_id,
            "company": company.company_name,
            "role": drive.job_title,
            "applied_on": str(app.application_date),
            "status": app.status
        }
            
        if app.status in ["Accepted", "Hired", "Rejected"]:
            history.append(app_data)
        else:
            current_apps.append(app_data)

    return jsonify({"active_applications": current_apps, "history": history}), 200

@student_route.route('/student/profile/<int:student_id>', methods=['GET', 'PUT'])
def manage_profile(student_id):
    student = db.session.get(Students, student_id)
    user = db.session.get(Users, student.user_id)

    if request.method == 'GET':
        return jsonify({
            "name": user.name,
            "email": user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "resume_url": student.resume_url,
            "year": student.year
        })

    if request.method == 'PUT':
        data = request.get_json()
        if 'branch' in data: student.branch = data['branch']
        if 'cgpa' in data: student.cgpa = data['cgpa']
        if 'year' in data: student.year = data['year']
        if 'resume_url' in data: student.resume_url = data['resume_url']
        if 'name' in data: user.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200