from flask import Blueprint, request, jsonify

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

rules = Blueprint("rules", __name__)


# GET all rules

@rules.route('/', methods=['GET'])
def apiRules():
    data = dbManager.queryGet("SELECT * FROM RuleFirewall", [])
    objects_list = []
    for row in data:
        d = {}
        d["id"] = row[0]
        d["ipDst"] = row[1]
        d["ipSrc"] = row[2]
        d["portDst"] = row[3]
        d["portSrc"] = row[4]
        d["protocol"] = row[5]
        d["ipVersion"] = row[6]
        objects_list.append(d)
    return jsonify(objects_list)


# GET one rule

@rules.route('/', methods=['GET'])
@rules.route('/<id>', methods=['GET'])
def apiRulesId(id=None):
    if id:
        data = dbManager.queryGet(
            "SELECT * FROM RuleFirewall WHERE id=?", [id])
        objects_list = []
        for row in data:
            d = {}
            d["id"] = row[0]
            d["ipDst"] = row[1]
            d["ipSrc"] = row[2]
            d["portDst"] = row[3]
            d["portSrc"] = row[4]
            d["protocol"] = row[5]
            d["ipVersion"] = row[6]
        objects_list.append(d)
        return jsonify(objects_list)
    else:
        return "Error : Need an id. "


# POST one rule

@rules.route('/', methods=['POST'])
def apiRulesCreate():
    if request.json:
        rule = request.get_json()
        if(rule["portDst"] == ""):
            rule["portDst"] = None
        if(rule["portSrc"] == ""):
            rule["portSrc"] = None
        if(rule["protocol"] == ""):
            rule["protocol"] = None
        if(rule["ipVersion"] == ""):
            rule["ipVersion"] = None
        dbManager.queryInsert("INSERT INTO `RuleFirewall` (`ipDest`, `ipSource`, `portDest`, `portSource`, `protocol`, `ipVersion`) VALUES (?, ?, ?, ?, ?, ?)",
                              [
                                  rule["ipDst"],
                                  rule["ipSrc"],
                                  rule["portDst"],
                                  rule["portSrc"],
                                  rule["protocol"],
                                  rule["ipVersion"]
                              ])
        return "Create Success"
    else:
        return "Error : Need json data"


# DELETE one frame

@rules.route('/', methods=['DELETE'])
@rules.route('/<id>', methods=['DELETE'])
def apiRulesDelete(id=None):
    if id:
        dbManager.queryInsert(
            "DELETE FROM RuleFirewall WHERE id = ?", [id])
        return "Delete Success"
    else:
        return "Error : Need an id."
