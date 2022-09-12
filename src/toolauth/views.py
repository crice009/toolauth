from toolauth.services.readtotool import reader_to_listed_tools
from toolauth.services.authorized import authreq
from toolauth.data import *

from quart import Quart, request, jsonify, abort, g
from quart_schema import QuartSchema, validate_request, validate_response
from toolauth import app
import sqlite3  # currently unused, but would like to...
import sys

# ---------------------------------------------------------------------------------------------------

@app.get("/")
async def main():
    return '''
    <h1>toolauth</h1>
    <p>Thanks for using this new Tool Authorization system. Instructions will be here one day.</p>
    <p>rules: <a href="http://localhost:8081/docs">http://localhost:8081/docs</a></p>
    '''


@app.get("/config")
async def config():
    # check this out: https://github.com/pawansingh126/yaml_editor
    return "This will let you edit the YAML in the browser, one day"

@app.get("/new/esphome")
async def new_esphome():
    # could be as simple as a form where you write in a name
    # and the server handles starting a UUID(filename + hostname) and the needed YAML file
    return "This will let you store some UUID address in the database, one day"


@app.get("/new/membercard")
async def new_membercard():
    # probably need a dedicated cardreader and ?websockets to make this easy
    return "This will assign a new card to the member, one day"


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
        return e #abort(500, "Could not connect to ESPHome device. Check network and config files.")
        # would be nice if we could report the good & bad esphome conenctions here


@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    return "Hello Session"
