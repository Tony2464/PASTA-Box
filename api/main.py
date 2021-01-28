import sys

from flask import Flask

#local imports
from conf import config
sys.path.append("..")
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
from routes import frames

if __name__ == "__main__":
    app.run(host=config.hostConfig, debug=config.debugMode)
