from aioesphomeapi.client import APIClient
from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
import yaml #easierthanadb.yaml (only while testing)
import os
import sys

async def device_enable(device_name, card_uid, member_uid, member_name, session_uid) -> None:
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'easierthanadb.yaml')
    with open(path, 'r') as file:           #easierthanadb.yaml (only while testing)
        keys = yaml.safe_load(file)                             #easierthanadb.yaml (only while testing)
        auth_enable_key = keys['jointer']['auth_enable_key']    #easierthanadb.yaml (only while testing)

    api = APIClient(
        address= device_name.strip()+".local",  # <----------------------------| will be unique for each tool controller
        port=6053,  # <--------------------------------------------------------| will probably be the same for all ESP32s
        password=os.environ.get("ESPHOME_PASSWORD"),  # <------------------------------------------------------| Don't think we'll use this
        noise_psk=os.environ.get("ESPHOME_NOISE_PSK"),  # <---------| will be the same for all ESP32s (in secret.yaml)
    )
    await api.connect(login=True)

    # List all entities of the device
    entities = await api.list_entities_services()
    user_services = [e for e in entities[1] if e.name == "auth_enable"] #< this is brilliant, but there is also an 'other_picked' service
    auth_enable_service = user_services[0] if user_services else None
    auth_enable_key = auth_enable_service.key if auth_enable_service else 0

    # -------------------------------------------------------------------------------------------
    # need this:
    # from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
    service = UserService(
        name="auth_enable",  # <------------------------------------------------| will be the same for all ESP32s
        key=auth_enable_key,  # <-----------------------------------------------| will be unique for each ESP32 and can only get after provisioning
        args=[  # needd to be in the same order as ESPHome
            #must be in this order (from ESPHome)
            # member_uid: int
            # member_name: string
            # card_uid: string
            # session_uid: int
            UserServiceArg(name="member_uid", type=UserServiceArgType.INT),
            UserServiceArg(name="member_name", type=UserServiceArgType.STRING),
            UserServiceArg(name="card_uid", type=UserServiceArgType.STRING),
            UserServiceArg(name="session_uid", type=UserServiceArgType.INT),
        ],
    )
    data = {"member_name":member_name, "member_uid":member_uid, "card_uid":card_serial, "session_uid":session_id}
    try:
        await api.execute_service(service, data)
        return False
    except Exception as e: 
        print(e, file=sys.errout)
        return device_name
    # -------------------------------------------------------------------------------------------