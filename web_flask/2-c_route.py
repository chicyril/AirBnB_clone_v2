#!/usr/bin/python3
"""Start a flask web application."""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """Return Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def is_fun(text):
    """Return C and the value of the text variable replacing '_' with ' '."""
    return f'C {escape(text.replace("_", " "))}'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
