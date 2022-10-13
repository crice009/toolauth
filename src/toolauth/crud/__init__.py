from quart import Blueprint

bp = Blueprint("crud", __name__)

from toolauth.crud import views

# CRUD operations:
# -------Create
# -------Read
# -------Update
# -------Delete
