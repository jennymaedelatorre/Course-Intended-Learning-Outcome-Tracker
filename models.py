from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        """Hash the password before storing"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify the password against the hash"""
        return bcrypt.check_password_hash(self.password, password)

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    instructor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationship para maka-access sa User object
    instructor = db.relationship("User", backref="courses")

class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    topic_no = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    quiz_file = db.Column(db.String(255), nullable=True)

    # Foreign Key sa course
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    # Relationship para ma-access ang course
    course = db.relationship("Course", backref="topics")