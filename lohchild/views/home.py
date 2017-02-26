from flask import Blueprint,render_template,g,request,redirect,url_for,session,current_app
from flask_login import current_user,login_required

home=Blueprint('home',__name__)

@home.route('/')
@home.route('/home')
@login_required
def homepage():
	return render_template('/home/home.html', username = current_user.username, google_app_id = current_app.config['GOOGLE_APP_ID'])

