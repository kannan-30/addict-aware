"""
Antigravity - Addict Aware
Main Application Entry Point

Flask application factory with all blueprint registrations,
JWT setup, and database initialization.
"""
import os
import sys
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_app():
    """Application factory"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'antigravity-secret-2024')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-addict-aware-super-secret-key-2024-secure')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production

    # Initialize extensions
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return redirect(url_for('auth.login'))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('auth.login'))

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return redirect(url_for('auth.login'))

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Landing page route
    @app.route('/')
    def index():
        return redirect(url_for('landing'))

    @app.route('/home')
    def landing():
        from flask import render_template
        return render_template('index.html')

    # Initialize database on first request
    with app.app_context():
        try:
            from database.db import get_db, init_db
            db = get_db()
            init_db(db)
        except Exception as e:
            print(f"[!] Database init warning: {e}")

        # Train ML model if not exists
        try:
            from models.ml_model import MODEL_PATH
            if not os.path.exists(MODEL_PATH):
                from models.generate_dataset import generate_dataset
                from models.ml_model import train_model
                generate_dataset()
                train_model()
        except Exception as e:
            print(f"[!] ML model init warning: {e}")

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
