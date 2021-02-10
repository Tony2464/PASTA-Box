import sys
from flask import Flask
from flask.templating import render_template

# Local
sys.path.append("../")
import main  # For dBmanager
from main import app  # For route

dbManager = main.dbManager


@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('pages/index.html', content=name)
