# src/toolauth/api/auth/__init__.py
from quart import Blueprint
from quart import current_app as app

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
