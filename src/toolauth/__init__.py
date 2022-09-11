from quart import Quart, g
from quart_schema import QuartSchema
import sqlite3 #currently unused, but would like to...

app = Quart(__name__)

QuartSchema(app)

from toolauth import views

def run(host='0.0.0.0') -> None:
    app.run()
