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

web_frames = Blueprint("web_frames", __name__)

@web_frames.route('/')
@web_connect.web_connection_required
def getFrames():
    return render_template('pages/frames.html')


@web_frames.route('/live')
@web_connect.web_connection_required
def getFramesLive():
    return render_template('pages/frames_live.html')
