from quart import Quart, g
from quart_schema import QuartSchema
import sqlite3  # currently unused, but would like to...

app = Quart(__name__)

QuartSchema(app)

from toolauth import views

def run() -> None:
    # big flaskbacks to https://github.com/miguelgrinberg/microblog
    # tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    app.run(host="0.0.0.0", port=8081) #corey needs this in 8080 on WSL2
