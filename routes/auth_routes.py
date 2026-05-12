"""
Antigravity - Addict Aware
Authentication Routes: Register, Login, Logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token, set_access_cookies, unset_jwt_cookies,
    jwt_required, get_jwt_identity
)
from database.db import get_db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        db = get_db()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        # Check if user exists
        if db.users.find_one({'email': email}):
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        # Create user
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_pw,
            'role': 'user',
            'created_at': datetime.utcnow()
        })

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        db = get_db()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not all([email, password]):
            flash('Email and password are required.', 'danger')
            return render_template('login.html')

        user = db.users.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['password'], password):
            # Create JWT token
            access_token = create_access_token(
                identity=str(user['_id']),
                additional_claims={
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            )

            # Redirect based on role
            if user['role'] == 'admin':
                response = make_response(redirect(url_for('admin.dashboard')))
            else:
                response = make_response(redirect(url_for('user.dashboard')))

            set_access_cookies(response, access_token)
            flash(f'Welcome back, {user["name"]}!', 'success')
            return response
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    flash('Logged out successfully.', 'info')
    return response
