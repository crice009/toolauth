from quart import Blueprint, render_template, g, request, redirect, url_for
import toolauth
from toolauth.crud_gui.services import ecrypt_pass, ota_pass
import logging, datetime

# define this blueprint (collection of web-routes)
crud_gui = Blueprint(
    "crud_gui",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/crud_gui",
)

# main CRUD route
@crud_gui.route("/")
async def index():
    logging.info("visited crud_gui index-route")
    return await render_template("crud2.html")


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== CREATE ==================================
# make a new device
@crud_gui.route("/create/device", methods=["GET", "POST"])
async def create_device():
    # logging.info("visited /create/device")
    if request.method == "POST":
        db = toolauth._get_db()
        form = await request.form
        # logging.info(form.keys())
        # # https://stackoverflow.com/questions/65362517/why-are-unchecked-checkboxses-ignored-when-posting-a-form
        # has_reader = 0
        # if form["has_reader"] is not None:
        #     has_reader = 1
        last_tool = {}
        # logging.info("drupal_name: " + form["drupal_name"] + " | is_vacuum: " + form["is_vacuum"])
        if form["is_vacuum"] == "0" and form["drupal_name"].replace(" ", "") != "":
            db.execute(
                "INSERT INTO 'tool' (drupal_name) VALUES (?)",
                [form["drupal_name"]],
            )
            db.commit()
            cur = db.execute(
                "SELECT id FROM tool ORDER BY id DESC",
            )
            last_tool = cur.fetchone()
        else:
            last_tool["id"] = None
        db.execute(
            "INSERT INTO 'base' (name, encrypt_pass, ota_pass, has_reader, is_vacuum, tool_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                form["name"],
                ecrypt_pass(),
                ota_pass(),
                form["has_reader"],
                form["is_vacuum"],
                last_tool["id"],
                str(datetime.datetime.now()),
            ],
        )
        db.commit()
        return redirect(url_for("crud_gui.read_devices"))
    else:
        return await render_template("create/device.html")


# make a new reader-to-tool link
@crud_gui.route("/create/reader_to_tool", methods=["GET", "POST"])
async def create_reader_to_tool():
    # logging.info("visited /create/reader_to_tool")
    db = toolauth._get_db()
    if request.method == "POST":
        form = await request.form
        db.execute(
            "INSERT INTO 'reader_to_tool' (reader_id, tool_id, created_at) VALUES (?,?,?)",
            [form["reader"], form["tool"], str(datetime.datetime.now())],
        )
        db.commit()
        return redirect(url_for("crud_gui.read_reader_to_tool"))
    else:
        cur = db.execute(
            """SELECT id, name
                 FROM base
                WHERE has_reader='1';""",
        )
        selectable_readers = cur.fetchall()
        cur = db.execute(
            """SELECT tool_id, name
                 FROM base 
                WHERE tool_id IS NOT NULL;""",
        )
        selectable_tools = cur.fetchall()
        return await render_template(
            "create/reader_to_tool.html",
            selectable_readers=selectable_readers,
            selectable_tools=selectable_tools,
        )


# make a new tool-to-vacuum link
@crud_gui.route("/create/tool_to_vacuum", methods=["GET", "POST"])
async def create_tool_to_vacuum():
    # logging.info("visited /create/tool_to_vacuum")
    db = toolauth._get_db()
    if request.method == "POST":
        form = await request.form
        db.execute(
            "INSERT INTO 'tool_to_vacuum' (tool_id, vacuum_id, created_at) VALUES (?,?,?)",
            [form["tool"], form["vacuum"], str(datetime.datetime.now())],
        )
        db.commit()
        return redirect(url_for("crud_gui.read_tool_to_vacuum"))
    else:
        cur = db.execute(
            """SELECT tool_id, name
                 FROM base 
                WHERE tool_id IS NOT NULL;""",
        )
        selectable_tools = cur.fetchall()
        cur = db.execute(
            """SELECT id, name
                 FROM base
                WHERE is_vacuum='1';""",
        )
        selectable_vacuums = cur.fetchall()
    return await render_template(
        "create/tool_to_vacuum.html",
        selectable_tools=selectable_tools,
        selectable_vacuums=selectable_vacuums,
    )


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== READ ====================================
# read device list
@crud_gui.route("/read/devices")
async def read_devices():
    # logging.info("visited /read/devices")
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id, 
                  name, 
                  mac_addr,
                  ip_addr, 
                  encrypt_pass, 
                  ota_pass, 
                  has_reader, 
                  is_vacuum
             FROM base
         ORDER BY id DESC""",
    )
    devices = cur.fetchall()
    logging.info(devices[0].keys())
    return await render_template("read/devices.html", devices=devices)


# read reader_to_tool list
@crud_gui.route("/read/reader_to_tool")
async def read_reader_to_tool():
    # logging.info("visited /read/reader_to_tool")
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id, reader_id, tool_id
             FROM reader_to_tool
         ORDER BY id DESC""",
    )
    raw_reader_to_tools = cur.fetchall()
    reader_to_tools = []
    for pair in raw_reader_to_tools:
        this_pair = {}
        this_pair["raw"] = pair
        # logging.info(pair.keys())
        cur = db.execute(
            """SELECT name
                 FROM base
                WHERE id=(?);""",
            [pair["reader_id"]],
        )
        this_pair["reader"] = cur.fetchone()
        cur = db.execute(
            """SELECT name
                 FROM base
                WHERE tool_id=(?);""",
            [pair["tool_id"]],
        )
        this_pair["tool"] = cur.fetchone()
        # logging.info(this_pair["reader"].keys())
        reader_to_tools.append(this_pair)
    return await render_template(
        "read/reader_to_tool.html", reader_to_tools=reader_to_tools
    )


