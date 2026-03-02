from flask import request, jsonify, Blueprint, current_app
import datetime
from model import *
from .auth import token_required,company_required

company_route = Blueprint("company_route",__name__)

@company_route.route('/company/dashboard', methods=['GET'])
@token_required
@company_required
def get_dashboard(current_user):
    company = Company.query.filter_by(user_id=current_user.user_id).first()
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404

    drives = PlacementDrive.query.filter_by(company_id=company.company_id).all()
    drives_data = []

    for drive in drives:
        applicant_count = Application.query.filter_by(drive_id=drive.drive_id).count()
        drives_data.append({
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "deadline": str(drive.application_deadline),
            "status": drive.status,
            "applicants": applicant_count
        })

    return jsonify({
        "company_details": {
            "name": company.company_name,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "approval_status": "Approved" if company.approval_status else "Pending"
        },"drives": drives_data}), 200

@company_route.route('/company/drive',methods = ['POST'])
@token_required
@company_required
def create_drive(current_user):
    company = Company.query.filter_by(user_id=current_user.user_id).first()
    if not company.approval_status:
        return jsonify({'error': 'You cannot create placement drives until the Admin approves your profile.'}), 403

    data = request.get_json()
    
    try:
        deadline = datetime.datetime.strptime(data.get('deadline'), '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    new_drive = PlacementDrive(company_id=company.company_id,job_title=data.get('job_title'),
                               eligibility_branch=data.get('eligibility_branch'),
                               eligibility_cgpa=data.get('eligibility_cgpa'),
                               eligibility_year=data.get('eligibility_year'),
                               application_deadline=deadline,status='Pending')
    
    db.session.add(new_drive)
    db.session.commit()

    return jsonify({'message': 'Placement drive created successfully!', 'drive_id': new_drive.drive_id}), 201

@company_route.route('/company/drive/<int:drive_id>/applications', methods=['GET'])
@token_required
@company_required
def view_applications(current_user, drive_id):
    company = Company.query.filter_by(user_id=current_user.user_id).first()
    drive = PlacementDrive.query.filter_by(drive_id=drive_id, company_id=company.company_id).first()

    if not drive:
        return jsonify({'error': 'Drive not found or unauthorized'}), 404

    applications = db.session.query(Application, Students, Users).\
        join(Students, Application.student_id == Students.student_id).\
        join(Users, Students.user_id == Users.user_id).\
        filter(Application.drive_id == drive_id).all()

    results = []
    for app, student, user in applications:
        results.append({
            "application_id": app.application_id,
            "student_name": user.name,
            "student_email": user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "resume_url": student.resume_url,
            "status": app.status
        })

    return jsonify(results), 200

@company_route.route('/company/application/<int:app_id>', methods=['PUT'])
@token_required
@company_required
def update_application(current_user, app_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'Missing status field'}), 400

    application = Application.query.get(app_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    company = Company.query.filter_by(user_id=current_user.user_id).first()
    drive = PlacementDrive.query.get(application.drive_id)
    
    if drive.company_id != company.company_id:
        return jsonify({'error': 'Unauthorized to edit this application'}), 403

    application.status = new_status
    db.session.commit()

    return jsonify({'message': f'Student application marked as {new_status}'}), 200