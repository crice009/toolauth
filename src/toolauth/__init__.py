from dataclasses import dataclass
from datetime import datetime

from quart import Quart, request, jsonify, abort, g
from quart_schema import QuartSchema, validate_request, validate_response
import sqlite3
import sys

DATABASE = 'test.db'

app = Quart(__name__)

QuartSchema(app)

def run() -> None:
    app.run()

#-------------------------------------------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#-------------------------------------------------

@dataclass
class AuthReqIn: #------ESP32 sends these right after a card read
    device_name: str #text-based name for tool intended to use 
    device_uid: str  #some kind of ID number for tool intended
    reader_name: str #text-based name for card reader
    reader_uid: str  #some kind of ID number for card reader
    card_uid: str    #the card_uid of member asking for permission

@dataclass
class SessionInit: #------Server sends this response to initalize a device session
    member_uid: int   #a number to keep track of members || easier data search
    member_name: str  #their name for possible display on screens, stickers, etc. || easier data search
    card_uid: str     #the actual number straight from their card, possibly without "-" || easier data search
    session_uid: int  #a number to keep track of individual card/tool use sessions || easier data search

@dataclass
class SessionIn: #------ESP32 sends these to begin or end a session on tool/device
    member_uid:  int      #a number to keep track of members || easier data search
    member_name: str      #their name for possible display on screens, stickers, etc. || easier data search
    card_uid: str         #the actual number straight from their card, possibly without "-" || easier data search
    session_uid: int      #a number to keep track of individual card/tool use sessions || easier data search
    active_session: bool  #the state of the tool session ~ might change this to 'session'
    action: str           #the reason this message is being sent (could be coded to int)
    device_uid: str       #a number to keep track of the devices || easier data search
    device_name: str      #the name of the tool || easier data search

#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------

@app.get("/")
async def main():
    return "Thanks for using this new Tool Authorization system. Instructions will be here one day. rules: http://localhost:5000/docs#/"

@app.get("/config")
async def config():
    # check this out: https://github.com/pawansingh126/yaml_editor
    return "This will let you edit the YAML in the browser, one day"

@app.get("/new/esphome")
async def new_esphome():
    #could be as simple as a form where you type in the MAC address and reader_name
    return "This will let you store the MAC address in the database, one day"

@app.get("/new/membercard")
async def new_membercard():
    #probably need a dedicated cardreader and ?websockets to make this easy
    return "This will assign a new card to the member, one day"


from toolauth.services.authorized import authreq
from toolauth.services.readtotool import reader_to_listed_tools

@app.post("/authreq")
@validate_request(AuthReqIn)
async def authorization_request(data: AuthReqIn):
    data = await request.json
    res = await authreq(data)

    try:
        if res:
            device_name = data.get("device_name").strip()
            card_uid = data.get("card_uid", "").replace("-", "").lower()
            member_name = "Homer Simpson"
            member_uid = res #only sends back the member uid as of now
            reader_name=data.get("reader_name").strip() #text-based name for card reader
            reader_uid=data.get("reader_uid").strip()   #some kind of ID number for card reader
            session_uid = 1 #would be great if a database generated these

            await reader_to_listed_tools(
                device_name, 
                card_uid, 
                member_name, 
                member_uid, 
                reader_name, 
                reader_uid, 
                session_uid)
        
            return "Hello Auth" 
        else:
            return abort(403, "Member not Authorized for use of this device.") #forbidden HTTP message
    except Exception as e: 
        return abort(500, "Could not connect to ESPHome device. Check network and config files.") 
        #would be nice if we could report the good & bad esphome conenctions here
        
    
@app.post("/session")
@validate_request(SessionIn)
async def session_handler(data: SessionIn):
    return "Hello Session"