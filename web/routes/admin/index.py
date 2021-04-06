from flask import Blueprint, render_template, request, jsonify

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

index = Blueprint("index", __name__)

@index.route('/')
def homepage():
    return render_template('pages/index.html')
