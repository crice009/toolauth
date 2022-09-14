# src/toolauth/__init__.py
"""Toolauth."""
import sqlite3  # currently unused, but would like to...

from quart import Quart
from quart import g
from quart_schema import QuartSchema


app = Quart(__name__)

QuartSchema(app)


def run() -> None:
    # big flaskbacks to https://github.com/miguelgrinberg/microblog
    # tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    from toolauth import views

    app.run(host="0.0.0.0", port=8081)  # corey needs this in 8080 on WSL2
