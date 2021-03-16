from flask import Blueprint, json, request, jsonify
from flask.helpers import flash

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
    dbManager = initDb()
    if request.args.get('limit'):
        limit = request.args.get('limit')
        data = dbManager.queryGet(
            "SELECT * FROM Frame ORDER BY `id` DESC limit ?", [limit])
    else:
        data = dbManager.queryGet("SELECT * FROM Frame ORDER BY `id` DESC", [])
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
