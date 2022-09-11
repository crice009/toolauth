import urllib.request, json
import os

async def authreq(data):
    # device_name="str", #text-based name for tool intended to use 
    # device_uid="str",  #some kind of ID number for tool intended
    # reader_name="str", #text-based name for card reader
    # reader_uid="str",  #some kind of ID number for card reader
    # card_uid="str",    #the card_uid of member asking for permission
    
    device_name = data.get("device_name").strip()
    card_uid = data.get("card_uid", "").replace("-", "").lower()

    response = await ask_drupal(device_name, card_uid)
    if response:
        return response
    else:
        return False


async def ask_drupal(device_name, card_uid):
    #drupal6 is the current card system, so work with that
    # https://www.makehaven.org/api/v0/serial/04376A6A5F5780/permission/door
    # https://www.makehaven.org/api/v0/serial/<card_uid>/permission/<badge_name>
    url = "https://www.makehaven.org/api/v0/serial/"+card_uid+"/permission/"+device_name

    response = urllib.request.urlopen(url)
    data = response.read()
    drupal_response = json.loads(data)
    # expecting: [{"permission":"Door","access":"true","uid":"2"}] #and 'uid' is the member id number
    if len(drupal_response)>=1: #returns [] from drupal if not authorized
        member_uid = drupal_response[0]["uid"]
        return member_uid
    else:
        return False #member not authorized for tool