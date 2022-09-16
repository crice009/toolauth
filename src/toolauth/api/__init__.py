# src/toolauth/api/__init__.py
"""Toolauth API"""
from quart import Quart
from quart_schema import QuartSchema


def create_app() -> Quart:
    """Main entrypoint for the Quart app/API"""
    app = Quart(__name__)
    QuartSchema(app)

    from .auth import views, auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app


def run() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=8081)
