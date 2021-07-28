# Local
import database.db_config as config
from database import db_manager

import ipaddress
from flask import Blueprint, jsonify, request
from flask_http_response import error, success
import json

def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


devices = Blueprint("devices", __name__)


# GET ALL

@devices.route('/', methods=['GET'])
def apiGetDevices():
    if request.args.get("macAddr") and request.args.get("ipAddr"):
        req = "SELECT * FROM Device WHERE macAddr = ? AND ipAddr = ?"
        params = [request.args.get("macAddr"), request.args.get("ipAddr")]
    elif request.args.get("ipAddr"):
        req = "SELECT * FROM Device WHERE ipAddr = ?"
        params = [request.args.get("ipAddr")]
    else:
        req = "SELECT * FROM Device"
        params = []
    dbManager = initDb()
    data = dbManager.queryGet(req, params)
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["role"] = row[1]
        d["idNetwork"] = row[2]
        d["macAddr"] = row[3]
        d["ipAddr"] = row[4]
        d["securityScore"] = row[5]
        d["netBios"] = row[6]
        d["activeStatus"] = row[7]
        d["firstConnection"] = row[8]
        d["lastConnection"] = row[9]
        d["lastScan"] = row[10]
        d["systemOS"] = row[11]
        objects_list.append(d)
    dbManager.close()
    if(len(objects_list) == 1):
        return jsonify(objects_list[0])
    else:
        return jsonify(objects_list)


# GET ONE

@devices.route('/', methods=['GET'])
@devices.route('/<id>', methods=['GET'])
def apiGetDevice(id=None):
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM Device WHERE id = ?", [id])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["role"] = row[1]
        d["idNetwork"] = row[2]
        d["macAddr"] = row[3]
        d["ipAddr"] = row[4]
        d["securityScore"] = row[5]
        d["netBios"] = row[6]
        d["activeStatus"] = row[7]
        d["firstConnection"] = row[8]
        d["lastConnection"] = row[9]
        d["lastScan"] = row[10]
        d["systemOS"] = row[11]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list[0])


# POST

@devices.route('/', methods=['POST'])
def apiPostDevice():
    if request.json:
        dbManager = initDb()
        device = request.get_json()

        # Check every key and its value
        if "role" not in device or device["role"] == "":
            device["role"] = None

        if "idNetwork" not in device or device["idNetwork"] == "":
            device["idNetwork"] = None

        if "macAddr" not in device or device["macAddr"] == "":
            device["macAddr"] = None

        if "ipAddr" not in device or device["ipAddr"] == "":
            device["ipAddr"] = None

        if "securityScore" not in device or device["securityScore"] == "":
            device["securityScore"] = None

        if "netBios" not in device or device["netBios"] == "":
            device["netBios"] = None

        if "activeStatus" not in device or device["activeStatus"] == "":
            device["activeStatus"] = None

        if "firstConnection" not in device or device["firstConnection"] == "":
            device["firstConnection"] = None

        if "lastConnection" not in device or device["lastConnection"] == "":
            device["lastConnection"] = None

        if "lastScan" not in device or device["lastScan"] == "":
            device["lastScan"] = None

        if "systemOS" not in device or device["systemOS"] == "":
            device["systemOS"] = None

        dbManager.queryInsert("INSERT INTO `Device` (`role`, `idNetwork`, `macAddr`, `ipAddr`, `securityScore`, `netBios`, `activeStatus`, `firstConnection`, `lastConnection`, `lastScan`, `systemOS`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              [
                                  device["role"],
                                  device["idNetwork"],
                                  device["macAddr"],
                                  device["ipAddr"],
                                  device["securityScore"],
                                  device["netBios"],
                                  device["activeStatus"],
                                  device["firstConnection"],
                                  device["lastConnection"],
                                  device["lastScan"],
                                  device["systemOS"]
                              ])
        dbManager.close()
        return success.return_response(status=201, message="Device added successfully")
    else:
        return error.return_response(status=400, message="Need JSON data")


# PUT

