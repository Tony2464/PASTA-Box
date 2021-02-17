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
        d["ip"] = row[1]
        d["port"] = row[2]
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
            d["ip"] = row[1]
            d["port"] = row[2]
            objects_list.append(d)
        return jsonify(objects_list)
    else:
        return "Error : Need an id. "


# POST one rule

@rules.route('/', methods=['POST'])
def apiRulesCreate():
    if request.json:
        data = request.get_json()
        rule = data[0]
        dbManager.queryInsert("INSERT INTO `RuleFirewall` (`ip`, `port`) VALUES (?, ?)",
                              [
                                  rule["ip"],
                                  rule["port"]
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
            "DELETE FROM `RuleFirewall` WHERE `RuleFirewall`.`id` = ?", [id])
        return "Delete Success"
    else:
        return "Error : Need an id."
