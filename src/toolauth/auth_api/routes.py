from .services.esphome_api import threaded_tool_enable, tool_enable
from .services.authorized import db_authreq
from .services.session import manage_other_picked, set_session_event, set_session_tool
from .data import *
from quart_schema import validate_request
from threading import Thread
import sys, asyncio, logging, toolauth
from quart import Blueprint, render_template, g, request, abort

# define this blueprint (collection of web-routes)
auth_api = Blueprint(
    "auth_api",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/auth_api",
)


# main auth_api route
@auth_api.route("/")
async def index():
    logging.info("visited auth_api")
    return await render_template("auth_api.html")


# ---------------------------------------------------------------------------------------------------
@auth_api.get("/simple")
async def simple():
    return """
    <h1>toolauth</h1>
    <p>Thanks for using this new Tool Authorization system. Instructions will be here one day.</p>
    <p>Rules for each of the endpoints: <a href="/docs">auto-generated-docs</a></p>
    """


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== NEW! ====================================


@auth_api.post("/authreq")
@validate_request(AuthReqInDB)
async def authorization_request(data: AuthReqInDB):
    # get the data out of the JSON

    data = await request.json
    reader_id = data["reader_id"]
    card_id = data["card_id"]
    card_id = card_id.replace("-", "").lower()

    try:
        # ask Drupal if user has authorization
        req_res = await db_authreq(reader_id, card_id)
        # 'abort' will be thrown if no tools authorized

        for tool in req_res.authorized_tools:
            # put the tool in 'enable' mode
            await tool_enable(tool, req_res.session_id)
            # !!!!!!!!!!!!!!!!!!!!! ------ This is may be too slow for ESP32's...

        # return to send out a 200 HTTP code
        return "Hello Auth"
    except Exception as e:
        print(e, file=sys.stderr)
        logging.info(e)
        return abort(500, e)


# needs much more definition for the long-term loggging
@auth_api.post("/session_event")
@validate_request(SessionInDB)
async def session_event_handler(data: SessionInDB):
    # get the data out of the JSON
    data = await request.json

    print("session_event | data recieved: " + str(data))
    # collect & format all the needed data to ask about authorization
    set_session_event(data)

    # decode the action from the event
    action = data.get("action")

    # only if this starts a session
    if action == "session start":
        try:
            await set_session_tool(data)
            # send out other-picked messages
            await manage_other_picked(data)
        except Exception as e:
            print(e, file=sys.stderr)
            logging.info(e)
            return abort(500, e)

    # return to send out a 200 HTTP code
    return "Hello Session"
