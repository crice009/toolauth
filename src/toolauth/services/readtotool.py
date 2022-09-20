from toolauth.services.esphome_api import device_enable, tool_com_error
from toolauth.services.authorized import is_member_authorized

import asyncio, yaml, sys, os


# could reduce the number of inputs to just reader_uid & session_uid, if the yaml or database are working
async def reader_to_listed_tools(session):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "config/readertodevice.yaml")

    with open(path, "r") as file:
        pairings = yaml.safe_load(file)
        devices = []
        if any(session.reader_name in n["reader"]["name"] for n in pairings):
            for n in pairings:
                if n["reader"]["name"] == session.reader_name:
                    devices = n["devices"]
        else:
            raise Exception(
                "Did not find requested reader in YAML config. Reader: "
                + session.reader_name
            )

        if len(devices) < 1:
            raise Exception(
                "Checked YAML, and found no devices assigned to reader: "
                + session.reader_name
            )
    try:
        com_err_catch = []
        for d in devices:
            session.device_name = d["name"]
            session.device_uid = d["id"]
            allowed = is_member_authorized(session)
            if allowed:
                session.potential_devices.append(
                    {"name": session.device_name, "id": session.device_uid}
                )
                response_err = await device_enable(session)
            if response_err is not None:
                com_err_catch.append(com_err_catch.device_name)

        if len(com_err_catch) >= 1:
            raise Exception(
                "Could not connect to ESPHome device(s): ".join(com_err_catch)
                + ". Check network and config files."
            )
    except Exception as e:
        print(e, file=sys.stderr)
        await tool_com_error(session.reader_name, com_err_catch)


# threading wrapper
def trigger_device_after_response(session):
    asyncio.run(reader_to_listed_tools(session))
