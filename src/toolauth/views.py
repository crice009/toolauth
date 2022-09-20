from toolauth import app
from toolauth.services.readtotool import reader_to_listed_tools, trigger_device_after_response
from toolauth.services.authorized import is_member_authorized
from toolauth.services.esphome_api import other_picked
from toolauth.data import *

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
    <p>Rules for each of the endpoints: <a href="/docs">auto-generated-docs</a></p>
    """


@app.post("/authreq")
@validate_request(AuthReqIn)
async def authorization_request(data: AuthReqIn):
    data = await request.json
    # log card-read in database: reader, possible tools, time, |member

    # reader &make session_uid > list_of_devices > *device > *authorized > *aioesphome_api &send Session

    # res = await is_member_authorized(data)

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

            startDevice = Thread(
                target=trigger_device_after_response,
                args=(
                    device_name,
                    card_uid,
                    member_name,
                    member_uid,
                    reader_name,
                    reader_uid,
                    session_uid,
                ),
            )

            startDevice.start()
            # await reader_to_listed_tools(
            #     device_name,
            #     card_uid,
            #     member_name,
            #     member_uid,
            #     reader_name,
            #     reader_uid,
            #     session_uid,
            # )

            return "Hello Auth"
    except Exception as e:
        print(e, file=sys.stderr)
        return abort(500, e)


# needs much more definition for the long-term loggging
@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    data = await request.json
    if data.action == "session start":
        # 
    # should add logic here to check if we need to run 'other_picked'
    # that would involve reading the YAML file that pairs readers with devices,
    # to see if any need shut-off with other_picked - then sending those messages.
    return "Hello Session"
