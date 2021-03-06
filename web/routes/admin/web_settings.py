# Local
import database.db_config as config
from database import db_manager
from . import web_connection_required as web_connect

# Flask
from flask import Blueprint, render_template, request
from flask_http_response import success, error
from settings.systemCommands import getCmd
from settings.systemSettings import getConfig, applyConfig, updateSystemFiles

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_settings = Blueprint("web_settings", __name__)


@web_settings.route('/')
@web_settings.route('/system/')
@web_connect.web_connection_required
def systemHomepage():
    configPasta = getConfig()
    return render_template('pages/system_settings.html', content=configPasta)


@web_settings.route('/system/', methods=['POST'])
def updateConfig():
    config = request.get_json()

    res = applyConfig(config)
    if(res != 0):
        return error.return_response(message=switchError(res))
    else:
        updateSystemFiles(config)
        return success.return_response(status=200)


# All the errors from the function verifyConfig in systemSettings.py

def switchError(result):
    switcher = {

        -1: "error_ip",
        -2: "error_gw",
        -3: "error_hostname",
        -4: "len_hostname",
        -5: "error_mask",
        -6: "error_cmd"

    }

    return switcher.get(result, 1)


@web_settings.route('/system/actions/', methods=['POST'])
def getCommand():
    action = request.get_json()
    res = getCmd(action['command'])

    if(res != 0):
        return error.return_response(message=switchError(res))
    else:
        return success.return_response(status=200)
