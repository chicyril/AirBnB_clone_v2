#!/usr/bin/python3
"""Start a flack web app listening on 0.0.0.0:5000"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def list_states():
    """Lists the states in the database."""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def rem_session(exception=None):
    """Remove the session after request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
