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

app = Flask(__name__)
# API
app.register_blueprint(frames, url_prefix="/api/frames")
app.register_blueprint(rules, url_prefix="/api/rules")

# Web Pages
app.register_blueprint(index, url_prefix="/admin")
app.register_blueprint(web_frames, url_prefix="/admin/frames")


@app.route('/')
def home():
    return "Index page"

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
    print("Sending frames")

    dbManager = initDb()
    data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])
    id = data[0]
    id = id[0]
    dbManager.close()

    counter = 0
    # Loop unless disconnection
    while not thread_stop_event.isSet():
        dbManager = initDb()

        # Prendre le plus grand id avant le while

        # Mettre cet id dans une variable
        # Faire la requete avec
        # Comparaison avec l'acnien id si nouveau envoie 
        #incremener la variable

        # data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])

        # data = dbManager.queryGet("SELECT * FROM `Frame` WHERE `id`=?", [id + counter])
        # counter += 1
        
        if counter == 20:
            counter = 0
            data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])
            id = data[0]
            id = id[0]
            sleep(0.3)
        else:
            data = dbManager.queryGet("SELECT * FROM `Frame` WHERE `id`=?", [id + counter])
            sleep(0.3)

        counter += 1
        newId = data[0]
        socketio.emit('newnumber', {'id':newId[0]}, namespace='/test')
        # socketio.sleep(0.5)
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
