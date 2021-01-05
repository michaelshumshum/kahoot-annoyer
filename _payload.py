import json
import time
import random

def lag():
    return random.randint(50,400)

def get_tc():
  return int(time.time() * 1000)

def name_payload(name,pin,clientId):
    name = str(name)
    data = [{"channel": "/service/controller", "clientId": clientId, "data": {"gameid": pin, "host": "kahoot.it", "name": name, "type": "login"}, "id": "14"}]
    return str(json.dumps(data))

def handshake_payload(ack):
    data = [{"advice": {"interval": 0, "timeout": 60000}, "channel": "/meta/handshake", "ext": {"ack": ack, "timesync": {"l": '0', "o": '-14', "tc": get_tc()}}, "id": "2", "minimumVersion" : "1.0", "supportedConnectionTypes": ["long-polling"], "version": "1.0"}]
    return str(json.dumps(data))

def first_con_payload(ack,clientId,subId):
    data = [{"advice": {"timeout": 0}, "channel": "/meta/connect", "clientId": clientId, "connectionType": "long-polling", "ext": {"ack": ack, "timesync": {"l": "0", "o": "-14", "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

def second_con_payload(ack,clientId,subId):
    data = [{"channel": "/meta/connect", "clientId": clientId, "connectionType": "long-polling", "ext": {"ack": ack, "timesync": {"l": "0", "o": "-14", "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

def answer_payload(pin,clientId,subId,choice,type):
    if type == 'quiz':
        choice = int(choice)
        id = 6
        answer = 'choice'
    elif type == 'open':
        id = 45
        choice = str(choice)
        answer = 'text'
    else:
        choice = list(choice)
        id = 45
        answer = 'choice'
    innerdata = {answer : choice, "meta": {"lag": lag(), "device": {"userAgent": "bigup_UK_grime", "screen": {"width": 1920, "height": 1080}}}}
    innerdata = json.dumps(innerdata)
    data = [{"channel": "/service/controller", "clientId": clientId, "data": {"content": innerdata, "gameid": pin, "host": "kahoot.it", "id": id, "type": "message"}, "id": subId}]
    return str(json.dumps(data))
