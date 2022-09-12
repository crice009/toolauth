from aioesphomeapi.client import APIClient
from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
import yaml  # easierthanadb.yaml (only while testing)
import os
import sys


async def device_enable(device_name, card_uid, member_uid, member_name, session_uid) -> None:
    print("made it to device_enable()", file=sys.stdout)
    # path = os.path.dirname(os.path.realpath(__file__))
    # path = os.path.join(path, 'easierthanadb.yaml')
    # with open(path, 'r') as file:  # easierthanadb.yaml (only while testing)
    #     keys = yaml.safe_load(file)  # easierthanadb.yaml (only while testing)
    #     for k in keys:  # easierthanadb.yaml (only while testing)
    #         # easierthanadb.yaml (only while testing)
    #         if k['device'] == device_name:
    #             # easierthanadb.yaml (only while testing)
    #             auth_enable_key = k['auth_enable_key']

    api = APIClient(
        address=device_name.strip()+".local",
        port=6053,
        password="",
        noise_psk="7NuG+LMZHTgyWCblaZnvn03acjyDnYYJz01BScw3eHM=",
    )
    await api.connect(login=True)

    # List all entities of the device
    entities, user_services = (await api.list_entities_services())
    # < this is brilliant, but there is also an 'other_picked' service
    services = dict((s.name, s) for s in user_services)
    service_keys = dict((s.name, s.key) for s in user_services)
    auth_enable_key = service_keys.get("auth_enable", 0)
    # other_picked_key = service_keys.get("other_picked", 0)

    # -------------------------------------------------------------------------------------------
    # need this:
    # from aioesphomeapi.model import UserService, UserServiceArg, UserServiceArgType
    service = UserService(
        name="auth_enable",
        key=auth_enable_key,  # <-----------------------------------------------| will be unique for each ESP32 and can only get after provisioning
        args=[  # needd to be in the same order as ESPHome
            # must be in this order (from ESPHome)
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
    data = {"member_name": member_name, "member_uid": member_uid,"card_uid": card_uid, "session_uid": session_uid}
    
    try:
        await api.execute_service(service, data)
        return
    except Exception as e:
        print(e, file=sys.stderr)
        return device_name
    # -------------------------------------------------------------------------------------------