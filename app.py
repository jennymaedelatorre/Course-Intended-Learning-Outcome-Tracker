from flask import Flask, redirect, url_for
from auth import auth_bp
from users import users_bp
from models import db, bcrypt   
from courses import courses_bp

# app.register_blueprint(courses_bp)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretkey123'

    # Database config (PostgreSQL)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1504@localhost:5432/cilo_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    # Create tables if not exists
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
