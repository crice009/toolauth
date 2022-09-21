from toolauth import app
from toolauth.services.readtotool import threaded_tool, threaded_other_tool
from toolauth.services.authorized import authreq
from toolauth.data import AuthReqIn, SessionIn, _connect_db

from quart import Quart, request, jsonify, abort, g
from quart_schema import QuartSchema, validate_request, validate_response

from uuid import uuid4
from threading import Thread
from datetime import datetime
import sys


def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db


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
            session_uid = uuid4().int

            startDevice = Thread(
                target=threaded_tool,
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
    db = _get_db()
    db.execute(  # always save the session data
        """ INSERT INTO session_entry (
            session_uid,
            entry_time,
            member_uid,
            member_name,
            card_uid,
            active_session,
            action_description,
            device_uid,
            device_name
            ) VALUES (?, ?)
        """,
        [
            data.get("session_uid"),
            datetime.utcnow(),
            data.get("member_uid"),
            data.get("member_name"),
            data.get("card_uid"),
            data.get("active_session"),
            data.get("action"),
            0,  # device_uid stand-in value...
            data.get("device_name"),
        ],
    )
    db.commit()

    if data.get("action") == "session start":

        other_picked = Thread(
            target=threaded_other_tool, args=(data.get("device_name"))
        )
        other_picked.start()
        return "other_picked was activated"
    else:
        return "Hello Session"
