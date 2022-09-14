from toolauth import app
from toolauth.services.readtotool import reader_to_listed_tools
from toolauth.services.authorized import authreq
from toolauth.services.esphome_api import other_picked
from toolauth.models import AuthReqIn, SessionIn
from quart import request, abort
from quart_schema import validate_request
from typing import Dict
import sys


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
    res = await authreq(data)

    try:
        if res:
            await reader_to_listed_tools(
                device_name=data.device_name.strip(),
                card_uid=data.card_uid.replace("-", "").lower(),
                member_name="Homer Simpson",
                member_uid=res,
                reader_name=data.reader_name.strip(),
                reader_uid=data.reader_uid.strip(),
                session_uid=12,
            )

            return "Hello Auth"
    except Exception as e:
        print(e, file=sys.stderr)
        return abort(500, e)


@app.post("/otherpicked")
async def otherpicked():
    """For server testing only"""
    d: Dict[str, str] = await request.json
    device_name = d["device_name"]
    await other_picked(device_name)
    return "other was picked"


# needs much more definition for the long-term loggging
@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    return "Hello Session"
