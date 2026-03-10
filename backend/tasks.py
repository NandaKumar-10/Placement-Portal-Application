from celery import Celery
from celery.schedules import crontab
import csv
import io
import datetime
import smtplib
from app import app
from model import db, PlacementDrive, Users, Students, Application, Company
import calendar
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

celery_app = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    broker_connection_retry_on_startup=True,
    broker_transport_options={'socket_keepalive': True}
)

def send_email(to_email, subject, body, input_type):
    SENDER_EMAIL = "bnandakumar2005@gmail.com" 
    SENDER_PASSWORD = "lipowjhzwvqydaef"

    msg = MIMEMultipart()
    msg['From'] = f"Placement Cell <{SENDER_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, input_type))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False
    

@celery_app.task
def send_daily_reminders():
    with app.app_context():
        target_date = datetime.date.today() + datetime.timedelta(days=1)

        upcoming_drives = db.session.query(PlacementDrive, Company)\
            .join(Company, PlacementDrive.company_id == Company.company_id)\
            .filter(
                PlacementDrive.application_deadline <= target_date, 
                PlacementDrive.application_deadline >= datetime.date.today(),
                PlacementDrive.status == 'Approved'
            ).all()

        if not upcoming_drives:
            return "No deadlines"

        for drive, company in upcoming_drives:
            
            applied_apps = db.session.query(Application.student_id).filter_by(drive_id=drive.drive_id).all()
            applied_ids = [app.student_id for app in applied_apps]
            
            student_query = db.session.query(Students, Users).join(Users, Students.user_id == Users.user_id)
            
            if applied_ids:
                student_query = student_query.filter(~Students.student_id.in_(applied_ids))
                
            student_query = student_query.filter(Students.cgpa >= drive.eligibility_cgpa)
            
            if hasattr(drive, 'eligibility_branch') and drive.eligibility_branch:
                student_query = student_query.filter(Students.branch.ilike(f"%{drive.eligibility_branch}%"))
                
            eligible_unapplied_students = student_query.all()

            for student, user in eligible_unapplied_students:
                
                subject = f"Action Required: {company.company_name} Deadline Approaching!"
                body = (
                    f"Hi {user.name},\n\n"
                    f"You are eligible for the '{drive.job_title}' role at {company.company_name}, "
                    f"but our records show you haven't applied yet.\n\n"
                    f"The deadline is rapidly approaching on {drive.application_deadline.strftime('%b %d, %Y')}.\n\n"
                    f"Please log in to the placement portal to submit your resume if you are interested.\n\n"
                    f"Best regards,\n"
                    f"The Placement Cell Team"
                )

                send_email(to_email=user.email, subject=subject, body=body, input_type='plain')

        return "Targeted email reminders complete."

@celery_app.task
def export_student_history_csv(student_id, user_email, user_name):
    with app.app_context():
        apps = db.session.query(Application, PlacementDrive, Company)\
            .join(PlacementDrive, Application.drive_id == PlacementDrive.drive_id)\
            .join(Company, PlacementDrive.company_id == Company.company_id)\
            .filter(Application.student_id == student_id)\
            .order_by(Application.application_date.desc()).all()

        si = io.StringIO()
        cw = csv.writer(si)
        
        cw.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Applied Date'])

        for app_obj, drive, company in apps:
            cw.writerow([
                student_id,
                company.company_name,
                drive.job_title,
                app_obj.status,
                app_obj.application_date.strftime('%Y-%m-%d')
            ])

        SENDER_EMAIL = "bnandakumar2005@gmail.com" 
        SENDER_PASSWORD = "lipowjhzwvqydaef"

        msg = MIMEMultipart()
        msg['From'] = f"Placement Cell <{SENDER_EMAIL}>"
        msg['To'] = user_email
        msg['Subject'] = "Your Placement Application History Export"

        body = f"Hi {user_name},\n\nYour requested placement application history export is attached as a CSV file.\n\nBest regards,\nThe Placement Cell"
        msg.attach(MIMEText(body, 'plain'))

        csv_attachment = MIMEApplication(si.getvalue().encode('utf-8'))
        csv_attachment.add_header('Content-Disposition', 'attachment', filename='My_Application_History.csv')
        msg.attach(csv_attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            return "Export sent successfully"
        except Exception as e:
            return "Export Failed"
        
@celery_app.task
def send_monthly_report():
    with app.app_context():    
        today = datetime.date.today()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - datetime.timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)
        
        month_name = calendar.month_name[first_day_prev_month.month]
        year = first_day_prev_month.year

        drives_conducted = db.session.query(PlacementDrive).filter(
            PlacementDrive.application_deadline >= first_day_prev_month,
            PlacementDrive.application_deadline <= last_day_prev_month,
            PlacementDrive.status == 'Approved'
        ).count()

        students_applied = db.session.query(Application).filter(
            Application.application_date >= first_day_prev_month,
            Application.application_date <= last_day_prev_month
        ).count()

        students_selected = db.session.query(Application).filter(
            Application.application_date >= first_day_prev_month,
            Application.application_date <= last_day_prev_month,
            Application.status.in_(['Hired', 'Accepted'])
        ).count()

        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #2563eb; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                        Monthly Placement Report
                    </h2>
                    <p>Here is the activity summary for <strong>{month_name} {year}</strong>:</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <tr style="background-color: #f8fafc; border-bottom: 1px solid #eee;">
                            <td style="padding: 12px; font-weight: bold;">Drives Conducted</td>
                            <td style="padding: 12px; text-align: right; font-size: 18px;">{drives_conducted}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 12px; font-weight: bold;">Students Applied</td>
                            <td style="padding: 12px; text-align: right; font-size: 18px;">{students_applied}</td>
                        </tr>
                        <tr style="background-color: #f8fafc; border-bottom: 1px solid #eee;">
                            <td style="padding: 12px; font-weight: bold;">Students Selected</td>
                            <td style="padding: 12px; text-align: right; font-size: 18px; color: #16a34a;">{students_selected}</td>
                        </tr>
                    </table>
                    
                    <p style="margin-top: 30px; font-size: 12px; color: #888;">
                        This is an automated report generated by the Placement Portal Celery Task.
                    </p>
                </div>
            </body>
        </html>
        """

        ADMIN_EMAIL = "admin@placement.com"

        send_email(ADMIN_EMAIL,subject=f"Monthly Activity Report - {month_name} {year}",body=html_content,input_type='html')

        return "Monthly report sent"

celery_app.conf.beat_schedule = {
    'send-reminders-every-morning': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),  
    },
    'send-monthly-admin-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(day_of_month='1', hour=8, minute=0)
    },
}