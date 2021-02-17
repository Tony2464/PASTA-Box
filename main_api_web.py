from flask import Flask
from flask.templating import render_template

# Local imports
import web.conf.config as config

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
    return render_template("frames.html")


if __name__ == "__main__":
    app.run(host=config.hostConfig, debug=config.debugMode)
