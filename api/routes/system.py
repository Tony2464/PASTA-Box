from flask import Blueprint, jsonify
from flask_http_response import success, error
import psutil
import platform
from datetime import datetime

# Local
import database.db_config as config
from database import db_manager

# Convert to readable format


def getSize(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


system = Blueprint("system", __name__)


# GET System info

@system.route('/info', methods=['GET'])
def apiGetSystem():
    data = {}
    data["totalCpu"] = psutil.cpu_percent()
    svmem = psutil.virtual_memory()
    data["totalMemPercent"] = psutil.virtual_memory().percent
    data["totalMem"] = getSize(svmem.total)
    data["usedMem"] = getSize(svmem.used)
    uname = platform.uname()
    data["hostname"] = uname.node
    return jsonify(data)
