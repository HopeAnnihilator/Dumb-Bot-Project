#!/usr/bin/env python3

import discord
from discord.ext import commands
import time
import threading
import re
import json
import numpy as np
from wordcloud import WordCloud
from PIL import Image
import datetime
from datetime import datetime as dt
from datetime import timedelta
from threading import Timer

global toolong
global strjoin
global helpinfo
global stream
global stream_up
global customemoji
global change
global roles
global words

client = commands.Bot(command_prefix = '')
helpinfo = open('help.txt').read().splitlines()

toolong = 1950
needsupdate = 0
roles = {}

strjoin = '\n'.join
stream = discord.Streaming(name = "Hocus Pocus...", url = 'https://www.twitch.tv/holonnetwork')

customemoji  = re.compile(r"<:\S*?:\d{18}>")
command = 'Hocus Pocus'


with open ('data.json') as the_mob:
    data = json.load(the_mob)

@client.event
async def on_ready():
    print('The Damned Thing Actually Started')
    timer = threading.Timer(300, save)
    timer.start()
    await role_check()
    await client.change_presence(status = discord.Status.online, activity = stream)


async def generate_wordcloud():
    words = open(time.strftime("messages/%Y-%m-%d")).read().splitlines()
    with Image.open ('dcdarknet.png') as dcdn:
        mask = np.array(dcdn)
    word_cloud = WordCloud(width = 750, height = 769, background_color = 'black', mask = mask)
    word_cloud.generate(str(words))
    cloud_file = time.strftime("wordclouds/%Y-%m-%d.png")
    word_cloud.to_file(cloud_file)
    await share_cloud(cloud_file)

async def share_cloud(cloud_file):
    channel = client.get_channel(wordcloud_channel_id)
    await channel.send(file = discord.File(cloud_file))

async def role_check():
    guild = client.get_guild(target_server_id)
    for item in data['holons']:
        if item and str(item) not in str(guild.roles):
            await guild.create_role(name = item)


def save():
    with open('data.json') as test:
        global needsupdate
        updated = json.load(test)
        if str(updated) != str(data) or needsupdate == 13:
            with open('data.json', 'w') as yay:
                json.dump(data, yay, indent = 4)
                print('Data updated')
                needsupdate = 0
        else:
            needsupdate = needsupdate + 1
    timer = threading.Timer(300, save)
    timer.start()

@client.event
async def on_message(message):
    if message.content.lower().startswith(command.lower()): 
        if "help" in message.content:
            await message.channel.send(strjoin(helpinfo))
                                       
        elif "opt out" in message.content: 
            if str(message.author.id) in data['opted_out']:
                await message.channel.send(str(message.author) + ' is already opted out')
            else:
                data['opted_out'].append(str(message.author.id))
                await message.channel.send(str(message.author) + ' is now opted out')
                
        elif "opt in" in message.content:
            if str(message.author.id) in data['opted_out']: 
                data['opted_out'].remove(str(message.author.id))
                await message.channel.send(str(message.author) + ' is now opted in')
            else:
                await message.channel.send(str(message.author) + ' is not opted out')
                
        elif "list" in message.content:
            request = 0

            for item in data:
                if item in message.content:
                    await message.channel.send('***' + item + '***')
                    await message.channel.send(strjoin(data[item]))
                    request = request + 1
                    break
                elif item in message.content and not data:
                    await message.channel.send(item + ' is empty')
                    request = request + 1
                    break
            if request == 0:
                await message.channel.send('**Dumb Bot can not find that list, here is a list of items that can be listed!**')
                await message.channel.send(strjoin(data))
        elif "iama" in message.content:
            messageinfo = message.content.split()
            if messageinfo[3] in data['holons']:
                for role in message.guild.roles:
                    if role.name == messageinfo[3]:
                        await message.author.add_roles(role)
            else:
                await message.channel.send('That role can not currently be assigned, try ```Hocus Pocus list holons``` for a list of assignable roles')
        elif "wordcloud" in message.content and message.author.id == admin_user_id:
            await generate_wordcloud()
    elif str(message.author.id) not in data['opted_out'] and message.author.id != bot_id:
        if str(message.channel.name) == '🍆':
                await message.add_reaction('\U0001F346')
                print('eggplant')
        wordlist = open(time.strftime("messages/%Y-%m-%d"), "a")
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
                da_message = re.sub(r"<:\S*?:\d{18}>", '', da_message)
            if da_message:
                wordlist.write(da_message + " ")
        else:
            wordlist.write(message.content + " ") 


wordcloud_channel_id = 
target_server_id = 
admin_user_id = 
bot_id = 
token = 
client.run(token)
