from toolauth.services.esphome_api import device_enable
from quart import abort
import yaml
import os 

async def reader_to_listed_tools(device_name, card_uid, member_name, member_uid, reader_name, reader_uid, session_uid):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'config/readertodevice.yaml')
    
    with open(path, 'r') as file:           
        pairings = yaml.safe_load(file)
        devices = []
        for n in pairings:
            if n['reader']['name'] == reader_name:
                devices = n['devices']
    
    err_catch=[]
    for d in devices:
        device_name = d['name']
        device_uid = d['id']
        resp = await device_enable(device_name, card_uid, member_uid, member_name, session_uid)
        if resp: err_catch.append(resp)
    
    if len(err_catch)>=1: 
        return abort(500, "Could not connect to ESPHome device. Check network and config files.") 
        # would be nice if we could report the good & bad esphome conenctions here