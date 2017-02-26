import sqlite3
import os
from flask import Flask,request,session,g,redirect,url_for,render_template
from flask_login import LoginManager, login_required, current_user
from flask_bower import Bower

from .controllers.model import User

#import blueprints
from .views.home import home
from .views.user_control import user_control
from .controllers.api import api

app=Flask(__name__,instance_relative_config=True)
app.config.from_object('config') #looks for capitalized variables declared
app.config.from_pyfile('config.py')

#database
app.config['DATABASE']=os.path.join(app.instance_path,'database.db')

Bower(app)

#register blueprints
app.register_blueprint(api)
app.register_blueprint(home)
app.register_blueprint(user_control)

#Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "user_control.login"

#Function to connect to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#Special functions to request connection
@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exeption):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
@app.after_request
def add_header(response):
	response.headers['Cache-Control']='public,max-age=0'
	return response

@login_manager.user_loader
def load_user(userid):
    username=str(userid)
    return User(username, app.config['DATABASE'])
