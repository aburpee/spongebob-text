import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(command_prefix = 'sponge', intents = discord.Intents.all())

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.content) > 35:
        response = [x for x in message.content]
        # message = message.content.split()
        
        for i in range(len(message.content)):
            upper_lower = random.randint(0,1)
            if upper_lower == 1:
                response[i] = message.content[i]
            elif upper_lower == 0:
                response[i] = message.content[i].upper()
        
        await message.channel.send(''.join(response))
            
            



client.run(TOKEN)