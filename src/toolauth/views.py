from toolauth.services.readtotool import reader_to_listed_tools
from toolauth.services.authorized import authreq
from toolauth.services.esphome_api import find_the_keys
from dataclasses import dataclass

from quart import Quart, request, jsonify, abort, g, render_template
from quart_schema import QuartSchema, validate_request, validate_response
from toolauth import app
import sqlite3  # currently unused, but would like to...
import sys



@dataclass
class AuthReqIn:  # ------ESP32 sends these right after a card read
    device_name: str  # text-based name for tool intended to use
    device_uid: str  # some kind of ID number for tool intended
    reader_name: str  # text-based name for card reader
    reader_uid: str  # some kind of ID number for card reader
    card_uid: str  # the card_uid of member asking for permission


@dataclass
class SessionInit:  # ------Server sends this response to initalize a device session
    member_uid: int  # a number to keep track of members || easier data search
    # their name for possible display on screens, stickers, etc. || easier data search
    member_name: str
    card_uid: str  # the actual number straight from their card, possibly without "-" || easier data search
    # a number to keep track of individual card/tool use sessions || easier data search
    session_uid: int


@dataclass
class SessionIn:  # ------ESP32 sends these to begin or end a session on tool/device
    member_uid:  int  # a number to keep track of members || easier data search
    # their name for possible display on screens, stickers, etc. || easier data search
    member_name: str
    card_uid: str     # the actual number straight from their card, possibly without "-" || easier data search
    # a number to keep track of individual card/tool use sessions || easier data search
    session_uid: int
    active_session: bool  # the state of the tool session ~ might change this to 'session'
    # the reason this message is being sent (could be coded to int)
    action: str
    device_uid: str   # a number to keep track of the devices || easier data search
    device_name: str  # the name of the tool || easier data search


# ---------------------------------------------------------------------------------------------------
# -------------------------------------------------
# DATABASE = 'test.db'

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
# -------------------------------------------------
# ---------------------------------------------------------------------------------------------------


@app.get("/")
async def main():
    return "Thanks for using this new Tool Authorization system. Instructions will be here one day. <br> rules: http://localhost:5000/docs#/ <br> You can also look for you device keys this way: http://localhost:5000/findkeys/(device_name)"


@app.get("/config")
async def config():
    # check this out: https://github.com/pawansingh126/yaml_editor
    return "This will let you edit the YAML in the browser, one day"

@app.get("/new/esphome")
async def new_esphome():
    # could be as simple as a form where you type in the MAC address and reader_name
    return "This will let you store the MAC address in the database, one day"


@app.get("/new/membercard")
async def new_membercard():
    # probably need a dedicated cardreader and ?websockets to make this easy
    return "This will assign a new card to the member, one day"


@app.route("/findkeys/<string:dname>", methods=["GET", "POST"])
async def foundkeys(dname):
    try:
        list = await find_the_keys(dname)
        # check this out: https://github.com/pawansingh126/yaml_editor
        return await render_template("find_keys.html", services=list)
    except Exception as e:
        print(e, file=sys.stderr)
        return abort(500, "Could not connect to ESPHome device. Check network and spelling in your URL.")


@app.post("/authreq")
@validate_request(AuthReqIn)
async def authorization_request(data: AuthReqIn):
    data = await request.json
    res = await authreq(data)

    try:
        if res:
            device_name = data.get("device_name").strip()
            card_uid = data.get("card_uid", "").replace("-", "").lower()
            member_name = "Homer Simpson"
            member_uid = res  # only sends back the member uid as of now
            # text-based name for card reader
            reader_name = data.get("reader_name").strip()
            # some kind of ID number for card reader
            reader_uid = data.get("reader_uid").strip()
            session_uid = 1  # would be great if a database generated these

            await reader_to_listed_tools(
                device_name,
                card_uid,
                member_name,
                member_uid,
                reader_name,
                reader_uid,
                session_uid)

            return "Hello Auth"
    except Exception as e:
        print(e, file=sys.stderr)
        return abort(500, "Could not connect to ESPHome device. Check network and config files.")
        # would be nice if we could report the good & bad esphome conenctions here


@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    return "Hello Session"
