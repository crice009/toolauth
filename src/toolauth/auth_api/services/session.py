from .getters_setters import (
    get_tool_from_base,
    get_session_reader,
    get_tool_is_busy,
    get_reader_name,
    get_member_name,
    get_tool_name,
)
from .readtotool import get_tools_for_a_reader
from datetime import datetime
import toolauth

# find all the tools that should be enabled by a card swipe, ask if they are authorized
async def manage_other_picked(data):
    # collect actionable info from the session_event
    session_id = int(data.get("session_id"))
    device_uid = data.get("device_id")
    tool_id = get_tool_from_base(device_uid)

    reader_id = get_session_reader(session_id)

    unpicked_tools = []
    tools = await get_tools_for_a_reader(reader_id)

    for tool in tools:
        # guard clause | pass for the tool that was selected
        if tool["tool_id"] == tool_id:
            continue
        # guard clause | pass for any previously busy tools
        if get_tool_is_busy(tool["tool_id"]):
            continue
        # send out the other_picked message


def set_session_number(card_id, member_id, reader_id):
    # make a new entry in the DB
    reader_name = get_reader_name(reader_id)
    member_name = get_member_name(member_id)
    db = toolauth._get_db()
    db.execute(
        """INSERT INTO session_core 
                (card_id,
                member_id, 
                member_name,   
                reader_id, 
                reader_name, 
                created_at) 
            VALUES (?, ?, ?, ?, ?, ?);""",
        [card_id, member_id, member_name, reader_id, reader_name, str(datetime.now())],
    )
    db.commit()
    # get the 'id' of this new session
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id
             FROM session_core
         ORDER BY id DESC;""",
    )
    session_id = cur.fetchone()["id"]  # session_id
    return session_id


# adjust entry in session_core to include the tool
# this happens after the member presses the green button (to accomodate one-to-many reader/tools)
def set_session_tool(session_id, tool_id):
    tool_name = get_tool_name(tool_id)
    db = toolauth._get_db()
    db.execute(
        """UPDATE session_core
              SET tool_id = (?), tool_name = (?)
            WHERE id=(?);""",
        [tool_id, tool_name, session_id],
    )
    db.commit()


def set_session_event(data):
    # make a new entry in the DB
    session_id = int(data.get("session_id"))
    active_session = data.get("active_session")
    print(type(active_session))
    if active_session is "1":
        print("active_session evaluates to True")
        active_session = 1
    else:
        print("active_session evaluates to False")
        active_session = 0
    action = data.get("action")
    device_uid = data.get("device_id")

    db = toolauth._get_db()
    db.execute(
        """INSERT INTO session_event 
                (session_id 
                action,   
                active_session, 
                created_at) 
            VALUES (?, ?, ?, ?);""",
        [
            session_id,
            action,
            active_session,
            str(datetime.now()),
        ],
    )
    db.commit()
    return
