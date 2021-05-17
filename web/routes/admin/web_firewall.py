# Local
import database.db_config as config
import requests
from database import db_manager

# Flask
from firewall.customRules import buildCustomRules
from flask import Blueprint, render_template, request
from flask_http_response import result, success

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

web_firewall = Blueprint("web_firewall", __name__)


@web_firewall.route('/')
def homepage():
    r = requests.get('http://localhost/api/rules')
    data = r.json()
    return render_template('pages/firewall.html', content=data)


@web_firewall.route('/rule', methods=['POST'])
def addRule():

    Rule = request.get_json()

    res = buildCustomRules(Rule)
    if(res != 0):
        return switchError(result)

    requests.post('http://localhost/api/rules', json=Rule)
    return success.return_response(status=200)


# All the errors from the function verifyRule in customRules.py

def switchError(result):
    switcher = {

        -1: "error_proto",
        -2: "error_icmp",
        -3: "no_inputs",
        -4: "error_ipvers_dst",
        -5: "error_ipvers_src",
        -6: "error_ipvers_notsame",
        -7: "error_port_src",
        -8: "error_port_dst"

    }

    return switcher.get(result, 1)
