from flask import Blueprint, request, session

module = Blueprint("main", __name__, url_prefix="/")

players_data = ['' for i in range(32)]

@module.post("/")
def index():
    data = request.get_json()

    nickname = data["nick"]
    SteamID = "https://steamcommunity.com/profiles/" + data["SteamID"]
    result = nickname + ' : ' + SteamID

    if result not in players_data:
        for i in range(len(players_data)):
            if(players_data[i] == ''):
                players_data[i] = result

    print(data)
    return result, players_data

@module.post("/delete")
def clear_data():
    data = request.get_json()

    nickname = data["nick"]
    SteamID = "https://steamcommunity.com/profiles/" + data["SteamID"]
    result = nickname + ' : ' + SteamID
    if result in players_data:
        for i in range(len(players_data)):
            if(players_data[i] == result):
                players_data[i] = ''
    
    print(data)
    return result, players_data

def get_players_data():
    players = players_data
    print(players)
    return players