import telebot
import a2s
import time
import waitress
import threading
from asyncio import new_event_loop, set_event_loop
from app import create_app

chat_id = 123

hashira_address = ("IP", 11111)
hkz_address = ("IP", 11111)

file = "kz-rec.txt"
records_file = open(file, "rt", encoding='utf-8')
records_list = list(records_file)
count_lines = sum(1 for line in open(file, "r"))

tgbot = telebot.TeleBot('')

chat_members = [
    
]

play_members = ['' for i in range(tgbot.get_chat_member_count(chat_id))]
print(play_members)

def get_cosy_record(map):
    for i in range(count_lines):
        list = records_list[i].split()
        if(map in list):
            print(records_list[i])
    
def get_server_info():
    info = a2s.info(hashira_address)
    mssg = ''
    mssg = str(info.server_name) + '\n' + '<b>Online:</b> ' \
        + str(info.player_count) + '/' + str(info.max_players) \
        + '\n' + '<b>Map:</b> ' + str(info.map_name) + '\n' + '\n' + '<b>Status:</b> ' + str(info.game)
    return mssg
    
def get_players():
    players = a2s.players(hashira_address)
    msgg = ''
    for i in range(0, len(players)):
        msgg = msgg + '\n' + '> ' + '<b>' + str(players[i].name) + '</b>'

        
    return msgg

def get_hkz_info():
    info = a2s.info(hkz_address)
    players = a2s.players(hkz_address)
    mssg = ''
    mssg = str(info.server_name) + '\n' + '<b>Online:</b> ' \
        + str(info.player_count) + '/' + str(info.max_players) \
        + '\n' + '<b>Map:</b> ' + str(info.map_name)
    
    msgg = ''
    record = ''
    for i in range(len(players)):
        if(players[i].score < 0):
            record = '<b>Server Record:</b>' + str(players[i].name)
        else:
            msgg = get_cosy_record(info.map_name) + '\n\n'
            msgg = msgg + '\n' + '> ' + str(players[i].name)
        
    return mssg + '\n' + record + '\n' + msgg 

@tgbot.message_handler(commands=['online', 'now'])
def online_hashira_now(message):
    msgg = ''
    msgg = get_server_info() + '\n'
    
    if(a2s.info(hashira_address).player_count > 0):
        msgg = '\n' + msgg + '\n' \
            + '=-----------------------=' \
            + get_players() + '\n' \
            + '=-----------------------='
            
    tgbot.send_message(message.chat.id, msgg, parse_mode='html')

@tgbot.message_handler(commands=['hkz'])
def online_hkz_now(message):
    msgg = get_hkz_info()
    tgbot.send_message(message.chat.id, msgg, parse_mode='html')

@tgbot.message_handler(commands=['all'])
def all(message):
    msgg = ''
    if play_members.count('') > len(play_members) - 1:
        return
    
    for i in range(len(play_members)):
        if play_members[i] != '': 
            msgg += '\n' + '@' + play_members[i]
    tgbot.send_message(message.chat.id, msgg)
    
@tgbot.message_handler(commands=['play', 'noplay'])
def set_member_status(message):
    list = message.text[1:].split()
    cmd = list[0]
    username = message.from_user.username
    if(cmd == 'play'):
        if username not in play_members:
            for i in range(len(play_members)):
                if play_members[i] == '':
                    play_members[i] = username
                    break
                
    elif cmd == 'noplay':
        if username in play_members:
            for i in range(len(play_members)):
                if play_members[i] == username:
                    play_members[i] = ''
                    break

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
