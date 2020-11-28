import json
import os
import discord
import constant
from discord.ext import commands

with open('config.json') as serverInfo:
    serverData = json.load(serverInfo)

client = discord.Client()

@client.event
async def on_ready():
    channel = client.get_channel(serverData['channel_id'])
    await channel.send('hello from bot')
    print(channel)

client.run(serverData['bot_token'])