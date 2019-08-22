#!/usr/bin/env python3
#cron this shit

import discord
import numpy as np
from wordcloud import WordCloud
from PIL import Image
import time
from discord.ext import commands

wordcloud_channel_id = 613861363797721108
client = commands.Bot(command_prefix = '')


@client.event
async def on_ready():
    await generate_wordcloud()

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
    exit()


token = 'NjEwNjk4OTg5NjQxNDAwMzMw.XVNMaw.gjCNUJhN9ZAaEnxJQGcCRfsyla4'
client.run(token)