# read tool_to_vacuum list
@crud_gui.route("/read/tool_to_vacuum")
async def read_tool_to_vacuum():
    # logging.info("visited /read/tool_to_vacuum")
    db = toolauth._get_db()
    cur = db.execute(
        """SELECT id, tool_id, vacuum_id
             FROM tool_to_vacuum
         ORDER BY id DESC""",
    )
    raw_tool_to_vacuum = cur.fetchall()
    tool_to_vacuums = []
    for pair in raw_tool_to_vacuum:
        this_pair = {}
        this_pair["raw"] = pair
        cur = db.execute(
            """SELECT name
                 FROM base
                WHERE tool_id=(?);""",
            [pair["tool_id"]],
        )
        this_pair["tool"] = cur.fetchone()
        cur = db.execute(
            """SELECT name
                 FROM base
                WHERE id=(?);""",
            [pair["vacuum_id"]],
        )
        this_pair["vacuum"] = cur.fetchone()
        tool_to_vacuums.append(this_pair)
    return await render_template(
        "read/tool_to_vacuum.html", tool_to_vacuums=tool_to_vacuums
    )


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== UPDATE ==================================
# update device
@crud_gui.route("/update/device", methods=["POST"])
async def update_device():
    # logging.info("visited /update/device")
    db = toolauth._get_db()
    form = await request.form
    db.execute(
        """UPDATE base
              SET (?) = (?)
            WHERE id=(?);""",
        [form["key"], form["value"], form["id"]],
    )
    db.commit()
    return redirect(url_for("crud_gui.read_devices"))


# update reader_to_tool
@crud_gui.route("/update/reader_to_tool", methods=["POST"])
async def update_reader_to_tool():
    # logging.info("visited /update/reader_to_tool")
    return redirect(url_for("crud_gui.read_reader_to_tool"))


# update tool_to_vacuum
@crud_gui.route("/update/tool_to_vacuum", methods=["POST"])
async def update_tool_to_vacuum():
    # logging.info("visited /update/tool_to_vacuum")
    return redirect(url_for("crud_gui.read_tool_to_vacuum"))


# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== DELETE ==================================
# delete device
@crud_gui.route("/delete/device", methods=["POST"])
async def delete_device():
    # logging.info("visited /delete/device")
    db = toolauth._get_db()
    form = await request.form
    full_delete = {}
    cur = db.execute(
        """SELECT tool_id
             FROM base
            WHERE id=(?);""",
        [form["id"]],
    )
    full_delete["base"] = cur.fetchone()
    # ----delete associated reader_to_tool
    db.execute(
        """DELETE
             FROM reader_to_tool
            WHERE reader_id=(?);""",
        [form["id"]],
    )
    db.execute(
        """DELETE
             FROM reader_to_tool
            WHERE tool_id=(?);""",
        [full_delete["base"]["tool_id"]],
    )
    # ----delete associated vacuum_to_tool
    db.execute(
        """DELETE 
             FROM tool_to_vacuum
            WHERE tool_id=(?);""",
        [full_delete["base"]["tool_id"]],
    )
    db.execute(
        """DELETE 
             FROM tool_to_vacuum
            WHERE vacuum_id=(?);""",
        [form["id"]],
    )
    # ----delete the entities themselves
    db.execute(
        """DELETE 
             FROM base
            WHERE id=(?);""",
        [form["id"]],
    )
    db.execute(
        """DELETE
             FROM tool
            WHERE id=(?);""",
        [full_delete["base"]["tool_id"]],
    )
    db.commit()
    return redirect(url_for("crud_gui.read_devices"))


# delete reader_to_tool
@crud_gui.route("/delete/reader_to_tool", methods=["POST"])
async def delete_reader_to_tool():
    # logging.info("visited /delete/reader_to_tool")
    db = toolauth._get_db()
    form = await request.form
    logging.info("form['id']: " + form["id"])
    db.execute(
        """DELETE
             FROM reader_to_tool
            WHERE id=(?);""",
        [form["id"]],
    )
    db.commit()
    return redirect(url_for("crud_gui.read_reader_to_tool"))


# delete tool_to_vacuum
@crud_gui.route("/delete/tool_to_vacuum", methods=["POST"])
async def delete_tool_to_vacuum():
    # logging.info("visited /delete/tool_to_vacuum")
    db = toolauth._get_db()
    form = await request.form
    db.execute(
        """DELETE
             FROM tool_to_vacuum
            WHERE id=(?);""",
        [form["id"]],
    )
    db.commit()
    return redirect(url_for("crud_gui.read_tool_to_vacuum"))
