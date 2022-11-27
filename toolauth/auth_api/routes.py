from .services.readtotool import threaded_tool, reader_to_listed_tools
from .services.authorized import authreq
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


@auth_api.post("/authreq")
@validate_request(AuthReqIn)
async def authorization_request(data: AuthReqIn):
    print(data)
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

            # startDevice = Thread(
            #     target=threaded_tool,
            #     args=(
            #         device_name,
            #         card_uid,
            #         member_name,
            #         member_uid,
            #         reader_name,
            #         reader_uid,
            #         session_uid,
            #     ),
            # )

            # startDevice.start()
            asyncio.ensure_future(
                reader_to_listed_tools(
                    device_name,
                    card_uid,
                    member_name,
                    member_uid,
                    reader_name,
                    reader_uid,
                    session_uid,
                )
            )
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
@auth_api.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    # should add logic here to check if we need to run 'other_picked'
    # that would involve reading the YAML file that pairs readers with devices,
    # to see if any need shut-off with other_picked - then sending those messages.
    return "Hello Session"
