import sys
from typing import Dict
from quart import abort, request
from quart_schema import validate_request
from threading import Thread
from toolauth import app
from toolauth.models import AuthReqIn, SessionIn
from toolauth.services.authorized import authreq
from toolauth.services.esphome_api import other_picked
from toolauth.services.readtotool import threaded_tool


@app.get("/")
async def main() -> str:
    return """
    <h1>toolauth</h1>
    <p>Thanks for using this new Tool Authorization system. Instructions will be here one day.</p>
    <p>rules: <a href="http://192.168.1.170:5000/docs">http://192.168.1.170:8081/docs</a></p>
    """


@app.post("/authreq")
@validate_request(AuthReqIn)
async def authorization_request(data: AuthReqIn) -> str:
    res = await authreq(data)

    if res:
        try:
            startDevice = Thread(
                target=threaded_tool,
                args=(
                    data.device_name,
                    data.card_uid,
                    "Homer Simpson",
                    res,
                    data.reader_name,
                    data.reader_uid,
                    12,
                ),
            )

            startDevice.start()

            return "Hello Auth"
        except Exception as e:
            print(e, file=sys.stderr)
            return abort(500, e)

    abort(403)


@app.post("/otherpicked")
async def otherpicked() -> str:
    """For server testing only"""
    d: Dict[str, str] = await request.json
    device_name = d["device_name"]
    await other_picked(device_name)
    return "other was picked"


@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn) -> None:
    """
    Needs much more definition to be useful for long-term logging.
    """
    print(data)
    pass
