#!/usr/bin/python3
"""
Starts a Flask web application
"""
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays a html page with states"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, id='all')


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays a html page with cities of a state."""
    state = storage.all(State).get(f'State.{id}')
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def close(exception=None):
    """close the db session when the app context is being popped at the end of
    the current request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