@devices.route('/', methods=['PUT'])
@devices.route('/<id>', methods=['PUT'])
def apiPutDevice(id=None):
    if id:
        if request.json:
            dbManager = initDb()
            device = request.get_json()

            # Initial request
            params = []
            req = []
            req.append("UPDATE `Device` SET ")

            # role
            if "role" in device and device["role"] != "":
                req.append("`role` = ?")
                params.append(device["role"])

            # idNetwork
            if "role" in device and device["role"] != "":
                req.append("`role` = ?")
                params.append(device["role"])

            # idNetwork
            if "idNetwork" in device and device["idNetwork"] != "":
                req.append("`idNetwork` = ?")
                params.append(device["idNetwork"])

            # macAddr
            if "macAddr" in device and device["macAddr"] != "":
                req.append("`macAddr` = ?")
                params.append(device["macAddr"])

            # ipAddr
            if "ipAddr" in device and device["ipAddr"] != "":
                req.append("`ipAddr` = ?")
                params.append(device["ipAddr"])

            # securityScore
            if "securityScore" in device and device["securityScore"] != "":
                req.append("`securityScore` = ?")
                params.append(device["securityScore"])

            # netBios
            if "netBios" in device and device["netBios"] != "":
                req.append("`netBios` = ?")
                params.append(device["netBios"])

            # activeStatus
            if "activeStatus" in device and device["activeStatus"] != "":
                req.append("`activeStatus` = ?")
                params.append(device["activeStatus"])

            # firstConnection
            if "firstConnection" in device and device["firstConnection"] != "":
                req.append("`firstConnection` = ?")
                params.append(device["firstConnection"])

            # lastConnection
            if "lastConnection" in device and device["lastConnection"] != "":
                req.append("`lastConnection` = ?")
                params.append(device["lastConnection"])

            # lastScan
            if "lastScan" in device and device["lastScan"] != "":
                req.append("`lastScan` = ?")
                params.append(device["lastScan"])

            # systemOS
            if "systemOS" in device and device["systemOS"] != "":
                req.append("`systemOS` = ?")
                params.append(device["systemOS"])

            # Concataining all the previous params
            finalReq = ""
            if len(device) > 1:
                for i in range(0, len(req)):
                    if i != len(req)-1 and i > 0:
                        finalReq += req[i]+","
                    else:
                        finalReq += req[i]
            else:
                for i in range(0, len(req)):
                    finalReq += req[i]

            # final id
            finalReq += ' WHERE id = ?'
            params.append(str(id))
            dbManager.queryInsert(finalReq, params)
            dbManager.close()

            return success.return_response(status=200, message="Device updated successfully")
        else:
            return error.return_response(status=400, message="Need JSON data")
    else:
        return error.return_response(status=400, message="Need an ID")


# DELETE

@devices.route('/', methods=['DELETE'])
@devices.route('/<id>', methods=['DELETE'])
def apiDeleteDevice(id=None):
    return 0


# Give all devices for map

@devices.route('/mapDevices')
def apiMapDevices():
    dbManager = initDb()
    data = dbManager.queryGet("SELECT * FROM Device", [])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["role"] = row[1]
        d["idNetwork"] = row[2]
        d["macAddr"] = row[3]
        d["ipAddr"] = row[4]
        d["securityScore"] = row[5]
        d["netBios"] = row[6]
        d["activeStatus"] = row[7]
        d["firstConnection"] = row[8]
        d["lastConnection"] = row[9]
        d["lastScan"] = row[10]
        d["systemOS"] = row[11]
        if d["ipAddr"] != None and checkIP(d["ipAddr"]) != 3 and ipaddress.ip_address(d["ipAddr"]).is_private and d["macAddr"] != None:
            objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)


# Settings configuration file
pastaConfigFile = "/PASTA-Box/settings/config.json"

# Get PASTA-Box system info
@devices.route('/pasta-info')
def apiGetPastaInfo():
    with open(pastaConfigFile, encoding="utf8", errors="ignore") as configFile:
        configData = configFile.read()
        configFile.close()
    return json.loads(configData)

# Check IP version


def checkIP(IP):
    try:
        return 1 if type(ipaddress.ip_address(IP)) is ipaddress.IPv4Address else 2
    except ValueError:
        return 3


@devices.route('/osRepartition', methods=['GET'])
def apiGetOsRepartition():
    dbManager = initDb()
    req = 'SELECT systemOS, COUNT(1) as occurrence FROM Device GROUP BY systemOS ORDER BY occurrence'
    data = dbManager.queryGet(req, [])
    objects_list = []
    for row in data:
        d = {}
        d["systemOS"] = row[0]
        d["occurrence"] = row[1]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)
