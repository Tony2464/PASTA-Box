# Local
import database.db_config as config
import requests
from database import db_manager
from . import web_connection_required as web_connect

# Flask
from flask import Blueprint, render_template, request
from flask_http_response import success, error

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_security_dashboard = Blueprint("web_security_dashboard", __name__)


@web_security_dashboard.route('/')
@web_connect.web_connection_required
def securityHomepage():
    r = requests.get('http://localhost/api/alert_devices/')
    data = r.json()
    return render_template('pages/security_dashboard.html', content=data)

