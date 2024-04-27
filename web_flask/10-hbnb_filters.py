#!/usr/bin/python3
"""Starts a flask app."""
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models import storage


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes = False)
def hbnb_filters():
    """Display a html page from deploy static."""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)

@app.teardown_appcontext
def close(exception=None):
    """close the db session when the app context is being popped at the end of
    the current request."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
