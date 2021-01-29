import sys
from flask import Flask
from flask.templating import render_template

# Local
from __main__ import app  # For route
import main  # For dBmanager

dbManager = main.dbManager


@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('pages/index.html', content=name)
