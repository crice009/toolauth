import sys
from dataclasses import asdict
from aioesphomeapi.client import APIClient
from aioesphomeapi.model import UserService
from aioesphomeapi.model import UserServiceArg
from aioesphomeapi.model import UserServiceArgType
from toolauth.api.auth.models import AuthEnableServicePayload


async def device_enable(
    device_name: str, card_uid: str, member_uid: int, member_name: str, session_uid: int
) -> str | None:
    """
    Calls ESPHome service to activate an ESP32. Assumes that a successful auth request has been made.
    """
    api = APIClient(
        address=f"{device_name.strip()}.local",
        port=6053,
        password="",
        noise_psk="7NuG+LMZHTgyWCblaZnvn03acjyDnYYJz01BScw3eHM=",
    )
    try:
        await api.connect(login=True)
    except:
        raise Exception(
            f"Could not connect to ESPHome device: {device_name} during ESPHome auth_enable Native API call."
        )

    _, user_services = await api.list_entities_services()
    service_keys = {s.name: s.key for s in user_services}
    auth_enable_key = service_keys.get("auth_enable", 0)

    service = UserService(
        name="auth_enable",
        key=auth_enable_key,
        args=[
            UserServiceArg(name="member_uid", type=UserServiceArgType.INT),
            UserServiceArg(name="member_name", type=UserServiceArgType.STRING),
            UserServiceArg(name="card_uid", type=UserServiceArgType.STRING),
            UserServiceArg(name="session_uid", type=UserServiceArgType.INT),
        ],
    )
    args = AuthEnableServicePayload(
        member_name=member_name,
        member_uid=member_uid,
        card_uid=card_uid,
        session_uid=session_uid,
    )

    try:
        return await api.execute_service(service, asdict(args))
    except Exception as e:
        print(e, file=sys.stderr)
        return device_name


async def other_picked(device_name: str) -> str | None:
    print("made it to other_picked()", file=sys.stdout)

    api = APIClient(
        address=device_name.strip() + ".local",
        port=6053,
        password="",
        noise_psk="7NuG+LMZHTgyWCblaZnvn03acjyDnYYJz01BScw3eHM=",
    )
    try:
        await api.connect(login=True)
    except:
        raise Exception(
            "Could not connect to ESPHome device: "
            + device_name
            + " During ESPHome other_picked Native API call."
        )

    _, user_services = await api.list_entities_services()
    service_keys = {s.name: s.key for s in user_services}
    other_picked_key = service_keys.get("other_picked", 0)
    service = UserService(name="other_picked", key=other_picked_key, args=[])

    try:
        return await api.execute_service(service, {})
    except Exception as e:
        print(e, file=sys.stderr)
        return device_name
