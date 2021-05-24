from flask import Blueprint, render_template

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

web_index = Blueprint("web_index", __name__)

@web_index.route('/')
def homepage():
    return render_template('pages/index.html')


