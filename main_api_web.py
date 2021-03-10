from types import new_class
from flask import Flask, jsonify
from flask.templating import render_template
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread, Event
from subprocess import Popen, PIPE, CalledProcessError

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

        # data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])

        # data = dbManager.queryGet("SELECT * FROM `Frame` WHERE `id`=?", [id + counter])
        # counter += 1
        
        # if counter == 20:
        #     counter = 0
        #     data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])
        #     id = data[0]
        #     id = id[0]
        #     # sleep(0.5)
        # else:
        #     data = dbManager.queryGet("SELECT * FROM `Frame` WHERE `id`=?", [id + counter])
        #     # sleep(0.5)

        # data = dbManager.queryGet(
        #     "SELECT * FROM `Frame` WHERE `id`=?", [id + counter])

        # counter += 1
        # newId = data[0]
    
        data = dbManager.queryGet("SELECT MAX(id) FROM `Frame`", [])

        #### 1
        # proc = subprocess.Popen(
        #     # call something with a lot of output so we can see it
        #     ["strace -p13579 -s9999 -e write"],
        #     shell=True,
        #     stdout=subprocess.PIPE,
        #     universal_newlines=True
        # )
        # for line in iter(proc.stdout.readline, ''):
        #     # Don't need this just shows the text streaming
        #     # time.sleep(1)
        #     socketio.sleep(1)
        #     # print(line.rstrip() + '<br/>\n')
        #     print("ok")
        #     socketio.emit('newnumber', {'id': line}, namespace='/test')
        ####


        #### 2
        # process = subprocess.Popen(shlex.split("strace -p13579 -s9999 -e write"), stdout=subprocess.PIPE)
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         # print(output.strip())
        #         socketio.emit('newnumber', {'id': output.strip()}, namespace='/test')

        # rc = process.poll()
        ####

        # echo root | sudo -u root
        # cmd = "echo motdepasse | sudo -S tcpdump -i eth0"

        cmd = "tshark -i eth0"
        # cmd = "while true; do echo 1;done"
        with Popen(cmd, shell=True,stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')  # process line here
                socketio.emit('newnumber', {'id': line}, namespace='/test')
                # sleep(1)
                if thread_stop_event.is_set():
                    return 0

        if p.returncode != 0:
            raise CalledProcessError(p.returncode, p.args)

        # sleep(3)
        # ps aux | grep -i 'insertTest.py'
        # strace -p11342 -s9999 -e write

        # socketio.emit('newnumber', {'id':data[0][0]}, namespace='/test')
        # socketio.sleep(0.3)
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

### Prvisous test
# import time 
# import subprocess
# import flask

# @app.route('/yield')
# def index_func():
#     def inner():
#         proc = subprocess.Popen(
#             # call something with a lot of output so we can see it
#             ['tshark -i eth0'],
#             shell=True,
#             stdout=subprocess.PIPE,
#             universal_newlines=True
#         )

#         for line in iter(proc.stdout.readline, ''):
#             # Don't need this just shows the text streaming
#             # time.sleep(1)
#             yield line.rstrip() + '<br/>\n'

#     # text/html is required for most browsers to show th$
#     return flask.Response(inner(), mimetype='text/html')

if __name__ == "__main__":
    # app.run(host=config.hostConfig, debug=config.debugMode)
    socketio.run(app, host=config.hostConfig, debug=config.debugMode)
