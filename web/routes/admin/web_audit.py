import database.db_config as config
from database import db_manager

from flask import Blueprint, render_template, request
from flask_http_response import success
from settings.systemCommands import *
from settings.systemSettings import *

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_audit = Blueprint("web_audit", __name__)


@web_audit.route('/')
def systemHomepage():
    return render_template('pages/audit.html')
