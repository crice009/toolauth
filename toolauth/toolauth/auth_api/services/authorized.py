from quart import abort
from ..data import *
import toolauth
from .readtotool import get_tools_for_a_reader
from .getters_setters import (
    get_reader_name,
    set_session_number,
    get_tool_is_busy,
)
import urllib.request, json
import os, logging


# ===============================================================================
# ===============================================================================
# ===============================================================================

# find all the tools that should be enabled by a card swipe, ask if they are authorized
async def db_authreq(reader_id, card_id):
    # collect & format all the needed data to ask about authorization
    # reader_id = data.get("reader_id").strip()
    # card_id = data.get("card_uid", "").replace("-", "").lower()

    # start to prepare for building a response
    req_res = ReqResDB(member_id=0, session_id=0, authorized_tools=[])

    # get the list of tools the card reader may unlock
    tools = await get_tools_for_a_reader(reader_id)

    # check the entire list of tools to see if any are authorized
    for tool in tools:
        print("db_authreq | checking on tool: " + str(tool["id"]))
        # ask Drupal if each tool is allowed
        res = await new_ask_drupal(tool, card_id)

        if res:
            req_res.member_id = res  # <= may set this redundatly...
            # guard clause | check to see if the tool is in use
            if get_tool_is_busy(tool["id"]):
                continue  # pass this tool
            # all is good: append to the list of authorized tools
            req_res.authorized_tools.append(tool["id"])

    print("authorized tools, known to not be busy:" + str(req_res.authorized_tools))

    # guard clause | if there is not one authorized tool in list, send 403
    if len(req_res.authorized_tools) == 0:
        abort(
            403,  # forbidden HTTP message
            "Member NOT Authorized for any available tools from reader: "
            + get_reader_name(reader_id),
        )

    # initalize a session_core
    req_res.session_id = set_session_number(card_id, req_res.member_id, reader_id)

    # return a response to calling function
    return req_res  # always returns if any tool can work


# ===============================================================================

# ask Drupal if member is authorized, report back either way
async def new_ask_drupal(tool, card_id):
    # drupal6 is the current card system, so work with that
    # https://www.makehaven.org/api/v0/serial/04376A6A5F5780/permission/door
    # https://www.makehaven.org/api/v0/serial/<card_uid>/permission/<badge_name>

    # only for testing
    if tool["drupal_name"] == "servertest":
        drupal_tool_name = "door"
    else:
        drupal_tool_name = tool["drupal_name"]

    url = (
        "https://www.makehaven.org/api/v0/serial/"
        + card_id
        + "/permission/"
        + drupal_tool_name
    )

    print("checking this URL: " + url)

    response = urllib.request.urlopen(url)
    data = response.read()
    drupal_response = json.loads(data)

    # expecting: [{"permission":"Door","access":"true","uid":"2"}] #and 'uid' is the member id number
    # expecting: returns [] from drupal if not authorized
    if len(drupal_response) >= 1:  # =============== member is approved for this tool
        member_uid = int(drupal_response[0]["uid"])  # given the response structure
        return member_uid
    else:  # ======================================= member is NOT approved for this tool
        return  # nothing
