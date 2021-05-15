from flask import Flask, redirect
from flask.helpers import url_for
from flask.templating import render_template
from flask_socketio import SocketIO
from time import sleep
from threading import Thread, Event
from subprocess import Popen, PIPE

# Local imports
import web.conf.config as config
import database.db_config as config

# Import all routes
# API routes
from api.routes.frames import frames
from api.routes.rules import rules
from api.routes.devices import devices

# Web pages routes
from web.routes.admin.index import homepage, index
from web.routes.admin.web_frames import web_frames
from web.routes.admin.web_firewall import web_firewall
from web.routes.admin.web_mapping import web_mapping
from web.routes.admin.web_settings import web_settings
from web.routes.admin.web_audit import web_audit

app = Flask(__name__)
# API
app.register_blueprint(frames, url_prefix="/api/frames")
app.register_blueprint(rules, url_prefix="/api/rules")
app.register_blueprint(devices, url_prefix="/api/devices")

# Web Pages
app.register_blueprint(index, url_prefix="/admin")
app.register_blueprint(web_frames, url_prefix="/admin/frames")
app.register_blueprint(web_firewall, url_prefix="/admin/firewall")
app.register_blueprint(web_mapping, url_prefix="/admin/map")
app.register_blueprint(web_settings, url_prefix="/admin/settings")
app.register_blueprint(web_audit, url_prefix="/admin/audit")


@app.route('/')
def home():
    return redirect("/admin", code=301)

# Web Scocket for Live frames


# turn the flask app into a socketio app
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

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(sendFrames)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    thread_stop_event.set()


# 404 web page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


if __name__ == "__main__":
    # app.run(host=config.hostConfig, debug=config.debugMode)
    socketio.run(app, host=config.hostConfig, debug=config.debugMode)
