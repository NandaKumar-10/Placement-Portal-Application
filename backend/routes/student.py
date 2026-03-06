from flask import request, jsonify, Blueprint, current_app
from model import *
from .auth import token_required,student_requried
import datetime
from Cache import cache

student_route = Blueprint("student_routes",__name__)

@student_route.route('/student/dashboard', methods=['GET'])
@token_required
@student_requried
def student_dashboard(current_user):
    student = Students.query.filter_by(user_id=current_user.user_id).first()
    
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404

    apps = db.session.query(Application, PlacementDrive, Company)\
        .join(PlacementDrive, Application.drive_id == PlacementDrive.drive_id)\
        .join(Company, PlacementDrive.company_id == Company.company_id)\
        .filter(Application.student_id == student.student_id)\
        .order_by(Application.application_date.desc())\
        .limit(5).all()

    recent_applications = []
    for app, drive, company in apps:
        recent_applications.append({
            "id": app.application_id,
            "company_name": company.company_name,
            "job_title": drive.job_title,
            "applied_date": app.application_date.strftime("%b %d, %Y") if app.application_date else "N/A",
            "status": app.status,
            "interview_date": app.interview_date,
            "interview_link": app.interview_link
        })

    return jsonify({ "profile": {
            "name": current_user.name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year": student.year
        },
        "applications": recent_applications}), 200

@student_route.route("/student/register", methods=['POST'])
@token_required
@student_requried
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

@student_route.route('/student/drive', methods=['GET'])
@token_required
@student_requried
@cache.cached(timeout=600, query_string=True)
def get_drives(current_user):
    student = Students.query.filter_by(user_id=current_user.user_id).first()
    
    applied_apps = Application.query.filter_by(student_id=student.student_id).all()
    applied_drive_ids = [app.drive_id for app in applied_apps]

    query = db.session.query(PlacementDrive, Company).join(Company).filter(PlacementDrive.status == 'Approved')

    min_cgpa = request.args.get('cgpa', type=float)
    target_branch = request.args.get('branch')

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
            "website": company.website,
            "has_applied": drive.drive_id in applied_drive_ids
        })
    return jsonify(result), 200

@student_route.route('/student/apply', methods=['POST'])
@token_required
@student_requried
def apply_for_drive(current_user):
    data = request.get_json()
    drive_id = data.get('drive_id')

    student = Students.query.filter_by(user_id=current_user.user_id).first()

    existing_app = Application.query.filter_by(student_id=student.student_id, drive_id=drive_id).first()
    if existing_app:
        return jsonify({'error': 'You have already applied for this drive'}), 400

    # student = db.session.get(Students, student_id)
    drive = db.session.get(PlacementDrive, drive_id)

    if student.cgpa < drive.eligibility_cgpa:
        return jsonify({'error': 'You do not meet the CGPA criteria'}), 400

    new_app = Application(
        student_id=student.student_id,
        drive_id=drive_id,
        application_date=datetime.date.today(),
        status="Applied"
    )
    db.session.add(new_app)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 200

@student_route.route('/student/my-applications/<int:student_id>', methods=['GET'])
@token_required
@student_requried
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

@student_route.route('/student/edit-profile', methods=['GET', 'PUT'])
@token_required
@student_requried
def manage_profile(current_user):
    student = Students.query.filter_by(user_id=current_user.user_id).first()
    
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404

    if request.method == 'GET':
        return jsonify({
            "name": current_user.name,
            "email": current_user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "resume_url": student.resume_url,
            "year": student.year
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        
        if 'branch' in data: student.branch = data['branch']
        if 'cgpa' in data: student.cgpa = data['cgpa']
        if 'year' in data: student.year = data['year']
        if 'resume_url' in data: student.resume_url = data['resume_url']
        if 'name' in data: current_user.name = data['name']
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200

@student_route.route('/student/history', methods=['GET'])
@token_required
@student_requried
def get_my_history(current_user):
    student = Students.query.filter_by(user_id=current_user.user_id).first()
    if not student:
        return jsonify({'error': 'Profile not found'}), 404
        
    apps = db.session.query(Application, PlacementDrive, Company)\
        .join(PlacementDrive, Application.drive_id == PlacementDrive.drive_id)\
        .join(Company, PlacementDrive.company_id == Company.company_id)\
        .filter(Application.student_id == student.student_id).all()

    history = []
    for app, drive, company in apps:
        if app.status in ["Accepted", "Hired", "Rejected", "Applied"]:
            history.append({
                "application_id": app.application_id,
                "company": company.company_name,
                "role": drive.job_title,
                "applied_on": str(app.application_date),
                "status": app.status
            })

    return jsonify({"history": history}), 200