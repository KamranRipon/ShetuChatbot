# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_user, logout_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
# from app import db
# from app.models import User
# from app import app 
# from auth import auth_blueprint

# auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and user.check_password(password):
#             login_user(user)
#             flash('Logged in successfully!')
#             return redirect(url_for('chatbot'))
        
#         flash('Invalid credentials, try again.')
    
#     return render_template('login.html')

# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists!')
#             return redirect(url_for('auth.signup'))
        
#         new_user = User(username=username)
#         new_user.set_password(password)

#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created! Please log in.')
#         return redirect(url_for('auth.login'))
    
#     return render_template('signup.html')

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.')
#     return redirect(url_for('auth.login'))
