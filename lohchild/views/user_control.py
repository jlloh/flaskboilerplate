from flask import Blueprint,render_template,g,request,redirect,url_for,session,flash,current_app,session
from flask_login import login_user,logout_user

user_control = Blueprint('user_control', __name__)

@user_control.route('/login')
def login():
    return render_template('user_control/login.html', google_app_id=current_app.config['GOOGLE_APP_ID'])

@user_control.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
