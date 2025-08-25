from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app, send_file
import os
from models import Course, Topic, db
from werkzeug.utils import secure_filename


users_bp = Blueprint('users', __name__)

@users_bp.route('/dashboard')
def dashboard():
    role = session.get('role')

    # Query from the Course model
    all_courses = Course.query.all()

    topics = Topic.query.all()

    if role == 'student':
        return render_template('student/dashboard.html', courses=all_courses, topics=topics)
    elif role == 'faculty':
        return render_template('faculty/dashboard.html', courses=all_courses, topics=topics)
    return redirect(url_for('auth.login'))


@users_bp.route('/courses')
def courses():
    import os
    from flask import current_app

    role = session.get('role')

     # Query from the Course model
    all_courses = Course.query.all()

    downloads_path = os.path.join(current_app.static_folder, 'downloads')
    files = []

    if os.path.exists(downloads_path):
        for filename in os.listdir(downloads_path):
            full_path = os.path.join(downloads_path, filename)
            if os.path.isfile(full_path):
                size_kb = os.path.getsize(full_path) / 1024
                readable_size = f"{size_kb:.1f} KB"
                files.append((filename, readable_size))

    if role == 'student':
        return render_template('student/courses.html', courses=all_courses, files=files)
    elif role == 'faculty':
        return render_template('faculty/courses.html', courses=all_courses, files=files)
    return redirect(url_for('auth.login'))


@users_bp.route('/cilos')
def cilos():
    role = session.get('role')

   
    courses = [
        {
            "name": "Introduction to Programming",
            "progress": 70,
            "cilos": [
                {"title": "CILO 1", "progress": 70},
                {"title": "CILO 2", "progress": 80},
                {"title": "CILO 3", "progress": 85}
            ]
        },
    ]

    if role == 'student':
        return render_template('student/cilos.html', courses=courses)
    
    elif role == 'faculty':
        return render_template('faculty/cilos.html', courses=courses)
    
    return redirect(url_for('auth.login'))
    


@users_bp.route('/profile')
def profile():
    role = session.get('role')
    if role == 'student':
        return render_template('student/profile.html')
    elif role == 'faculty':
        return render_template('faculty/profile.html')
    return redirect(url_for('auth.login'))




@users_bp.route('/topic/<int:course_id>', methods=['GET', 'POST'])
def manage_topics(course_id):
    role = session.get('role')

    if role != 'faculty':
        return redirect(url_for('auth.login'))

    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        topic_no = request.form['topic_no']
        title = request.form['title']
        subtitle = request.form['subtitle']
        
        quiz_file = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                quiz_file = filename

        #  create new topic object
        new_topic = Topic(
            topic_no=topic_no,
            title=title,
            subtitle=subtitle,
            quiz_file=quiz_file,   
            course_id=course.id
        )

        db.session.add(new_topic)   
        db.session.commit()

        flash("Topic uploaded successfully!", "success")
        return redirect(url_for('users.manage_topics', course_id=course.id))

    topics = Topic.query.filter_by(course_id=course.id).all()
    return render_template('faculty/topic.html', course=course, topics=topics)




@users_bp.route('/course/<int:course_id>/topics')
def view_topics(course_id):
    course = Course.query.get_or_404(course_id)
    topics = Topic.query.filter_by(course_id=course.id).all()
    role = session.get('role')

    if role == 'student':
        return render_template('student/topic.html', course=course, topics=topics)
    elif role == 'faculty':
        return render_template('faculty/topic.html', course=course, topics=topics)

    return redirect(url_for('auth.login'))




@users_bp.route('/topic/<int:topic_id>/view')
def view_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    if not topic.quiz_file:
        flash("No file uploaded for this topic.", "warning")
        return redirect(url_for('users.view_topics', course_id=topic.course_id))

    file_url = url_for('static', filename=f'uploads/{topic.quiz_file}', _external=True)
    
  
    if topic.quiz_file.lower().endswith(".pdf"):
        return redirect(file_url)

    
    if topic.quiz_file.lower().endswith((".docx", ".pptx")):
        gview_url = f"https://docs.google.com/viewer?url={file_url}&embedded=true"
        return redirect(gview_url)

 
    return redirect(file_url)




@users_bp.route('/download/<int:topic_id>')
def download_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    if not topic.quiz_file:
        flash("No file uploaded for this topic.", "warning")
        return redirect(url_for('users.view_topic', course_id=topic.course_id))

    # Path in uploads
    upload_path = os.path.join(current_app.static_folder, 'uploads', topic.quiz_file)

    if not os.path.exists(upload_path):
        flash("File not found in uploads.", "danger")
        return redirect(url_for('users.view_topic', course_id=topic.course_id))

    # Copy to downloads
    downloads_path = os.path.join(current_app.static_folder, 'downloads', topic.quiz_file)
    import shutil
    shutil.copy(upload_path, downloads_path)

   
    return send_file(upload_path, as_attachment=True)



@users_bp.route('/quiz')
def quiz():
    role = session.get('role')
    if role == 'student':
        return render_template('student/quiz.html')
    elif role == 'faculty':
        return render_template('faculty/quiz.html')
    return redirect(url_for('auth.login'))
