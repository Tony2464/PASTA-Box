from flask import Blueprint, json, render_template
from flask.helpers import url_for

# Local
import database.db_config as config
from database import db_manager

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_settings = Blueprint("web_settings", __name__)

@web_settings.route('/')
@web_settings.route('/network/')
def getFrames():
    return render_template('pages/network_settings.html')
