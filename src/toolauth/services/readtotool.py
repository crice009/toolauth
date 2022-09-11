from toolauth.services.esphome_api import device_enable
import yaml
import os 

async def reader_to_listed_tools(device_name, card_uid, member_name, member_uid, reader_name, reader_uid, session_uid):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'config/readertodevice.yaml')
    
    with open(path, 'r') as file:           
        pairings = yaml.safe_load(file)
        for n in pairings:
            if n['reader']['name'] == reader_name:
                devices = n['devices']
    
    err_catch=[]
    for d in devices:
        device_name = d['name']
        device_uid = d['id']
        resp = await device_enable(device_name, card_uid, member_uid, member_name, session_uid)
        # if resp: err_catch.append(resp)
    
    if len(err_catch)>=1: 
        raise Exception(err_catch) #could not reach ESPHome device