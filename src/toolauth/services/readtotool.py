from toolauth.services.esphome_api import device_enable
import yaml
import os


async def reader_to_listed_tools(
    device_name, card_uid, member_name, member_uid, reader_name, reader_uid, session_uid
):
    """
    Could reduce the number of inputs to just reader_uid & session_uid, if the yaml
    or database are working.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "config/readertodevice.yaml")

    with open(path, "r") as file:
        pairings = yaml.safe_load(file)
        devices = [n["devices"] for n in pairings if n["reader"]["name"] == reader_name]

        if not len(devices):
            raise Exception(
                f"Did not find requested reader/device pair in YAML config. Reader: {reader_name} | Device: {device_name}"
            )

    err_catch = []
    for d in devices:
        resp = await device_enable(
            d["name"], card_uid, member_uid, member_name, session_uid
        )
        if resp:
            err_catch.append(resp)

    if len(err_catch):
        raise Exception(
            f"{'Could not connect to ESPHome device(s): '.join(err_catch)}. Check network and config files."
        )
