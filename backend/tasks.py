from celery import Celery
from celery.schedules import crontab

import datetime
import smtplib
from app import app
from model import db, PlacementDrive, Users, Students, Application, Company
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

celery = Celery(
    app.name,
    broker='redis://172.26.87.199:6379/0',
    backend='redis://172.26.87.199:6379/0'
)

celery.conf.update(
    broker_url='redis://172.26.87.199:6379/0',
    result_backend='redis://172.26.87.199:6379/0',
    broker_connection_retry_on_startup=True,
    broker_transport_options={'socket_keepalive': True}
)

def send_email(to_email, subject, body):
    SENDER_EMAIL = "bnandakumar2005@gmail.com" 
    SENDER_PASSWORD = "lipowjhzwvqydaef"

    msg = MIMEMultipart()
    msg['From'] = f"Placement Cell <{SENDER_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
    

@celery.task
def send_daily_reminders():
    with app.app_context():
        target_date = datetime.date.today() + datetime.timedelta(days=1)

        upcoming_drives = db.session.query(PlacementDrive, Company)\
            .join(Company, PlacementDrive.company_id == Company.company_id)\
            .filter(
                PlacementDrive.application_deadline <= target_date, 
                PlacementDrive.application_deadline >= datetime.date.today(), # Don't remind for past drives
                PlacementDrive.status == 'Approved'
            ).all()

        if not upcoming_drives:
            print("No upcoming deadlines for today.")
            return "No deadlines"

        for drive, company in upcoming_drives:
            print(f"--- Processing Drive: {drive.job_title} at {company.company_name} ---")
            
            # 1. Bulletproof approach: Get a simple list of student_ids who already applied
            applied_apps = db.session.query(Application.student_id).filter_by(drive_id=drive.drive_id).all()
            applied_ids = [app.student_id for app in applied_apps] # Extracts just the numbers into a list
            
            # 2. Start the student query
            student_query = db.session.query(Students, Users).join(Users, Students.user_id == Users.user_id)
            
            # 3. Only filter out applied students if someone has ACTUALLY applied
            if applied_ids:
                student_query = student_query.filter(~Students.student_id.in_(applied_ids))
                
            # 4. Apply CGPA criteria
            student_query = student_query.filter(Students.cgpa >= drive.eligibility_cgpa)
            
            # 5. Apply Branch criteria (handling case-insensitivity)
            if hasattr(drive, 'eligibility_branch') and drive.eligibility_branch:
                student_query = student_query.filter(Students.branch.ilike(f"%{drive.eligibility_branch}%"))
                
            # Execute the query
            eligible_unapplied_students = student_query.all()
            print(f"Found {len(eligible_unapplied_students)} eligible students who haven't applied yet.")

            # 6. Send the emails!
            for student, user in eligible_unapplied_students:
                print(f"📧 Sending reminder to {user.name} ({user.email})...")
                
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

                send_email(to_email=user.email, subject=subject, body=body)

        return "Targeted email reminders complete."

celery.conf.beat_schedule = {
    'send-reminders-every-morning': {
        'task': 'tasks.send_daily_reminders',
        # Schedule it to run every day at 9:00 AM
        # 'schedule': crontab(hour=9, minute=0), 
        
        # NOTE FOR TESTING: Uncomment the line below to run it every 1 minute to test if it works!
        'schedule': crontab(minute='*'), 
    },
}