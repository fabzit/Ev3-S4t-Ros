import requests
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
    return r.json()

def searchBoard(boards, board_name):
    for i in boards['boards']:
        if board_name in i['name']:
            if i['status'] == 'online':
                print ('TROVATO e ONLINE')
                print ('Ha il seguente IP: '+i['connectivity']['local_ip']+' e i seguenti servizi: ')
                print(getDetailsFromBoard(token, i['uuid']))
            else:
                print ('TROVATO ma OFFLINE')
                print ('Ha il seguente IP: '+i['connectivity']['local_ip']+' e i seguenti servizi: ')
                print(getDetailsFromBoard(token, i['uuid']))    
        else:
            print ('Non ho trovato nessun device con nome: ', board_name)