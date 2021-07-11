# Local
import database.db_config as config
from database import db_manager

from flask import Blueprint, jsonify, request
from flask_http_response import error, success


def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


alertProtocol = Blueprint("alertProtocol", __name__)


# GET ALL

@alertProtocol.route('/', methods=['GET'])
def apiGetProtocolAlerts():
    req = "SELECT * FROM ProtocolAlert"
    params = []
    dbManager = initDb()
    data = dbManager.queryGet(req, params)
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["level"] = row[1]
        d["date"] = row[2]
        d["type"] = row[3]
        d["description"] = row[4]
        d["idFrame"] = row[5]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# GET ALL BASED ON FRAME

@alertProtocol.route('/', methods=['GET'])
@alertProtocol.route('/<id>', methods=['GET'])
def apiGetProtocolAlertsId(id=None):
    dbManager = initDb()
    data = dbManager.queryGet(
        "SELECT * FROM ProtocolAlert WHERE idFrame = ?", [id])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["level"] = row[1]
        d["date"] = row[2]
        d["type"] = row[3]
        d["description"] = row[4]
        d["idFrame"] = row[5]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# POST

@alertProtocol.route('/', methods=['POST'])
def apiPostProtocolAlert():
    if request.json:
        dbManager = initDb()
        alert = request.get_json()

        # Check every key and its value
        if "level" not in alert or alert["level"] == "":
            alert["level"] = None

        if "date" not in alert or alert["date"] == "":
            alert["date"] = None

        if "type" not in alert or alert["type"] == "":
            alert["type"] = None

        if "description" not in alert or alert["description"] == "":
            alert["description"] = None

        if "idFrame" not in alert or alert["idFrame"] == "":
            alert["idFrame"] = None

        dbManager.queryInsert("INSERT INTO `ProtocolAlert` (`level`, `date`, `type`, `description`, `idFrame`) VALUES (?, ?, ?, ?, ?)",
                              [
                                  alert["role"],
                                  alert["idNetwork"],
                                  alert["macAddr"],
                                  alert["ipAddr"],
                                  alert["securityScore"]
                              ])
        dbManager.close()
        return success.return_response(status=201, message="Alert added successfully")
    else:
        return error.return_response(status=400, message="Need JSON data")


# DELETE

@alertProtocol.route('/', methods=['DELETE'])
@alertProtocol.route('/<id>', methods=['DELETE'])
def apiDeleteProtocolAlert(id=None):
    return 0
