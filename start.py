import json

import EV3_S4T_ROS.modules.api as API

if __name__=="__main__":
    # Token request
    token = API.getToken()
    json_data = json.loads(token.text)
    print(json.dumps(json_data, indent = 4, sort_keys=True))#stampa in modo leggibile
    
    print("#####################################################################")
    print("#####################################################################")
    print("#####################################################################")
    
    # connected boards request
    #boards = API.getBoards(token)
    #json_data = json.loads(boards.text)
    #print(json.dumps(json_data, indent = 4, sort_keys=True))#stampa in modo leggibile
    
    # looking for a device called "webcam"
    #API.searchBoard(token, boards, 'webcam')
    #json_data = json.loads(prova.text)
    #print(json.dumps(json_data, indent = 4, sort_keys=True))#stampa in modo leggibile
    print(API.postPlugin(token, 'data/plugins/camera.py', 'camera2', "false", "true", ""))
    print(API.postPlugin(token, 'data/plugins/startCamera.py', 'startCamera', "true", "true", "")) #devo inserire parametri per id plugin
    print(API.injectPlugin(token, "webcam", "camera2", "false").text)


    #print(API.getLocation)