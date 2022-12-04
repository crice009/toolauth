from aioesphomeapi.client import APIClient
from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
from .getters_setters import (
    get_base_from_tool,
    get_base_from_reader,
    get_encrypt_pass,
    get_tool_name,
    get_reader_name,
)
import asyncio, sys, logging

# ===============================================================================
# \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
#  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /
#   \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/
# ===================================== NEW =====================================


# threading wrapper
def threaded_tool_enable(tool, session_id):
    asyncio.run(tool_enable(tool, session_id))


# put a tool in 'enable' mode for a short time
async def tool_enable(tool, session_id) -> None:
    print("made it to tool_enable")
    base = get_base_from_tool(tool)
    encrypt_pass = get_encrypt_pass(base["id"])

    api = APIClient(
        address=base["name"] + ".local",
        port=6053,
        password="",
        noise_psk=encrypt_pass,
    )
    try:
        await api.connect(login=True)
    except:
        # this may be premature - maybe only raise the exception after trying all the listed tools?
        await tool_com_error(base["id"], tool)
        raise Exception(
            "Could not connect to ESPHome tool: "
            + base["name"]
            + " During ESPHome auth_enable Native API call."
        )

    # List all entities of the tool
    entities, user_services = await api.list_entities_services()
    # < this is brilliant, but there is also an 'other_picked' service
    services = dict((s.name, s) for s in user_services)
    service_keys = dict((s.name, s.key) for s in user_services)
    # print("Service Keys for "+tool["name"]+": "+json.dumps(service_keys), file=sys.stdout)
    auth_enable_key = service_keys.get("auth_enable", 0)
    # other_picked_key = service_keys.get("other_picked", 0)

    # need this:
    # from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
    service = UserService(
        name="auth_enable",
        key=auth_enable_key,  # will be unique for each ESP32 and can only get after provisioning
        args=[  # need to be in the same order as ESPHome
            UserServiceArg(name="session_uid", type=UserServiceArgType.INT),
        ],
    )
    data = {
        "session_uid": session_id,
    }

    try:
        await api.execute_service(service, data)
        return
    except Exception as e:
        print(e, file=sys.stderr)
        logging.info(e)
        return
    # -------------------------------------------------------------------------------------------


# some other tool was chose, so end the 'enable' session on unsused tools
async def other_picked(tool, session_id) -> None:
    print("made it to other_picked()", file=sys.stdout)
    base = get_base_from_tool(tool)
    encrypt_pass = get_encrypt_pass(base["id"])

    api = APIClient(
        address=base["name"] + ".local",
        port=6053,
        password="",
        noise_psk=encrypt_pass,
    )
    try:
        await api.connect(login=True)
    except:
        raise Exception(  # message back to server
            "Could not connect to ESPHome device: "
            + base["name"]
            + " During ESPHome other_picked Native API call."
        )

    # List all UserService's of the device
    entities, user_services = await api.list_entities_services()
    service_keys = dict((s.name, s.key) for s in user_services)
    # print("Service Keys for "+tool["name"]+": "+json.dumps(service_keys), file=sys.stdout)
    other_picked_key = service_keys.get("other_picked", 0)

    # define the service to be contacted
    service = UserService(name="other_picked", key=other_picked_key, args=[])
    data = {}

    try:
        await api.execute_service(service, data)
        return  # everything worked
    except Exception as e:
        print(e, file=sys.stderr)
        logging.info(e)
        return


# -------------------------------------------------------------------------------------------


async def tool_com_error(reader_id, tool_id) -> None:
    print(
        "tool_com_error | reader_id: " + str(reader_id) + "  tool_id: " + str(tool_id)
    )
    base_name = get_reader_name(reader_id)
    encrypt_pass = get_encrypt_pass(reader_id)
    print(base_name + "     " + encrypt_pass)

    api = APIClient(
        address=base_name + ".local",
        port=6053,
        password="",
        noise_psk=encrypt_pass,
    )
    try:
        await api.connect(login=True)
    except:
        raise Exception(  # message back to server
            "Could not connect to ESPHome device: "
            + base_name
            + " During ESPHome tool_com_error Native API call, while trying to report error reaching the device:"
            + get_tool_name(tool_id)
        )

    # List all UserService's of the device
    entities, user_services = await api.list_entities_services()
    service_keys = dict((s.name, s.key) for s in user_services)
    # print("Service Keys for "+device_name+": "+json.dumps(service_keys), file=sys.stdout)
    tool_com_key = service_keys.get("tool_com_error", 0)

    # define the service to be contacted
    service = UserService(name="tool_com_error", key=tool_com_key, args=[])
    data = {}

    try:
        await api.execute_service(service, data)
        return  # everything worked
    except Exception as e:
        print(e, file=sys.stderr)
        logging.info(e)
        return
