from flask import Blueprint, render_template
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

web_frames = Blueprint("web_frames", __name__)

@web_frames.route('/')
def getFrames():
    r = requests.get('http://192.168.0.52/api/frames')
    data = r.json()
    return render_template('frames.html', content=data)
