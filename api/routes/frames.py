from flask import Blueprint, request, jsonify
from flask_http_response import success, error

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
def apiGetFrames():
    if len(request.args) < 1:
        return error.return_response(status=400, message="Need params")

    dbManager = initDb()

    # Initial request
    params = []
    req = []

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

    # MAC Address Source
    if request.args.get('macAddrSource'):
        reqMac = "macAddrSource LIKE ? "
        req.append(reqMac)
        params.append("%"+request.args.get('macAddrSource')+"%")

    # MAC Address Dest
    if request.args.get('macAddrDest'):
        reqMac = "macAddrDest LIKE ? "
        req.append(reqMac)
        params.append("%"+request.args.get('macAddrDest')+"%")

    # Port Source
    if request.args.get('portSource'):
        reqPort = "portSource LIKE ? "
        req.append(reqPort)
        params.append("%"+request.args.get('portSource')+"%")

    # Port Dest
    if request.args.get('portDest'):
        reqPort = "portDest LIKE ? "
        req.append(reqPort)
        params.append("%"+request.args.get('portDest')+"%")

    # IP Source
    if request.args.get('ipSource'):
        reqIP = "ipSource LIKE ? "
        req.append(reqIP)
        params.append("%"+request.args.get('ipSource')+"%")

    # IP Dest
    if request.args.get('ipDest'):
        reqIP = "ipDest LIKE ? "
        req.append(reqIP)
        params.append("%"+request.args.get('ipDest')+"%")

    # Both Source and Dest
    # MAC
    if request.args.get('macSourceAndDest'):
        reqMac = '(macAddrDest LIKE ? OR macAddrSource LIKE ?) '
        req.append(reqMac)
        params.append("%"+request.args.get('macSourceAndDest')+"%")
        params.append("%"+request.args.get('macSourceAndDest')+"%")

    # Port
    if request.args.get('portSourceAndDest'):
        reqPort = '(portDest LIKE ? OR portSource LIKE ?) '
        req.append(reqPort)
        params.append("%"+request.args.get('portSourceAndDest')+"%")
        params.append("%"+request.args.get('portSourceAndDest')+"%")

    # IP
    if request.args.get('ipSourceAndDest'):
        reqIP = '(ipDest LIKE ? OR ipSource LIKE ?) '
        req.append(reqIP)
        params.append("%"+request.args.get('ipSourceAndDest')+"%")
        params.append("%"+request.args.get('ipSourceAndDest')+"%")

    # Limit request
    if request.args.get('limit'):
        reqLimit = "ORDER BY `id` DESC limit ? "
        req.append(reqLimit)
        params.append(request.args.get('limit'))
        # return req
        # data = dbManager.queryGet(req, params)
    else:
        return error.return_response(status=400, message="Need a limit")

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
def apiGetFrame(id=None):
    if id:
        dbManager = initDb()
        data = dbManager.queryGet("SELECT * FROM Frame WHERE id=?", [id])
        d = {}
        d["id"] = data[0]
        d["portSource"] = data[1]
        d["portDest"] = data[2]
        d["ipSource"] = data[3]
        d["ipDest"] = data[4]
        d["macAddrSource"] = data[5]
        d["macAddrDest"] = data[6]
        d["protocolLayerApplication"] = data[7]
        d["protocolLayerTransport"] = data[8]
        d["protocolLayerNetwork"] = data[9]
        d["date"] = data[10]
        d["domain"] = data[11]
        d["info"] = data[12]
        dbManager.close()
        return jsonify(d)
    else:
        return error.return_response(status=400, message="Need an ID")

# Get unique MAC address from frames


@frames.route('/macAddr', methods=['GET'])
def apiGetMac():
    dbManager = initDb()
    req = "SELECT macAddrSource as macAddr, MAX(date) as date FROM Frame GROUP BY macAddrSource UNION SELECT macAddrDest, MAX(date) FROM Frame GROUP BY macAddrDest"
    data = dbManager.queryGet(req, [])
    objects_list = []
    for row in data:
        d = {}
        d["macAddr"] = row[0]
        d["date"] = row[1]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)

# Get new MAC address to insert


@frames.route('/macToInsert', methods=['GET'])
def apiGetMacToInsert():
    dbManager = initDb()
    req = "SELECT Frame.macAddrSource as macAddr, MAX(date) as date FROM Frame LEFT JOIN Device ON Device.macAddr = Frame.macAddrSource WHERE Device.macAddr IS NULL GROUP BY macAddrSource UNION SELECT Frame.macAddrDest, MAX(date)FROM Frame LEFT JOIN Device ON Device.macAddr = Frame.macAddrDest WHERE Device.macAddr IS NULL GROUP BY macAddrDest"
    data = dbManager.queryGet(req, [])
    objects_list = []
    for row in data:
        d = {}
        d["macAddr"] = row[0]
        d["date"] = row[1]
        objects_list.append(d)
    dbManager.close()
    return jsonify(objects_list)
