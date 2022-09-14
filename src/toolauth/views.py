import sys
from typing import Dict

from quart import abort
from quart import request
from quart_schema import validate_request

from toolauth import app
from toolauth.models import AuthReqIn
from toolauth.models import SessionIn
from toolauth.services.authorized import authreq
from toolauth.services.esphome_api import other_picked
from toolauth.services.readtotool import reader_to_listed_tools


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

    if not res:
        return

    try:
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


@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    """
    Needs much more definition to be useful for long-term logging.
    """
    print(data)
    pass
