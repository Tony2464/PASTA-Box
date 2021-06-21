from flask import Blueprint, render_template, session, current_app, url_for
import requests

# Local
import database.db_config as config
from database import db_manager
from . import web_connection_required as web_connect

from flask import request, redirect
import jwt
import datetime
from functools import wraps
import jwt

import sys
sys.path.append("..")


def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


web_connection = Blueprint("web_connection", __name__)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        # Check token presence
        if not token:
            return redirect("/admin/account/login", code=401)
        # Check token validity
        try:
            token = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return redirect("/admin/account/login", code=401)
        # Check token expiration
        if token["expiration"]:
            tokenTime = token["expiration"]
            if tokenTime != "never":
                if datetime.datetime.strptime(tokenTime, "%Y-%m-%d %X.%f") < datetime.datetime.now():
                    return redirect("/admin/account/login", code=401)
        return func(*args, **kwargs)
    # Continue
    return decorated

# Test


@web_connection.route('/auth', methods=['GET'])
# @token_required
@web_connect.web_connection_required
def auth():
    return "Session created, welcome."


@web_connection.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form['email'] and request.form['password']:
            params = {
                'email': request.form['email'],
                'password': request.form['password']
            }
            r = requests.post('http://localhost/api/user/login', data=params)

            returnCode = str(r.status_code)

            # return returnCode
            if returnCode == "200":
                data = r.json()
                session['id'] = data[0]['id']
                session['firstname'] = data[0]['firstname']
                return render_template('pages/index.html')
            # Badd request, missing email or password keys or values
            if returnCode == "400":
                return render_template('pages/login.html')
            # Wrong password
            if returnCode == "403":
                return render_template('pages/login.html', message="Sorry, wrong password.")
            # User not found
            if returnCode == "404":
                return render_template('pages/login.html', message="Sorry, wrong email.")

            return "Ah"

            # session['logged'] = True
            # token = jwt.encode(
            #     {
            #         "user": request.form['email'],
            #         "expiration": str(datetime.datetime.now() + datetime.timedelta(seconds=30))
            #     },
            #     current_app.config['SECRET_KEY'],
            #     algorithm="HS256"
            # )
            # resp = make_response()
            # resp.set_cookie('token', token, httponly=True)
            # return resp
        else:
            render_template('pages/login.html')
    else:
        return render_template('pages/login.html')


@web_connection.route('/logout', methods=['GET'])
@web_connect.web_connection_required
def logOut():
    session.pop('id', default=None)
    session.pop('firstname', default=None)
    return redirect(url_for('web_connection.login'))
