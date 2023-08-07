import telebot
import a2s

addrs_server = ("46.174.52.22", 27213)
tgbot = telebot.TeleBot('6448127663:AAERpRolcSEpaJAH7cCRhNzn8bMdZKZcqjc')

chat_id = -1001951718196

chat_members = ['alexandertruewig', 'dxnteee', 'mtmrphosis ', 'b0lLb', 'Flamethrower1337 ', 'destinyfire', 'speedgainer', \
    'barakudboy', 'mex13370', 'galyapypsik', 'l0l0l0l0l0l00l', 'young_sakura', 'haikoro', 'mightyskrudge', 'girlsarethesame',\
    'cloudy1337']

noplay_members = ['' for i in range(tgbot.get_chat_member_count(chat_id))]
play_members = chat_members
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
    players = a2s.players(addrs_server)
    mssg = ''
    for i in range(0, a2s.info(addrs_server).player_count):
        mssg = mssg + '<b><i>' + str(players[i].name) + '</i></b>' + ' | Kills: ' + str(players[i].score) + '\n'
    return mssg

@tgbot.message_handler(commands=['online', 'now'])
def online_now(message):
    msgg = ''
    msgg = get_server_info() + '\n'
    
    if(a2s.info(addrs_server).player_count > 0):
        msgg = '\n' + msgg + '\n' \
            + '=-----------------------=' + '\n' \
            + get_players() + '\n' \
            + '=-----------------------=' + '\n'
        
    tgbot.send_message(chat_id, msgg, parse_mode='html')
    
@tgbot.message_handler(commands=['all'])
def all(message):
    msgg = ''
    for i in range(len(play_members)):
        if play_members[i] != '': 
            msgg += '\n' + '@' + play_members[i]
    # tgbot.send_message(chat_id, msgg)
    print(msgg)
    
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
    
def main():
    tgbot.polling(none_stop=True)
        
if __name__ == '__main__':
    main()
    
# import waitress
# from app import create_app

# if __name__ == "__main__":
#     waitress.serve(app=create_app(), port=2525)