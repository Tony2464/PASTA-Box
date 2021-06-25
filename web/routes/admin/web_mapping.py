from flask import Blueprint, render_template

# Local
import database.db_config as config
from database import db_manager
from . import web_connection_required as web_connect

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_mapping = Blueprint("web_mapping", __name__)


@web_mapping.route('/')
@web_connect.web_connection_required
def getMap():
    return render_template('pages/map.html')
