import requests
import threading
from flask import Blueprint, render_template, redirect
from flask_http_response import success, error

# Local
import database.db_config as config
from database import db_manager
from . import web_connection_required as web_connect
from audit.scanVulnDevices import main as scanIP
from audit.objects.Device import Device

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_device = Blueprint("web_device", __name__)


@web_device.route('/<id>')
@web_device.route('/')
@web_connect.web_connection_required
def getDevice(id=None):
    if not id:
        return redirect("/admin/map", code=400)
    r = requests.get('http://localhost/api/devices/' + id)
    data = r.json()
    r2 = requests.get('http://localhost/api/alert_devices/' + id)
    content = r2.json()

    temp = 0
    for i in range(len(content)):
        if(content[i]["level"] > temp):
            temp = content[i]["level"]

    return render_template('pages/device.html', device=data, max=temp)


# Scan the device

@web_device.route('/scan/<id>/', methods=['POST'])
def scanDevice(id=None):
    if not id:
        return error.return_response(status=400, message="This device cannot be scanned without knowing the ID")
    r = requests.get('http://localhost/api/devices/' + id)
    data = r.json()
    
    if(int(data["activeStatus"]) == 2):
        return error.return_response(status=400, message="This device is still being scanned")
    if(int(data["activeStatus"]) == 0):
        return error.return_response(status=400, message="This device isn't active on the network, it cannot be scanned")
   
    device = Device(data["netBios"], data["systemOS"],
                    data["ipAddr"], data["macAddr"], None)
    t = threading.Thread(target=scanIP, args=(device,id,))
    t.start()
    return success.return_response(status=200, message="Your device is being scanned")
