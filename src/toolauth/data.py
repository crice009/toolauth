from dataclasses import dataclass


@dataclass
class AuthReqIn:  # ------ESP32 sends these right after a card read
    device_name: str  # text-based name for tool intended to use
    device_uid: str  # some kind of ID number for tool intended
    reader_name: str  # text-based name for card reader
    reader_uid: str  # some kind of ID number for card reader
    card_uid: str  # the card_uid of member asking for permission


@dataclass
class SessionInit:  # ------Server sends this response to initalize a device session
    member_uid: int  # a number to keep track of members || easier data search
    member_name: str  # their name for possible display on screens, stickers, etc. || easier data search
    card_uid: str  # the actual number straight from their card, possibly without "-" || easier data search
    session_uid: int  # a number to keep track of individual card/tool use sessions || easier data search


@dataclass
class SessionIn:  # ------ESP32 sends these to begin or end a session on tool/device
    member_uid: int  # a number to keep track of members || easier data search
    member_name: str  # their name for possible display on screens, stickers, etc. || easier data search
    card_uid: str  # the actual number straight from their card, possibly without "-" || easier data search
    session_uid: int  # a number to keep track of individual card/tool use sessions || easier data search
    active_session: bool  # the state of the tool session ~ might change this to 'session'
    action: str  # the reason this message is being sent (could be coded to int)
    device_uid: str  # a number to keep track of the devices || easier data search
    device_name: str  # the name of the tool || easier data search

    def get(self, key):
        return self.get(key)
