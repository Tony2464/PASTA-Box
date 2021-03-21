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
    return "Index page"

### Web Scocket for Live frames


#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


def sendFrames():
    print("Sending frames")
    # Loop unless disconnection
    cmd = "tshark -i br0"
    with Popen(cmd, shell=True, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')  # process line here
            socketio.emit('newnumber', {'id': line}, namespace='/test')
            socketio.sleep(0.04)
            if thread_stop_event.is_set():
                return 0


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

### Web Scocket for Live frames END


if __name__ == "__main__":
    # app.run(host=config.hostConfig, debug=config.debugMode)
    socketio.run(app, host=config.hostConfig, debug=config.debugMode)
