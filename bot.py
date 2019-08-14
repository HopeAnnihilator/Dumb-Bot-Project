import discord
from discord.ext import commands
import time
import threading

global holons
global opted_out


client = commands.Bot(command_prefix = '')
opted_out = open("opted_out.txt").read().splitlines()
holons = []

            
@client.event
async def on_ready():
    print('The Damned Thing Actually Started')
    timer = threading.Timer(30, save)
    timer.start()


def save():
    with open('opted_out.txt', 'w') as yay:
        for user in opted_out:
            if user:
                yay.write(user + '\n')
    print('opted_out saved')
    timer = threading.Timer(30, save)
    timer.start()
    

@client.event
async def on_message(message):

    if message.content.startswith('Hocus Pocus'): #this is where commands are run to bot by beginning message with 'Hocus Pocus'
        if "opt out" in message.content: 
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
            if str(message.author.id) == admin_user_id and 'opted_out' in message.content:
                if opted_out:
                    await message.channel.send('**opted_out:**')
                    await message.channel.send(opted_out)
                else:
                    await message.channel.send('***Either your list is fucked or nobody opted out!***')
            if str(message.author.id) == user_id and 'holons' in message.content:
                if holons:
                    await message.channel.send('**holons:**')
                    await message.channel.send(holons)
                else:
                    await message.channel.send('***Either your list is fucked or no holons currently exist***')
                
        
            
    elif str(message.author.id) not in opted_out and str(message.author.id) != bot_id:
        wordlist = open(time.strftime("wordlist-%Y-%m-%d"), "a")
        if message.mentions:
            da_message = (message.content)
            for mention in message.raw_mentions:
                da_message = da_message.replace(str(mention), '').replace('<@>','')
            if da_message:
                wordlist.write(da_message + " ")
                print(da_message)
        else:
            wordlist.write(message.clean_content + " ")
            print(message.content)  

admin_user_id = ''
bot_id = ''
token = ''
client.run(token)
