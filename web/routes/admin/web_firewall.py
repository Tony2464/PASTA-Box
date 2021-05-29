# Local
import database.db_config as config
import requests
from database import db_manager

# Flask
from firewall.customRules import buildCustomRules
from flask import Blueprint, render_template, request
from flask_http_response import success, error

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"],
)

web_firewall = Blueprint("web_firewall", __name__)


@web_firewall.route("/")
def homepage():
    r = requests.get("http://localhost/api/rules")
    data = r.json()
    return render_template("pages/firewall.html", content=data)


@web_firewall.route("/rule", methods=["POST"])
def addRule():

    Rule = request.get_json()

    res = buildCustomRules(Rule, True)
    if(res != 0):
        return error.return_response(message=switchError(res))

    requests.post("http://localhost/api/rules", json=Rule)
    return success.return_response(status=200)


@web_firewall.route('/rule/delete', methods=['POST'])
def deleteRule():

    id = request.form['id']

    if(id):
        
        response = requests.get("http://localhost/api/rules/" + str(id))
        Rule = response.json()
        res = buildCustomRules(Rule, False)

        if res == 0:
            requests.delete("http://localhost/api/rules/" + str(id))
            return success.return_response(status=200)
        else:
            return error.return_response(status=400)
    
    else:
        return error.return_response(status=400)


# All the errors from the function verifyRule in firewall/customRules.py

def switchError(result):

    switcher = {
        -1: "error_proto",
        -2: "error_icmp",
        -3: "no_inputs",
        -4: "error_ipvers_dst",
        -5: "error_ipvers_src",
        -6: "error_ipvers_notsame",
        -7: "error_port_src",
        -8: "error_port_dst",
    }

    return switcher.get(result, 1)
