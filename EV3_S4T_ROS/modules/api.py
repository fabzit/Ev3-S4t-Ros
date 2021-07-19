import requests
import json
from datetime import datetime

ip = "http://212.189.207.233"

def getToken():
    url = ip + ':5000/v3/auth/tokens'
    headers = {'Content-Type' : 'application/json'}
    t = requests.post(url, data=open('data/auth.json', 'rb'), headers=headers)
    return t

def check_expiration(expires_at):
    current_date = datetime.now()
    expires_at = datetime.fromisoformat(expires_at[:-1]) #Levo la Z
    return current_date < expires_at #True=valida False=scaduta 

def getBoards(token):
    expires_at = token.json()['token']['expires_at']
    if token=="" or check_expiration(expires_at):
        token = getToken()
    url = ip + ':8812/v1/boards/'
    headers = {'Content-Type' : 'application/json','X-Auth-Token' : token.headers["X-Subject-Token"]}
    r = requests.get(url, headers=headers)
    return r

def getDetailsFromBoard(token, boardID):
    expires_at = token.json()['token']['expires_at']
    if token=="" or check_expiration(expires_at):
        token = getToken()
    url = ip + ':8812/v1/boards/'+boardID
    headers = {'X-Auth-Token' : token.headers["X-Subject-Token"]}
    r = requests.get(url, headers=headers)
    return r

def searchBoard(token, boards, board_name):
    boards = boards.json()
    for i in boards['boards']:
        if board_name in i['name']:
            if i['status'] == 'online':
                oggetto = i             
    if oggetto != "":
        print ('Ha il seguente IP: '+oggetto['connectivity']['local_ip']+' e i seguenti servizi: ')
        json_data = json.loads(getDetailsFromBoard(token, oggetto['uuid']).text)
        print(json.dumps(json_data, indent = 4, sort_keys=True))#stampa in modo leggibile
    else:
        print("Non è stato trovato nessun: ", board_name)

def postPlugin(token, path, name, callable, public, parameters):
    expires_at = token.json()['token']['expires_at']
    if token=="" or check_expiration(expires_at):
        token = getToken()
    url = ip + ':8812/v1/plugins'
    headers = {'Content-Type' : 'application/json', 'X-Auth-Token' : token.headers["X-Subject-Token"]}
    file = open(path, 'r').read()
    data_set = {
        "code": file,
        "name": name,
        "callable": callable,
        "public": public,
        "parameters": parameters
        }
    json_dump = json.dumps(data_set)
    r = requests.post(url, data=json_dump, headers=headers)
    return r

def injectPlugin(token, board_name, plugin_name, onboot):
    expires_at = token.json()['token']['expires_at']
    if token=="" or check_expiration(expires_at):
        token = getToken()
    url = ip + ':8812/v1/boards/{}/plugins'.format(board_name)
    headers = {'Content-Type' : 'application/json', 'X-Auth-Token' : token.headers["X-Subject-Token"]}
    data_set = {
        "plugin": plugin_name,
        "onboot": onboot,
        }
    json_dump = json.dumps(data_set)
    r = requests.put(url, data=json_dump, headers=headers)  
    return r

def executePlugin(token, board_name, plugin_name, parameters):
    expires_at = token.json()['token']['expires_at']
    if token=="" or check_expiration(expires_at):
        token = getToken()
    url = ip + ':8812/v1/boards/{}/plugins/{}'.format(board_name, plugin_name)
    headers = {'Content-Type' : 'application/json', 'X-Auth-Token' : token.headers["X-Subject-Token"]}
    data_set = {
        "action": "PluginCall",
        "parameters": parameters
        }
    json_dump = json.dumps(data_set)
    print(json_dump)
    r = requests.post(url, data=json_dump, headers=headers)
    return r          