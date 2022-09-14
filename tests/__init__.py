"""Test suite for the toolauth package."""
from toolauth import app
from toolauth.models import *


async def test_authreq() -> None:
    test_client = app.test_client()
    response = await test_client.post(
        "/authreq",
        json=AuthReqIn(
            device_name="servertest",  # text-based name for tool intended to use
            device_uid="12345",  # some kind of ID number for tool intended
            reader_name="servertest",  # text-based name for card reader
            reader_uid="56789",  # some kind of ID number for card reader
            card_uid="04376A6A5F5780",  # the card_uid of member asking for permission
        ),
    )
    data = await response
    assert data is "Hello Auth"


async def test_session() -> None:
    test_client = app.test_client()
    response = await test_client.post(
        "/session",
        json=SessionIn(
            member_uid=5,  # a number to keep track of members || easier data search
            member_name="Corey",  # their name for possible display on screens, stickers, etc. || easier data search
            card_uid="04376A6A5F5780",  # the actual number straight from their card, possibly without "-" || easier data search
            session_uid=10,  # a number to keep track of individual card/tool use sessions || easier data search
            active_session=True,  # the state of the tool session ~ might change this to 'session'
            action="test",  # the reason this message is being sent (could be coded to int)
            device_uid="12345",  # a number to keep track of the devices || easier data search
            device_name="servertest",  # the name of the tool || easier data search
        ),
    )
    data = await response
    assert data is "Hello Session"
