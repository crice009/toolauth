"""toolauth"""
from quart_schema import QuartSchema
from toolauth.auth_api.routes import auth_api
from toolauth.crud_gui.routes import crud_gui
from pathlib import Path
from sqlite3 import dbapi2 as sqlite3
from quart import g, Quart, render_template
import logging

# logging the main operations of the server
logging.basicConfig(
    filename="toolauth.log",
    level=logging.DEBUG,
    format="%(asctime)-15s %(message)s",
)

app = Quart(__name__)
# quart-schema auto-populates the '/docs' for the server (very convenient)
QuartSchema(app)

# register the two blueprints for the server, to keep the two main functions organized
app.register_blueprint(auth_api)
app.register_blueprint(crud_gui)

# this route is probably not needed, but is a good sanity-check for the server working at all...
@app.route("/")
async def hello():
    return await render_template("index.html")


app.config.update(
    {
        "DATABASE": app.root_path / "db/toolauth.db",
    }
)


def _connect_db():
    engine = sqlite3.connect(app.config["DATABASE"])
    engine.row_factory = sqlite3.Row
    return engine


def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db


def init_db():
    db = _connect_db()
    with open(app.root_path / "db/sql/schema.sql", mode="r") as file_:
        db.cursor().executescript(file_.read())
    db.commit()


def run() -> None:
    app.run()
