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


alertDevices = Blueprint("alertDevices", __name__)


# GET ALL

@alertDevices.route('/', methods=['GET'])
def apiGetDeviceAlerts():
    req = "SELECT * FROM DeviceAlert"
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
        d["idDevice"] = row[5]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# GET ALL BASED ON DEVICE

@alertDevices.route('/', methods=['GET'])
@alertDevices.route('/<id>', methods=['GET'])
def apiGetDeviceAlertsId(id=None):
    dbManager = initDb()
    data = dbManager.queryGet(
        "SELECT * FROM DeviceAlert WHERE idDevice = ?", [id])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["level"] = row[1]
        d["date"] = row[2]
        d["type"] = row[3]
        d["description"] = row[4]
        d["idDevice"] = row[5]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# POST

@alertDevices.route('/', methods=['POST'])
def apiPostDeviceAlert():
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

        if "idDevice" not in alert or alert["idDevice"] == "":
            alert["idDevice"] = None

        dbManager.queryInsert("INSERT INTO `DeviceAlert` (`level`, `date`, `type`, `description`, `idDevice`) VALUES (?, ?, ?, ?, ?)",
                              [
                                  alert["level"],
                                  alert["date"],
                                  alert["type"],
                                  alert["description"],
                                  alert["idDevice"]
                              ])
        dbManager.close()
        return success.return_response(status=201, message="Alert added successfully")
    else:
        return error.return_response(status=400, message="Need JSON data")


# DELETE ALERTS FROM A DEVICE

@alertDevices.route('/', methods=['DELETE'])
@alertDevices.route('/<id>', methods=['DELETE'])
def apiDeleteDeviceAlerts(id=None):
    if id:
        dbManager = initDb()
        dbManager.queryInsert(
            "DELETE FROM DeviceAlert WHERE idDevice = ?", [id])
        return success.return_response(status=200, message="Alert(s) deleted successfully")
    else:
        return error.return_response(status=400, message="Need an ID")
    return 0

# Get number of alerts by time


@alertDevices.route('/alertsByDate', methods=['GET'])
def apiGetAlertsByDate():
    dbManager = initDb()
    req = 'SELECT DATE_FORMAT(date,"%m-%e-%Y"), COUNT(1) as alerts FROM DeviceAlert GROUP BY date ORDER BY date DESC limit 7'
    data = dbManager.queryGet(req, [])
    objects_list = []
    for row in data:
        d = {}
        d["date"] = row[0]
        d["alerts"] = row[1]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)
