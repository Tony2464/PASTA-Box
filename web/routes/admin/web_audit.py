from flask.helpers import url_for
import requests
import ipaddress
import json
import database.db_config as config
from audit.objects.Device import Device
from audit.scanVulnDevices import main as scanIP
from audit.manageAudit import getAuditMode, changeAuditMode, addTempDevice
from database import db_manager
from flask import Blueprint, render_template, request, redirect
from flask_http_response import success, error
from . import web_connection_required as web_connect

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_audit = Blueprint("web_audit", __name__)


# Check IP version

def checkIP(IP):
    try:
        return 1 if type(ipaddress.ip_address(IP)) is ipaddress.IPv4Address else 2
    except ValueError:
        return 3


@web_audit.route('/')
@web_connect.web_connection_required
def systemHomepage():
    auditMode = getAuditMode()
    return render_template('pages/audit.html', content=auditMode)


# Change audit mode

@web_audit.route('/mode', methods=['POST'])
def auditMode():
    Mode = request.get_json()
    res = changeAuditMode(Mode)

    if(res != 0):
        return error.return_response(status=400, message="Wrong audit mode")
    else:
        return success.return_response(status=200, message="Audit mode changed successfully, wait a few seconds...")


# Scan a specific IP address

@web_audit.route('/scanip', methods=['POST'])
def scanSpecificIP():
    data = request.get_json()
    res = checkIP(data["ipAddr"])
    if res == 3:
        return error.return_response(status=400, message="This is not an IP address")

    r = requests.get('http://localhost/api/devices/', params=data)
    device = r.json()
    if(len(device) == 0):
        newDevice = addTempDevice(data["ipAddr"])
        deviceID = newDevice.id
    else:
        
        try:

            temp = device[0]["ip"]

        except Exception:

            newDevice = Device(device["netBios"], device["systemOS"],
                                device["ipAddr"], device["macAddr"], None)
            deviceID = device["id"]
            # scanIP(newDevice)
            
        else:
            return error.return_response(status=400, message="This IP address is used by several devices")

    return redirect(url_for("web_device.getDevice", id=deviceID), code=303)
