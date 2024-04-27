#!/usr/bin/python3
"""
Starts a Flask web application.
"""
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Liste the cities in each state in alphabetical order"""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception=None):
    """close the db session when the app context is being popped at the end of
    the current request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0',)
