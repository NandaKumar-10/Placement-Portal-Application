from flask import Blueprint, request, jsonify
from model import *
from .auth import token_required,admin_required
from Cache import cache

admin_routes = Blueprint("admin_route", __name__)

@admin_routes.route('/admin/company-reg', methods=['PUT'])
@token_required
@admin_required
def approve_reject_company():
    data = request.get_json()
    company_id = data.get('company_id')
    new_status = data.get('approval_status')
    if company_id is None or new_status is None:
        return jsonify({'error': 'Missing company_id or approval_status'}), 400

    company = Company.query.get(company_id)

    if not company:
        return jsonify({'error': 'Company not found'}), 404

    company.approval_status = new_status
    db.session.commit()

    action = "approved" if new_status else "rejected"
    return jsonify({'message': f'Company {action} successfully', 'company_id': company.company_id}), 200

    
@admin_routes.route('/admin/placement-drive',methods=['PUT'])
@token_required
@admin_required
def approve_reject_drive():
    data = request.get_json()
    drive_id = data.get('drive_id')
    status_update = data.get('status')

    if not drive_id or not status_update:
        return jsonify({'error': 'Missing drive_id or status'}), 400
        
    allowed_statuses = ["Approved", "Rejected", "Pending"]
    if status_update not in allowed_statuses:
        return jsonify({'error': f'Invalid status. Allowed: {allowed_statuses}'}), 400

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({'error': 'Placement drive not found'}), 404

    drive.status = status_update
    db.session.commit()

    return jsonify({
        'message': f'Placement drive marked as {status_update}', 
        'drive_id': drive.drive_id
    }), 200
    

@admin_routes.route('/admin/students', methods=['GET'])
@token_required
@admin_required
def get_all_students():
    students = db.session.query(Students, Users).join(Users, Students.user_id == Users.user_id).all()
    result = []
    for student, user in students:
        result.append({
            "student_id": student.student_id,
            "user_id": user.user_id,
            "status": user.role,
            "name": user.name,
            "email": user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year": student.year,
            "resume_url": student.resume_url
        })
    return jsonify(result), 200

