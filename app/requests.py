from flask import Blueprint, request, session

module = Blueprint("main", __name__, url_prefix="/")

players_data = ['' for i in range(32)]

@module.post("/")
def index():
    data = request.get_json()

    PlayerSDATA = data["PlayerSDATA"]

    if PlayerSDATA not in players_data:
        for i in range(len(players_data)):
            if(players_data[i] == ''):
                players_data[i] = PlayerSDATA
                break

    print(data)
    return PlayerSDATA

@module.post("/delete")
def clear_data():
    data = request.get_json()

    PlayerSDATA = data["PlayerSDATA"]
    if PlayerSDATA in players_data:
        for i in range(len(players_data)):
            if(players_data[i] == PlayerSDATA):
                players_data[i] = ''
    
    print(data)
    return PlayerSDATA

def get_players_data():
    players = players_data
    print(players)
    return players