import discord
from discord.ext import commands
import time

client = commands.Bot(command_prefix = '')
opted_out = open("opted_out.txt").read().splitlines()
holons = []

@client.event
async def on_ready():
    print('The Damned Thing Actually Started')

            
@client.event
async def on_message(message):
    global opted_out
    global holons
    if message.content.startswith('Hocus Pocus'): #this is where commands are run to bot by beginning message with 'Hocus Pocus'
        if "opt out" in message.content: 
            if str(message.author.id) in opted_out:
                await message.channel.send(str(message.author) + ' is already opted out')
            else: #gotta love this shitshow
                opted_out = open("opted_out.txt", 'a')
                opted_out.write(str(message.author.id) + '\n')
                opted_out.close()
                opted_out = open("opted_out.txt").read().splitlines()
                await message.channel.send(str(message.author) + ' is now opted out')
                
        elif "opt in" in message.content:
            if str(message.author.id) in opted_out: 
                with open('opted_out.txt', 'w') as f: #gotta love this shitshow
                    for line in opted_out:
                        if line != str(message.author.id) and line:
                            f.write(line + '\n')
                opted_out = open("opted_out.txt").read().splitlines()
                await message.channel.send(str(message.author) + ' is now opted in')
            else:
                await message.channel.send(str(message.author) + ' is not opted out')
                
        elif "list" in message.content: #this is made so that multiple lists can be output at once
            if str(message.author.id) == user_id and 'opted_out' in message.content:
                if opted_out:
                    await message.channel.send('**opted_out:**')
                    await message.channel.send(opted_out)
                else:
                    await message.channel.send('**Either your list is fucked or nobody opted out!**')
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

user_id = ''
bot_id = ''
token = ''
client.run(token)
