from flask import Blueprint, render_template
from models import Course

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/courses")
def list_courses():
    courses = Course.query.all()

    for c in courses:
        print(f"{c.code} - {c.title} | Instructor: {c.instructor.full_name}")
        
    return render_template("courses.html", courses=courses)
