from quart import render_template
from toolauth.crud import bp

# CRUD operations:
# -------Create
# -------Read
# -------Update
# -------Delete

# #---------------------- Configuration between ESPHome devices -----------------------------
# @bp.get("/config/update")
# async def update_config():
#     # check this out: https://github.com/pawansingh126/yaml_editor
#     return "This will let you edit the YAML in the browser, one day"


# #---------------------- ESPHome Things: Readers, tools, vacuums ---------------------------
# @bp.get("/esphomething/create")
# async def create_esphomething():
#     # could be as simple as a form where you write in a name
#     # and the server handles starting a UUID(filename + hostname) and the needed YAML file
#     return "This will let you store some UUID address in the database, one day"

# #---------------------- Badges tied to ESPHome tools --------------------------------------
# @bp.get("/badge/create")
# async def create_badge():
#     # probably need a dedicated cardreader and ?websockets to make this easy
#     return "This will define a new badge, possibly automatically after adding ESPhome tools"

# #---------------------- Members & RFID Cards ----------------------------------------------
# @bp.get("/membercard/create")
# async def create_membercard():
#     # probably from some web-based interface
#     return "This will create a new member (who will very soon need a card)"


# @bp.get("/membercard/update")
# async def update_membercard():
#     # probably need a dedicated cardreader and ?websockets on a web interface to make this easy
#     return "This will assign a new card to the member"

# #---------------------- Badges for Each Member --------------------------------------------

# @bp.get("/memberbadge/create")
# async def create_memberbadge():
#     # probably need an api call to make this from a quiz result
#     return "This will create a badge for a specific member, maybe after a quiz."


# @bp.get("/memberbadge/update")
# async def update_memberbadge():
#     # probably need a web interface to let facilitators update these
#     return "This will allow facilitators to upgrade/downgrade badges manually."
