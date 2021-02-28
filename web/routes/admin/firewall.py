from flask import Blueprint, render_template, request, jsonify
import requests

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

firewall = Blueprint("firewall", __name__)

@firewall.route('/')
def homepage():
    r = requests.get('http://localhost/api/rules')
    data = r.json()
    return render_template('pages/firewall.html', content=data)