@admin_routes.route('/admin/student/<int:student_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_student(student_id):
    student = db.session.get(Students, student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    user = db.session.get(Users, student.user_id)
    db.session.delete(user) 
        
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student record deleted successfully'}), 200

@admin_routes.route('/admin/companies', methods=['GET'])
@token_required
@admin_required
def get_all_companies():
    companies = Company.query.all()
    result = []
    for comp in companies:
        result.append({
            "company_id": comp.company_id,
            "company_name": comp.company_name,
            "hr_contact": comp.hr_contact,
            "website": comp.website,
            "approval_status": "Approved" if comp.approval_status else "Pending"
        })
    return jsonify(result), 200

@admin_routes.route('/admin/company/<int:company_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_company(company_id):
    company = db.session.get(Company, company_id)
    company_user = Users.query.filter_by(user_id = company.user_id).first()
    if not company:
        return jsonify({'error': 'Company not found'}), 404
            
    db.session.delete(company)
    db.session.delete(company_user)
    db.session.commit()
    return jsonify({'message': 'Company deleted successfully'}), 200

@admin_routes.route('/admin/placement-drives', methods=['GET'])
@token_required
@admin_required
def get_all_drives():
    drives = db.session.query(PlacementDrive, Company).\
        join(Company, PlacementDrive.company_id == Company.company_id).all()
        
    result = []
    for drive, comp in drives:
        result.append({
            "drive_id": drive.drive_id,
            "company_name": comp.company_name,
            "job_title": drive.job_title,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "deadline": str(drive.application_deadline),
            "status": drive.status
        })
    return jsonify(result), 200

@admin_routes.route('/admin/placement-drive/<int:drive_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_drive(drive_id):
    drive = db.session.get(PlacementDrive, drive_id)
    if not drive:
        return jsonify({'error': 'Drive not found'}), 404
            
    db.session.delete(drive)
    db.session.commit()
    return jsonify({'message': 'Placement drive deleted successfully'}), 200
    
@admin_routes.route('/admin/search', methods=['GET'])
@token_required
@admin_required
def search_entities():
    query_param = request.args.get('q', '').strip()
        
    if not query_param:
        return jsonify({'error': 'Search query required'}), 400

    search_pattern = f"%{query_param}%"

    students_query = db.session.query(Students, Users)\
        .join(Users, Students.user_id == Users.user_id)\
        .filter(or_(Users.name.ilike(search_pattern), Users.email.ilike(search_pattern))).all()
        
    student_results = []
    for student, user in students_query:
        student_results.append({
            "type": "Student",
            "id": student.student_id,
            "name": user.name,
            "email": user.email,
            "status": user.role
        })

    companies_query = Company.query.filter(Company.company_name.ilike(search_pattern)).all()
        
    company_results = []
    for comp in companies_query:
        company_results.append({
            "type": "Company",
            "id": comp.company_id,
            "name": comp.company_name,
            "email": "N/A",
            "status": "Approved" if comp.approval_status else "Pending"
            })

    return jsonify({
        "students": student_results,
        "companies": company_results
    }), 200

@admin_routes.route('/admin/blacklist', methods=['POST'])
@token_required
@admin_required
def blacklist_user():
    data = request.get_json()
    user_id = data.get('user_id')
    action = data.get('action') 

    if not user_id or not action:
        return jsonify({'error': 'Missing user_id or action'}), 400

        
    user = Users.query.filter_by(user_id = user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if action == "block":
        if user.role != "Blacklisted":
            user.role = "Blacklisted" 
            db.session.commit()
            return jsonify({'message': f'User {user.email} has been blacklisted'}), 200
        else:
            return jsonify({'message': 'User is already blacklisted'}), 200

    elif action == "unblock":
        if user.student:
            user.role = "Student"
        elif user.company:
            user.role = "Company"
        else:
            user.role = "User"
            
        db.session.commit()
        return jsonify({'message': f'User {user.email} restored to {user.role}'}), 200

    else:
        return jsonify({'error': 'Invalid action. Use "block" or "unblock"'}), 400

    
@admin_routes.route('/admin/statistics', methods=['GET'])
@token_required
@admin_required
@cache.cached(timeout = 600, query_string = True)
def get_placement_statistics():
    total_students = db.session.query(func.count(Students.student_id)).scalar()
    total_companies = db.session.query(func.count(Company.company_id)).scalar()
    total_drives = db.session.query(func.count(PlacementDrive.drive_id)).scalar()

    placed_students_count = db.session.query(func.count(func.distinct(Application.student_id)))\
        .filter(Application.status.in_(['Accepted', 'Hired'])).scalar()

    placement_percentage = 0
    if total_students and total_students > 0:
        placement_percentage = round((placed_students_count / total_students) * 100, 2)

    branch_stats = db.session.query(Students.branch, func.count(Students.student_id))\
        .group_by(Students.branch).all()
        
    branch_data = {branch: count for branch, count in branch_stats}

    company_stats = db.session.query(Company.approval_status, func.count(Company.company_id))\
        .group_by(Company.approval_status).all()
        
    company_status_data = {
        "Approved": 0,
        "Pending": 0
    }
    for status, count in company_stats:
        key = "Approved" if status else "Pending"
        company_status_data[key] = count

    report = {
        "overview": {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_drives": total_drives,
        },
        "placement_performance": {
            "placed_students": placed_students_count,
            "unplaced_students": total_students - placed_students_count,
            "placement_rate_percentage": placement_percentage
        },
        "demographics": {
            "students_by_branch": branch_data
        },
        "administrative": {
            "company_approvals": company_status_data
            }
        }

    return jsonify(report), 200

@admin_routes.route('/admin/drive/<int:drive_id>', methods=['GET', 'PUT'])
@token_required
@admin_required
def manage_drive(drive_id):
    if request.method == 'PUT':
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Missing status field'}), 400

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        drive.status = new_status
        db.session.commit()

        cache.clear()
        
        return jsonify({'message': f'Drive status successfully updated to {new_status}'}), 200

    if request.method == 'GET':
        drive = db.session.query(PlacementDrive, Company)\
            .join(Company, PlacementDrive.company_id == Company.company_id)\
            .filter(PlacementDrive.drive_id == drive_id).first()

        if not drive:
            return jsonify({'error': 'Drive not found'}), 404

        drive_data, company_data = drive
        applications = db.session.query(Application, Students, Users)\
            .join(Students, Application.student_id == Students.student_id)\
            .join(Users, Students.user_id == Users.user_id)\
            .filter(Application.drive_id == drive_id).all()

        app_list = []
        for app, student, user in applications:
            app_list.append({
                "application_id": app.application_id,
                "student_name": user.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "status": app.status,
                "resume_url": student.resume_url
            })

        return jsonify({
            "drive_details": {
                "job_title": drive_data.job_title,
                "company_name": company_data.company_name,
                "deadline": str(drive_data.application_deadline),
                "eligibility_cgpa": drive_data.eligibility_cgpa,
                "status": drive_data.status
            },
            "applicants": app_list
        }), 200