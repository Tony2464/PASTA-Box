import sys
import requests

from flask import Flask, redirect, url_for
from flask.templating import render_template

#Local imports
# sys.path.append("./conf")
# import config as config
# import db_connect as db

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
from routes import homepages

# @app.route('/')
# @app.route('/<name>')
# def index(name=None):
#         return render_template('index.html', content=name)

# @app.route('/frames')
# def getFrames():
#         r = requests.get('http://192.168.0.52:5000/api/frames')
#         # data = jsonify(r.json())
#         data = r.json()
#         return render_template('frames.html',content=data,content2="Bonjour")
#         # return data

# @app.route('/admin')
# def admin():
#         return redirect(url_for("index"))


# if __name__ == "__main__":
#         app.run(host=config.hostConfig, debug=config.debugMode, port=8080)
if __name__ == "__main__":
    app.run(host=config.hostConfig, debug=config.debugMode)
