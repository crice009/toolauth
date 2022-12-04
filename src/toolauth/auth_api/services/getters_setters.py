from datetime import datetime
import toolauth


def get_reader_name(reader_id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT name
             FROM base
            WHERE id=(?);""",
        [reader_id],
    )
    return cur.fetchone()["name"]


def get_tool_name(tool_id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT name
             FROM base
            WHERE tool_id=(?);""",
        [tool_id],
    )
    return cur.fetchone()["name"]


def get_tool_name_from_drupal(drupal_name):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT tool_id
             FROM tool
            WHERE drupal_name=(?);""",
        [drupal_name],
    )
    tool_id = cur.fetchone()["tool_id"]
    cur = db.execute(
        """SELECT name
             FROM base
            WHERE tool_id=(?);""",
        [tool_id],
    )
    return cur.fetchone()["name"]


def get_tool_from_base(id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT tool_id
             FROM base
            WHERE id=(?);""",
        [id],
    )
    return cur.fetchone()["tool_id"]


def get_member_name(member_id):
    # probably need to ask Drupal...
    return  # name


def get_base_from_tool(tool_id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id, name
             FROM base
            WHERE tool_id=(?);""",
        [tool_id],
    )
    return cur.fetchone()


def get_base_from_reader(reader_id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id, name
             FROM base
            WHERE id=(?);""",
        [reader_id],
    )
    return cur.fetchone()


def get_encrypt_pass(id):
    print("get_encrypt_pass | id: " + str(id))
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT encrypt_pass
             FROM base
            WHERE id=(?);""",
        [id],
    )
    return cur.fetchone()["encrypt_pass"]


def get_tool_is_busy(tool_id):
    db = toolauth._get_db()
    # get the most recent session_id for the tool
    cur = db.execute(
        """SELECT id
             FROM session_core
            WHERE tool_id = (?)
         ORDER BY id DESC;""",
        [tool_id],
    )
    latest_session = cur.fetchone()
    # guard clause | return false if the tool has never been used
    if latest_session is None:
        return False
    # check the most recent session_event to find if tool is busy
    cur = db.execute(
        """SELECT active_session
             FROM session_event
            WHERE session_id = (?)
         ORDER BY id DESC;""",
        [latest_session],
    )
    if cur.fetchone()["active_session"] == 1:
        return True
    else:
        return False


def get_session_reader(id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT reader_id
             FROM session_core
            WHERE id=(?);""",
        [id],
    )
    return cur.fetchone()["reader_idd"]


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
