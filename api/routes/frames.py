from flask import Blueprint, request, jsonify
import re

# Local
import database.db_config as config
from database import db_manager


def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager


frames = Blueprint("frames", __name__)

# GET all frames


@frames.route('/', methods=['GET'])
def apiFrames():
    if len(request.args) < 1:
        return "Need params"

    dbManager = initDb()

    # Initial request
    params = []
    req = []

    # if len(request.args) > 1:
    #     req.append("SELECT * FROM Frame WHERE ")
    # else:
    #     req.append("SELECT * FROM Frame ")
    req.append("SELECT * FROM Frame ")

    # Date request begin and end
    if request.args.get('startDate') and request.args.get('endDate'):
        reqDate = "date >= ? AND date <= ? "
        req.append(reqDate)
        params.append(request.args.get('startDate'))
        params.append(request.args.get('endDate'))
    else:
        # Date request begin
        if request.args.get('startDate'):
            reqDate = "date >= ? "
            req.append(reqDate)
            params.append(request.args.get('startDate'))
        # Date request end
        if request.args.get('endDate'):
            reqDate = "date <= ? "
            req.append(reqDate)
            params.append(request.args.get('endDate'))

    # Domain
    if request.args.get('domain'):
        reqDomain = "domain LIKE ? "
        req.append(reqDomain)
        params.append("%"+request.args.get('domain')+"%")

    # Info
    if request.args.get('info'):
        reqInfo = "info LIKE ? "
        req.append(reqInfo)
        params.append("%"+request.args.get('info')+"%")

    # Application
    if request.args.get('application'):
        reqApplication = "protocolLayerApplication LIKE ? "
        req.append(reqApplication)
        params.append("%"+request.args.get('application')+"%")

    # Transport
    if request.args.get('transport'):

        reqTransport = "protocolLayerTransport LIKE ? "
        req.append(reqTransport)
        params.append("%"+request.args.get('transport')+"%")

    # Network
    if request.args.get('network'):
        reqNetwork = "protocolLayerNetwork LIKE ? "
        req.append(reqNetwork)
        params.append("%"+request.args.get('network')+"%")

    # Limit request
    if request.args.get('limit'):
        reqLimit = "ORDER BY `id` DESC limit ? "
        req.append(reqLimit)
        params.append(request.args.get('limit'))
        # return req
        # data = dbManager.queryGet(req, params)
    else:
        return "Error : Need a limit"

    # Final Step
    finalReq = ""
    if len(request.args) > 1:
        for i in range(0, len(req)):
            if i == 1:
                finalReq += "WHERE "+req[i]
            else:
                if i > 1:
                    if i == len(req) - 1:
                        finalReq += req[i]
                    else:
                        finalReq += "AND " + req[i]
                else:
                    finalReq += req[i]
    else:
        for i in range(0, len(req)):
            finalReq += req[i]

    # return (str(finalReq)+" "+str(params))

    data = dbManager.queryGet(finalReq, params)
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["portSource"] = row[1]
        d["portDest"] = row[2]
        d["ipSource"] = row[3]
        d["ipDest"] = row[4]
        d["macAddrSource"] = row[5]
        d["macAddrDest"] = row[6]
        d["protocolLayerApplication"] = row[7]
        d["protocolLayerTransport"] = row[8]
        d["protocolLayerNetwork"] = row[9]
        d["date"] = row[10]
        d["domain"] = row[11]
        d["info"] = row[12]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)


# GET one frame


@frames.route('/', methods=['GET'])
@frames.route('/<id>', methods=['GET'])
def apiFramesId(id=None):
    if id:
        dbManager = initDb()
        data = dbManager.queryGet("SELECT * FROM Frame WHERE id=?", [id])
        objects_list = []
        for row in data:
            d = {}
            d["id"] = row[0]
            d["portSource"] = row[1]
            d["portDest"] = row[2]
            d["ipSource"] = row[3]
            d["ipDest"] = row[4]
            d["macAddrSource"] = row[5]
            d["macAddrDest"] = row[6]
            d["protocolLayerApplication"] = row[7]
            d["protocolLayerTransport"] = row[8]
            d["protocolLayerNetwork"] = row[9]
            d["date"] = row[10]
            d["domain"] = row[11]
            d["info"] = row[12]
            objects_list.append(d)
        dbManager.close()
        return jsonify(objects_list)
    else:
        return "Error : Need an id. "


# POST one frame
@frames.route('/', methods=['POST'])
def apiFramesCreate():
    if request.json:
        dbManager = initDb()
        data = request.get_json()
        frame = data[0]
        dbManager.queryInsert("INSERT INTO `Frame` (`portSource`, `portDest`, `ipSource`, `ipDest`, `macAddrSource`, `macAddrDest`, `protocolLayerApplication`, `protocolLayerTransport`, `protocolLayerNetwork`, `date`, `domain`, `info`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              [
                                  frame["portSource"],
                                  frame["portDest"],
                                  frame["ipSource"],
                                  frame["ipDest"],
                                  frame["macAddrSource"],
                                  frame["macAddrDest"],
                                  frame["protocolLayerApplication"],
                                  frame["protocolLayerTransport"],
                                  frame["protocolLayerNetwork"],
                                  frame["date"],
                                  frame["domain"],
                                  frame["info"]
                              ])
        dbManager.close()
        return "Create Success"
    else:
        return "Error : Need json data"


# Put one frame
@frames.route('/', methods=['PUT'])
@frames.route('/<id>', methods=['PUT'])
def apiFramesUpdate(id=None):
    if id:
        if request.json:
            dbManager = initDb()
            data = request.get_json()
            frame = data[0]
            # UPDATE `Frame` SET `portSource` = '22' WHERE `Frame`.`id` = 1
            dbManager.queryInsert("UPDATE `Frame` SET `portSource` = ?, `portDest` = ?, `ipSource` = ?, `ipDest` = ?, `macAddrSource` = ?, `macAddrDest` = ?, `protocolLayerApplication` = ?, `protocolLayerTransport` = ?, `protocolLayerNetwork` = ?, `date` = ?, `domain` = ?, `info` = ? WHERE `Frame`.`id` = ?",
                                  [
                                      frame["portSource"],
                                      frame["portDest"],
                                      frame["ipSource"],
                                      frame["ipDest"],
                                      frame["macAddrSource"],
                                      frame["macAddrDest"],
                                      frame["protocolLayerApplication"],
                                      frame["protocolLayerTransport"],
                                      frame["protocolLayerNetwork"],
                                      frame["date"],
                                      frame["domain"],
                                      frame["info"],
                                      id
                                  ])
            dbManager.close()
            return "Update Success"
        else:
            return "Error : Need json data."
    else:
        return "Error : Need an id."


# DELETE one frame
@frames.route('/', methods=['DELETE'])
@frames.route('/<id>', methods=['DELETE'])
def apiFramesDelete(id=None):
    if id:
        dbManager = initDb()
        dbManager.queryInsert(
            "DELETE FROM `Frame` WHERE `Frame`.`id` = ?", [id])
        dbManager.close()
        return "Delete Success"
    else:
        return "Error : Need an id."
