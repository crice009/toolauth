from dataclasses import dataclass


@dataclass
class AuthReqIn:
    """
    Request payload sent by ESP32 after a card read.

    Attributes:
        device_name: text-based name for tool intended to use
        device_uid: some kind of ID number for tool intended
        reader_name: text-based name for card reader
        reader_uid: some kind of ID number for card reader
        card_uid: the card_uid of member asking for permission
    """

    device_name: str
    device_uid: str
    reader_name: str
    reader_uid: str
    card_uid: str


@dataclass
class SessionInit:
    """
    Sent by server to ESP32 to initialize a device session.

    Attributes:
        member_uid: a number to keep track of members || easier data search
        member_name: their name for possible display on screens, stickers, etc. || easier data search
        card_uid: the actual number straight from their card, possibly without "-" || easier data search
        session_uid: a number to keep track of individual card/tool use sessions || easier data search

    """

    member_uid: int
    member_name: str
    card_uid: str
    session_uid: int


@dataclass
class SessionIn:
    """
    Sent by ESP32 to begin or end a session on tool/device.

    Attributes:
        member_uid: a number to keep track of members || easier data search
        member_name: their name for possible display on screens, stickers, etc. || easier data search
        card_uid: the actual number straight from their card, possibly without "-" || easier data search
        session_uid: a number to keep track of individual card/tool use sessions || easier data search
        active_session: the state of the tool session ~ might change this to 'session'
        action: the reason this message is being sent (could be coded to int)
        device_uid: a number to keep track of the devices || easier data search
        device_name: the name of the tool || easier data search
    """

    member_uid: int
    member_name: str
    card_uid: str
    session_uid: int
    active_session: bool
    action: str
    device_uid: str
    device_name: str
