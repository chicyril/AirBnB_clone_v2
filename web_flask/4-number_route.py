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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def is_cool(text='is cool'):
    """Return Python and the value of the text variable or is cool by default
    replacing any '_' with ' '.
    """
    return f'Python {escape(text.replace("_", " "))}'


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Display `the value of n` is a number only if n is an integer."""
    return f'{n} is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
