import telebot
import a2s
import time
import waitress
import threading
from asyncio import new_event_loop, set_event_loop
from app import create_app
from app.requests import get_players_data

addrs_server = ("46.174.52.22", 27213)
tgbot = telebot.TeleBot('6448127663:AAERpRolcSEpaJAH7cCRhNzn8bMdZKZcqjc')

chat_id = -1001951718196

chat_members = ['alexandertruewig', 'dxnteee', 'mtmrphosis ', 'b0lLb', 'Flamethrower1337 ', 'destinyfire', 'speedgainer', \
    'barakudboy', 'mex13370', 'galyapypsik', 'l0l0l0l0l0l00l', 'young_sakura', 'haikoro', 'mightyskrudge', 'girlsarethesame',\
    'cloudy1337', 'Lukaa']

play_members = ['' for i in range(tgbot.get_chat_member_count(chat_id))]
noplay_members = chat_members
print(noplay_members)
print(play_members)

def get_server_info():
    info = a2s.info(addrs_server)
    mssg = ''
    mssg = str(info.server_name) + '\n' + '<b>Online:</b> ' \
        + str(info.player_count) + '/' + str(info.max_players) \
        + '\n' + '<b>Map:</b> ' + str(info.map_name) + '\n' + '\n' + '<b>Status:</b> ' + str(info.game)
    return mssg
    
def get_players():
    players = get_players_data()
    print(players)
    mssg = ''
    for i in range(0, len(players)):
        mssg = mssg + '<b><i>' + players[i] + '</i></b>' + '\n'
    return mssg

@tgbot.message_handler(commands=['online', 'now'])
def online_now(message):
    msgg = ''
    msgg = get_server_info() + '\n'
    
    if(a2s.info(addrs_server).player_count > 0):
        msgg = '\n' + msgg + '\n' \
            + '=-----------------------=' + '\n' \
            + get_players() + '\n' \
            
    tgbot.send_message(message.chat.id, msgg, parse_mode='html')
    
@tgbot.message_handler(commands=['all'])
def all(message):
    msgg = ''
    for i in range(len(play_members)):
        if play_members[i] != '': 
            msgg += '\n' + '@' + play_members[i]
    tgbot.send_message(chat_id, msgg)
    
@tgbot.message_handler(commands=['play', 'noplay'])
def set_member_status(message):
    list = message.text[1:].split()
    cmd = list[0]
    username = message.from_user.username
    if(cmd == 'play'):
        if username in play_members:
            return
        if username in noplay_members:
            for i in range(len(noplay_members)):
                if noplay_members[i] == username:
                    noplay_members[i] = ''

            for i in range(len(play_members)):
                if play_members[i] == '':
                    play_members[i] = username
                
    elif cmd == 'noplay':
        if username in noplay_members:
            return
        if username in play_members:
            for i in range(len(play_members)):
                if play_members[i] == username:
                    play_members[i] = ''

            for i in range(len(noplay_members)):
                if noplay_members[i] == '':
                    noplay_members[i] = username
                
@tgbot.message_handler(commands=['author'])
def author(message):
    tgbot.send_message(chat_id, 'Antarktida: https://github.com/qwingel')

def bot_polling():
    while True:
        try:
            set_event_loop(new_event_loop())
            tgbot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(str(e))

def start_sserv():
    waitress.serve(app=create_app(), port=80)

bot_thread = threading.Thread(target=bot_polling)
bot_thread.daemon = True
bot_thread.start()

app_thread = threading.Thread(target=start_sserv)
app_thread.daemon = True
app_thread.start()

if __name__ == '__main__':
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break