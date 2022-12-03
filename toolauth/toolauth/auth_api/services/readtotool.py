from .getters_setters import get_reader_name
import toolauth, logging


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== READ ====================================


# ===============================================================================
# ===============================================================================
# ===============================================================================


async def get_tools_for_a_reader(reader_id):
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT tool_id
             FROM reader_to_tool
            WHERE reader_id=(?)""",
        [reader_id],
    )
    tools = cur.fetchall()
    # throw an exception if there aren't any asigned tools
    if len(tools) < 1:
        raise Exception(
            "Did not find requested any reader_to_tool pairings in database. Reader: "
            + get_reader_name(reader_id)
        )
    for i in tools:
        print("reader # " + str(reader_id) + "  tool # " + str(i["tool_id"]))
        cur = db.execute(
            """SELECT id, drupal_name
                FROM tool
                WHERE id=(?)""",
            [i["tool_id"]],
        )
        tools = cur.fetchall()
    return tools


# ===============================================================================
async def put_tools_in_enable_mode(tools):
    pass
