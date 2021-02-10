import sys
import requests

from flask import Flask, redirect, url_for
from flask.templating import render_template

#Local imports

import web.conf.config as config
from database import db_manager

app = Flask(__name__)

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

#Import all routes
import web.routes.homepages

if __name__ == "__main__":
    app.run(host=config.hostConfig, debug=config.debugMode)
