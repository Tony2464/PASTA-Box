from flask import session, redirect
from functools import wraps
from flask.helpers import url_for

def web_connection_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not session.get('id') :
            return redirect(url_for('web_connection.login'))
        return func(*args, **kwargs)
    # Continue
    return decorated
