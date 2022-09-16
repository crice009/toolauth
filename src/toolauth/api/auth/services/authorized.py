import json
import urllib.request
from quart import abort
from typing import Literal
from toolauth.api.auth.models import AuthReqIn


async def authreq(data: AuthReqIn) -> int | Literal[False]:
    """Initial handler used to handle a card read sent by the ESP32."""
    permission_details = await ask_drupal(
        device_name=data.device_name.strip(),
        card_uid=data.card_uid.replace("-", "").lower(),
    )

    return permission_details or False


async def ask_drupal(device_name: str, card_uid: str) -> int:
    # drupal6 is the current card system, so work with that
    # https://www.makehaven.org/api/v0/serial/04376A6A5F5780/permission/door
    # https://www.makehaven.org/api/v0/serial/<card_uid>/permission/<badge_name>
    if device_name == "servertest":
        device_name = "door"  # only for testing

    url = (
        "https://www.makehaven.org/api/v0/serial/"
        + card_uid
        + "/permission/"
        + device_name
    )

    response = urllib.request.urlopen(url)
    data = response.read()
    drupal_response = json.loads(data)
    # expecting: [{"permission":"Door","access":"true","uid":"2"}] #and 'uid' is the member id number
    if len(drupal_response) >= 1:  # returns [] from drupal if not authorized
        member_uid = int(drupal_response[0]["uid"])
        return member_uid
    else:
        abort(
            403, "Member not Authorized for use of " + device_name + " device."
        )  # forbidden HTTP message
