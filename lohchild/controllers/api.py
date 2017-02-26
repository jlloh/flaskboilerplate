from flask import Blueprint, render_template, request, redirect, session, Response, current_app, url_for
from flask_login import login_required, current_user, login_user
from oauth2client import client, crypt

import json

from ..controllers.model import User

api = Blueprint('api', __name__)

@api.route('/tokensignin', methods = ['POST'])
def validate_token():
    id_token = request.form['idtoken']
    idinfo = client.verify_id_token(id_token, current_app.config['GOOGLE_APP_ID'])
    user_id = idinfo['sub']
    email = idinfo['email']
    username = email
    print email
    validuser = False
    user = User(username, current_app.config['DATABASE'])
    if user.is_anonymous() == True:
        error = 'Unregistered User'
        redirect = url_for('user_control.login')
    else:
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            error = 'Wrong client'
            redirect = url_for('user_control.login')
        else:
            login_user(user)
            redirect = url_for('home.homepage')
            validuser = True 
    return json.dumps({'redirect_url': redirect, 'validuser': validuser})

