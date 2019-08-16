import discord
from discord.ext import commands
import time
import threading
import re

global holons
global opted_out
global toolong
global strjoin
global helpinfo
global stream
global customemoji
global lists

client = commands.Bot(command_prefix = '')
opted_out = open("opted_out.txt").read().splitlines()
holons = open('holons.txt').read().splitlines()
helpinfo = open('help.txt').read().splitlines()
lists = open('lists.txt').read().splitlines()
toolong = 1950
strjoin = '\n'.join
stream = discord.Streaming(name = "Hocus Pocus...", url = 'https://www.twitch.tv/holonnetwork')
customemoji  = re.compile("<:.*:\d{18}>")

            
@client.event
async def on_ready():
    print('The Damned Thing Actually Started')
    timer = threading.Timer(300, save)
    timer.start()
    await client.change_presence(status = discord.Status.online, activity = stream)


def save():
    with open('opted_out.txt', 'w') as yay:
        for user in opted_out:
            if user:
                yay.write(user + '\n')
    with open('holons.txt', 'w') as yay:
        for holon in holons:
            if holon:
                yay.write(holon + '\n')
    print('Files updated')
    timer = threading.Timer(300, save)
    timer.start()
    

@client.event
async def on_message(message):
    if message.content.startswith('Hocus Pocus'): #this is where commands are run to bot by beginning message with 'Hocus Pocus'
        if "help" in message.content:
            await message.channel.send(strjoin(helpinfo))
                                       
        elif "opt out" in message.content: 
            if str(message.author.id) in opted_out:
                await message.channel.send(str(message.author) + ' is already opted out')
            else:
                opted_out.append(str(message.author.id))
                await message.channel.send(str(message.author) + ' is now opted out')
                
        elif "opt in" in message.content:
            if str(message.author.id) in opted_out: 
                opted_out.remove(str(message.author.id))
                await message.channel.send(str(message.author) + ' is now opted in')
            else:
                await message.channel.send(str(message.author) + ' is not opted out')
                
        elif "list" in message.content: #this is made so that multiple lists can be output at once
            request = 0
            for item in lists:
                if item in message.content and item:
                    await message.channel.send('***' + item + '***')
                    await message.channel.send(strjoin(eval(item)))
                    request = request + 1
                    break
                elif item in message.content and not item:
                    await message.channel.send(item + ' is empty')
                    request = request + 1
                    break
            if request == 0:
                await message.channel.send('Dumb Bot can not find that list')
                
        
    elif str(message.author.id) not in opted_out and str(message.author.id) != bot_id:
        wordlist = open(time.strftime("wordlist-%Y-%m-%d"), "a")
        if message.mentions or message.role_mentions or message.channel_mentions or message.mention_everyone or customemoji.search(message.content):
            da_message = (message.content)
            for mention in message.raw_mentions:
                da_message = da_message.replace(str(mention), '').replace('<@>','')
            for mention in message.raw_channel_mentions:
                da_message = da_message.replace(str(mention), '').replace('<#>','')
            for mention in message.raw_role_mentions:
                da_message = da_message.replace(str(mention), '').replace('<@&>','')
            if message.mention_everyone:
                da_message = da_message.replace(str('@everyone'), '').replace(str('@here'), '')
            if customemoji.search(message.content):
                da_message = re.sub(r"<:.*:\d{18}>", '', da_message)
            if da_message:
                wordlist.write(da_message + " ")
                print(da_message)
                print('message was editted')
        else:
            wordlist.write(message.clean_content + " ")
            print(message.content)  

admin_user_id = ''
bot_id = ''
token = ''
client.run(token)
