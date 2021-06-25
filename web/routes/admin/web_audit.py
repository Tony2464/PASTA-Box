import database.db_config as config
from audit.manageAudit import getAuditMode, changeAuditMode
from database import db_manager
from flask import Blueprint, render_template, request
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


@web_audit.route('/')
@web_connect.web_connection_required
def systemHomepage():
    auditMode = getAuditMode()
    return render_template('pages/audit.html', content=auditMode)


@web_audit.route('/mode', methods=['POST'])
def auditMode():
    Mode = request.get_json()
    res = changeAuditMode(Mode)

    if(res != 0):
        return error.return_response(status=400, message="Wrong audit mode")
    else:
        return success.return_response(status=200, message="Audit mode changed successfully, wait a few seconds...")
