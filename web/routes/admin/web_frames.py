from flask import Blueprint, json, render_template
from flask.helpers import url_for
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
    return render_template('pages/frames.html')


@web_frames.route('/live')
def getFramesLive():
    return render_template('pages/frames_live.html')
