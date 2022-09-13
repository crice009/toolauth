from toolauth.services.esphome_api import device_enable
from quart import abort
import yaml
import os 

#could reduce the number of inputs to just reader_uid & session_uid, if the yaml or database are working
async def reader_to_listed_tools(device_name, card_uid, member_name, member_uid, reader_name, reader_uid, session_uid):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'config/readertodevice.yaml')
    
    with open(path, 'r') as file:           
        pairings = yaml.safe_load(file)
        devices = []
        for n in pairings:
            if n['reader']['name'] == reader_name:
                devices = n['devices']

        if len(devices) < 1:
            raise Exception("Did not find requested reader/device pair in YAML config. Reader: " + reader_name+" | Device: "+device_name)
    
    err_catch=[]
    for d in devices:
        device_name = d['name']
        device_uid = d['id']
        resp = await device_enable(device_name, card_uid, member_uid, member_name, session_uid)
        if resp: err_catch.append(resp)
    
    if len(err_catch)>=1: 
        raise Exception("Could not connect to ESPHome device(s): ".join(err_catch)+". Check network and config files.")