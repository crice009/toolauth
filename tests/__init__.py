from toolauth import app, TodoIn

async def test_authreq() -> None:
    test_client = app.test_client()
    response = await test_client.post("/authreq", json=AuthReqIn(
            device_name="str", #text-based name for tool intended to use 
            device_uid="str",  #some kind of ID number for tool intended
            reader_name="str", #text-based name for card reader
            reader_uid="str",  #some kind of ID number for card reader
            card_uid="str",    #the card_uid of member asking for permission
    ))
    data = await response
    assert data is not None

async def test_create_todo() -> None:
    test_client = app.test_client()
    response = await test_client.post("/session", json=SessionIn(
            member_uid=5,        #a number to keep track of members || easier data search
            member_name="str",   #their name for possible display on screens, stickers, etc. || easier data search
            card_uid= "str",     #the actual number straight from their card, possibly without "-" || easier data search
            session_uid= 10,     #a number to keep track of individual card/tool use sessions || easier data search
            active_session=True, #the state of the tool session ~ might change this to 'session'
            action="str",        #the reason this message is being sent (could be coded to int)
            device_uid="str",    #a number to keep track of the devices || easier data search
            device_name="str"    #the name of the tool || easier data search
        ))
    data = await response
    assert data is not None