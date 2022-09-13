from toolauth import app
from toolauth.services.readtotool import reader_to_listed_tools
from toolauth.services.authorized import authreq
from toolauth.services.esphome_api import other_picked
from toolauth.models import AuthReqIn, SessionIn

from quart import Quart, request, jsonify, abort, g
from quart_schema import QuartSchema, validate_request, validate_response

import sqlite3  # currently unused, but would like to...
from uuid import uuid4
from threading import Thread
import sys

# ---------------------------------------------------------------------------------------------------


@app.get("/")
async def main():
    return """
    <h1>toolauth</h1>
    <p>Thanks for using this new Tool Authorization system. Instructions will be here one day.</p>
    <p>rules: <a href="http://192.168.1.170:5000/docs">http://192.168.1.170:8081/docs</a></p>
    """


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
            session_uid = (
                12  # uuid4().int  # would be great if a database generated these
            )

            await reader_to_listed_tools(
                device_name,
                card_uid,
                member_name,
                member_uid,
                reader_name,
                reader_uid,
                session_uid,
            )

            return "Hello Auth"
    except Exception as e:
        print(e, file=sys.stderr)
        return abort(500, e)


@app.post("/otherpicked")  # server testing only
async def otherpicked():  # server testing only
    d = await request.json  # server testing only
    device_name = d["device_name"]  # server testing only
    await other_picked(device_name)  # server testing only
    return "other was picked"  # server testing only


# needs much more definition for the long-term loggging
@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    return "Hello Session"
