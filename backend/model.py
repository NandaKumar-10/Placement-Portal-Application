from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship, join
import bcrypt

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    user_id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(100),unique = True, nullable = False)
    password: Mapped[str] = mapped_column(String(500), nullable = False)
    role: Mapped[str] = mapped_column(String(300), nullable = False)

    company = relationship("Company", back_populates="user", uselist = False)
    student = relationship("Students", back_populates="user", uselist = False)

    def __init__(self,email,name,password,role):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('UTF-8'),bcrypt.gensalt()).decode('UTF-8')
        self.role = role

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))


class Company(db.Model):
    __tablename__ = "Companies"
    company_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    company_name: Mapped[str] = mapped_column(String(200), nullable = False)
    hr_contact: Mapped[str] = mapped_column(String(200), nullable = False)
    website: Mapped[str] = mapped_column(String(300), nullable = False)
    approval_status: Mapped[Boolean]  = mapped_column(Boolean,default=False)

    user = relationship("Users", back_populates="company")
    placement_drives = relationship("PlacementDrive", back_populates="company")

    def __init__(self,user_id,company_name,hr_contact,website):
        self.user_id = user_id
        self.company_name = company_name
        self.hr_contact = hr_contact
        self.website = website

class Students(db.Model):
    __tablename__ = "Students"
    student_id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    branch: Mapped[str] = mapped_column(String(300), nullable = False)
    cgpa: Mapped[float] = mapped_column(Float)
    year: Mapped[int] = mapped_column(Integer)
    resume_url: Mapped[str] = mapped_column(String(300), nullable = False)

    def __init__(self,user_id,branch,cgpa,year,resume_url):
        self.user_id = user_id
        self.branch = branch
        self.cgpa = cgpa
        self.year = year
        self.resume_url = resume_url

    user = relationship("Users", back_populates="student")
    applications = relationship("Application", back_populates = "student")

class PlacementDrive(db.Model):
    __tablename__ = "Placement_drives"

    drive_id: Mapped[int] = mapped_column(primary_key = True)
    company_id: Mapped[int] = mapped_column(ForeignKey("Companies.company_id"))
    job_title: Mapped[str] = mapped_column(String(200), nullable = False)
    eligibility_branch: Mapped[str] = mapped_column(String(200), nullable = False)
    eligibility_cgpa: Mapped[float] = mapped_column(nullable = False)
    eligibility_year: Mapped[int] = mapped_column(Integer)
    application_deadline: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(100),nullable = False)

    company = relationship("Company", back_populates="placement_drives")
    applications = relationship("Application",back_populates="drive")

    def __init__(self,company_id,job_title,eligibility_branch,eligibility_cgpa,eligibility_year,application_deadline,status):
        self.company_id = company_id
        self.job_title =  job_title
        self.eligibility_branch = eligibility_branch
        self.eligibility_cgpa = eligibility_cgpa
        self.eligibility_year = eligibility_year
        self.application_deadline = application_deadline
        self.status = status

class Application(db.Model):
    __tablename__ = "Application"
    application_id: Mapped[int] = mapped_column(primary_key = True)
    student_id: Mapped[int] = mapped_column(ForeignKey("Students.student_id"))
    drive_id: Mapped[int] = mapped_column(ForeignKey("Placement_drives.drive_id"))
    application_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(200))

    student = relationship("Students", back_populates = "applications")
    drive = relationship("PlacementDrive", back_populates = "applications")

    def __init__(self,student_id,drive_id,application_date,status):
        self.student_id = student_id
        self.drive_id = drive_id
        self.application_date = application_date
        self.status = status

if __name__ == "__main__":
    db.create_all()
