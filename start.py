import EV3_S4T_ROS.modules.api as API
import json

if __name__=="__main__":
    token = API.getToken()
    json_data = json.loads(token.text)
    print(print(json.dumps(json_data, indent = 4, sort_keys=True)))#stampa in modo leggibile
    print("#####################################################################")
    print("#####################################################################")
    print("#####################################################################")
    boards = API.getBoards(token)
    json_data = json.loads(boards.text)
    print(print(json.dumps(json_data, indent = 4, sort_keys=True)))#stampa in modo leggibile
    
    #API.searchBoard(boards, 'webcam')

    
    #print(API.getLocation)