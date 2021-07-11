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


services = Blueprint("services", __name__)


# GET ALL

@services.route('/', methods=['GET'])
def apiGetServices():
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM Service", [])
    objects_list = []
    for row in data:
        d = {}
        d["idService"] = row[0]
        d["idDevice"] = row[1]
        d["numberPort"] = row[2]
        d["type"] = row[3]
        d["serviceName"] = row[4]
        d["serviceVersion"] = row[5]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# GET ALL BASED ON DEVICE

@services.route('/', methods=['GET'])
@services.route('/<id>', methods=['GET'])
def apiGetService(id=None):
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM Service WHERE idDevice = ?", [id])
    objects_list = []
    for row in data:
        d = {}
        d["idService"] = row[0]
        d["idDevice"] = row[1]
        d["numberPort"] = row[2]
        d["type"] = row[3]
        d["serviceName"] = row[4]
        d["serviceVersion"] = row[5]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)


# POST

@services.route('/', methods=['POST'])
def apiPostService():
    if request.json:
        dbManager = initDb()
        service = request.get_json()
        print(service)
        # Check every key and its value
        if "type" not in service or service["type"] == "":
            service["type"] = None

        if "serviceName" not in service or service["serviceName"] == "":
            service["serviceName"] = None

        if "serviceVersion" not in service or service["serviceVersion"] == "":
            service["serviceVersion"] = None

        dbManager.queryInsert("INSERT INTO `Service` (`idDevice`, `numberPort`, `type`, `serviceName`, `serviceVersion`) VALUES (?, ?, ?, ?, ?)",
                              [
                                  service["idDevice"],
                                  service["numberPort"],
                                  service["type"],
                                  service["serviceName"],
                                  service["serviceVersion"]
                              ])
        dbManager.close()
        return success.return_response(status=201, message="Service added successfully")
    else:
        return error.return_response(status=400, message="Need JSON data")


# DELETE

@services.route('/', methods=['DELETE'])
@services.route('/<id>', methods=['DELETE'])
def apiDeleteService(id=None):
    return 0
