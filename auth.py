from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User   

auth_bp = Blueprint('auth', __name__)


# ---------------- Register ----------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Username already exists.")

        # create new user
        new_user = User(full_name=full_name,username=username, role=role)
        new_user.set_password(password)   
        db.session.add(new_user)
        db.session.commit()

        # auto-login after register 
        session['user'] = new_user.username
        session['role'] = new_user.role
        return redirect(url_for('users.dashboard'))

    return render_template('register.html')


# ---------------- Login ----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password): 
            if user.role != role:  
                return render_template('login.html', error="Invalid role selected.")

            session['user_id'] = user.id
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('users.dashboard'))

        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


# ---------------- Logout ----------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
