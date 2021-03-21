import json
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


settings = {'prefix':'command prefix for bot: ',
            'bot_key':'discord bot secret key: ',
            'bot_id':'discord bots id:',
            'deposit_channel':'deposit channels id (You need to make a deposit channe for users to deposit KR): ',
            'withdraw_channel':'withdraw channels id (You need to make a withdraw channel for users to withdraw KR): ',
            'command_channel':'command channels id (Your servers general bot command channel): ',
            'coinflip_channel':'coinflip channels id (You server needs a coinflip channel for users to perform coinflips): ',
            'coinflip_log_channel':'coinflip log channel (Logs all coinflip actions, make sure this channel is visible to the bot): ',
            'dealer_role_id':'dealer role ID (This role lets people add/remove KR from peoples accounts. give it wisely): '}

try:
    current = json.load(open('config.json'))
except:
    current = {}

for setting in settings:
    if setting not in current:
        current[setting] = None

def reset_settings():
    global current
    for setting in settings:
        current[setting] = None
    j = json.dumps(current)
    with open("config.json", "w") as f:
        f.write(j)
        f.close()

while True:
    for setting in settings:
        print(f'{setting}: {current[setting]}')
    print('Type RESET to reset settings')
    print('Press ENTER to exit')
    setting_choice = input('Type the corresponding name of the setting to edit it\n')

    if setting_choice == '':
        break
    if setting_choice == 'RESET':
        reset_settings()


    setting_value = input(settings[setting_choice])
    current[setting_choice] = setting_value
    j = json.dumps(current)
    with open("config.json", "w") as f:
        f.write(j)
        f.close()



