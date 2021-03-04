from types import new_class
from flask import Flask, jsonify
from flask.templating import render_template
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread, Event

# Local imports
import web.conf.config as config
import database.db_config as config
from database import db_manager

# Import all routes
# API routes
from api.routes.frames import frames
from api.routes.rules import rules

# Web pages routes
from web.routes.admin.index import index
from web.routes.admin.web_frames import web_frames
from web.routes.admin.firewall import firewall

app = Flask(__name__)
# API
app.register_blueprint(frames, url_prefix="/api/frames")
app.register_blueprint(rules, url_prefix="/api/rules")

# Web Pages
app.register_blueprint(index, url_prefix="/admin")
app.register_blueprint(web_frames, url_prefix="/admin/frames")
app.register_blueprint(firewall, url_prefix="/admin/firewall")


@app.route('/')
def home():
    return "test"

# Web 

def initDb():
    dbManager = db_manager.DbManager(
        config.dbConfig["user"],
        config.dbConfig["password"],
        config.dbConfig["host"],
        config.dbConfig["port"],
        config.dbConfig["database"]
    )
    return dbManager

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()
def sendFrames():
    #infinite loop of magical random numbers
    print("Sending frames")
    number = 0
    oldData = -1
    while not thread_stop_event.isSet():
        dbManager = initDb()    
        data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])
        # objects_list = []
        # for row in data:
        #     d = {}
        #     d["id"] = row[0]
        #     d["portSource"] = row[1]
        #     d["portDest"] = row[2]
        #     d["ipSource"] = row[3]
        #     d["ipDest"] = row[4]
        #     d["macAddrSource"] = row[5]
        #     d["macAddrDest"] = row[6]
        #     d["protocolLayerApplication"] = row[7]
        #     d["protocolLayerTransport"] = row[8]
        #     d["protocolLayerNetwork"] = row[9]
        #     d["date"] = row[10]
        #     d["idDeviceSource"] = row[11]
        #     d["idDeviceDest"] = row[12]
        #     d["idNetworkSource"] = row[13]
        #     d["idNetworkDest"] = row[14]
        #     d["domain"] = row[15]
        #     d["info"] = row[16]
        #     objects_list.append(d)
        # data = jsonify(objects_list)
        # number += 1
        # if data[0] != oldData:
        socketio.emit('newnumber', {'number': data[0],}, namespace='/test')
        # oldData = data[0]
        socketio.sleep(0.5)
        dbManager.close()

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    thread_stop_event.clear()

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(sendFrames)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    thread_stop_event.set()

if __name__ == "__main__":
    # app.run(host=config.hostConfig, debug=config.debugMode)
    socketio.run(app, host=config.hostConfig, debug=config.debugMode)
