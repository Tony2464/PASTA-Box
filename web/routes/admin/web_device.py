from flask import Blueprint, render_template, redirect
import requests

# Local
import database.db_config as config
from database import db_manager

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
def getDevice(id=None):
    if not id:
        return redirect("/admin/map", code=400)
    r = requests.get('http://localhost/api/devices/'+id)
    data = r.json()
    return render_template('pages/device.html',device=data)


