from flask import Flask
from flask.templating import render_template

# Local imports
import web.conf.config as config

# Import all routes
from api.routes.frames import frames

app = Flask(__name__)
app.register_blueprint(frames, url_prefix="/api/frames")

@app.route('/')
def home():
    return "Homepage"

if __name__ == "__main__":
    app.run(host=config.hostConfig, debug=config.debugMode)
