from flask import Blueprint, request, jsonify

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


devices = Blueprint("devices", __name__)

# GET ALL


@devices.route('/', methods=['GET'])
def apiGetDevices():
    return 0

# GET ONE


@devices.route('/', methods=['GET'])
@devices.route('/<id>', methods=['GET'])
def apiGetDevice(id=None):
    return 0

# POST


@devices.route('/', methods=['POST'])
def apiPostDevice():
    return 0

# PUT


@devices.route('/', methods=['PUT'])
@devices.route('/<id>', methods=['PUT'])
def apiPutDevice(id=None):
    return 0

# DELETE


@devices.route('/', methods=['DELETE'])
@devices.route('/<id>', methods=['DELETE'])
def apiDeleteDevice(id=None):
    return 0
