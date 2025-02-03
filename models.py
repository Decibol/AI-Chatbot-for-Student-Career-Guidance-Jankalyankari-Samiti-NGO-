from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    academic_level = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.String(200), nullable=False)

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.String(50))
    link = db.Column(db.String(200))
    academic_level = db.Column(db.String(50))

class ExamResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    preparation_tips = db.Column(db.Text)
    recommended_books = db.Column(db.String(200))
    website = db.Column(db.String(200))

class CareerPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.String(200))
    average_salary = db.Column(db.String(50))