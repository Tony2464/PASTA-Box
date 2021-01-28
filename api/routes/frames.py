import sys
from flask import Flask, request, jsonify

# Local
from __main__ import app  # For route
import main  # For dBmanager

dbManager = main.dbManager

# GET all frames


@app.route('/api/frames', methods=['GET'])
def apiFrames():
    data = dbManager.queryGet("SELECT * FROM Frame", [])
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
        d["idDeviceSource"] = row[11]
        d["idDeviceDest"] = row[12]
        d["idNetworkSource"] = row[13]
        d["idNetworkDest"] = row[14]
        d["domain"] = row[15]
        objects_list.append(d)
    return jsonify(objects_list)


# GET one frame


@app.route('/api/frames/', methods=['GET'])
@app.route('/api/frames/<id>', methods=['GET'])
def apiFramesId(id=None):
    if id:
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
            d["idDeviceSource"] = row[11]
            d["idDeviceDest"] = row[12]
            d["idNetworkSource"] = row[13]
            d["idNetworkDest"] = row[14]
            d["domain"] = row[15]
            objects_list.append(d)
        return jsonify(objects_list)
    else:
        return "Error : Need an id. "


# POST one frame
@app.route('/api/frames', methods=['POST'])
def apiFramesCreate():
    if request.json:
        data = request.get_json()
        frame = data[0]
        dbManager.queryInsert("INSERT INTO `Frame` (`portSource`, `portDest`, `ipSource`, `ipDest`, `macAddrSource`, `macAddrDest`, `protocolLayerApplication`, `protocolLayerTransport`, `protocolLayerNetwork`, `date`, `idDeviceSource`, `idDeviceDest`, `idNetworkSource`, `idNetworkDest`, `domain`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                                  frame["idDeviceSource"],
                                  frame["idDeviceDest"],
                                  frame["idNetworkSource"],
                                  frame["idNetworkDest"],
                                  frame["domain"]
                              ])
        return "Create Success"
    else:
        return "Error : Need json data"


# Put one frame
@app.route('/api/frames/', methods=['PUT'])
@app.route('/api/frames/<id>', methods=['PUT'])
def apiFramesUpdate(id=None):
    if id:
        if request.json:
            data = request.get_json()
            frame = data[0]
            # UPDATE `Frame` SET `portSource` = '22' WHERE `Frame`.`id` = 1
            dbManager.queryInsert("UPDATE `Frame` SET `portSource` = ?, `portDest` = ?, `ipSource` = ?, `ipDest` = ?, `macAddrSource` = ?, `macAddrDest` = ?, `protocolLayerApplication` = ?, `protocolLayerTransport` = ?, `protocolLayerNetwork` = ?, `date` = ?, `idDeviceSource` = ?, `idDeviceDest` = ?, `idNetworkSource` = ?, `idNetworkDest` = ?, `domain` = ? WHERE `Frame`.`id` = ?",
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
                                      frame["idDeviceSource"],
                                      frame["idDeviceDest"],
                                      frame["idNetworkSource"],
                                      frame["idNetworkDest"],
                                      frame["domain"],
                                      id
                                  ])
            return "Update Success"
        else:
            return "Error : Need json data."
    else:
        return "Error : Need an id."


# DELETE one frame
@app.route('/api/frames/', methods=['DELETE'])
@app.route('/api/frames/<id>', methods=['DELETE'])
def apiFramesDelete(id=None):
    if id:
        dbManager.queryInsert(
            "DELETE FROM `Frame` WHERE `Frame`.`id` = ?", [id])
        return "Delete Success"
    else:
        return "Error : Need an id."
