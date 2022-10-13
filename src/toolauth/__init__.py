from quart import Quart, g
from quart_schema import QuartSchema
from pathlib import Path
from sqlite3 import dbapi2 as sqlite3
import os, sys

app = Quart(__name__)

app.config.update(
    {
        "DATABASE": app.root_path / "toolauth.db",
    }
)

QuartSchema(app)


def run() -> None:
    # big flaskbacks to https://github.com/miguelgrinberg/microblog
    # tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    from toolauth.crud import bp as crud_bp

    app.register_blueprint(crud_bp)

    app.run(host="0.0.0.0", port=8081)  # corey needs this in 8080 on WSL2


def _connect_db():
    engine = sqlite3.connect(app.config["DATABASE"])
    engine.row_factory = sqlite3.Row
    return engine


def init_db():
    db = _connect_db()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "schema.sql")

    with open(path, mode="r") as file_:
        # print("madeit", file=sys.stdout)
        db.cursor().executescript(file_.read())
    db.commit()
