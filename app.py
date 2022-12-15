import os
import discord
from discord.utils import get
from dotenv import load_dotenv
import random
import re
import time

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
    # if the message is by the bot break the function - this stops endless loops
    if message.author == client.user:
        return
    # sends spongebob-text message
    if len(message.content) > 35:
        response = [x for x in message.content]
        for i in range(len(message.content)):
            upper_lower = random.randint(0,1)
            if upper_lower == 1:
                response[i] = message.content[i]
            elif upper_lower == 0:
                response[i] = message.content[i].upper()
        
        await message.channel.send(''.join(response))
    # looks for /d and number to roll random number generator
    if '/d' in message.content:
        num = re.search('(?<=\/d).[0-9]+', message.content)
        if num.group(0).isnumeric():
            string = f'{str(random.randrange(1,int(num.group(0))+1))}'

            await message.channel.send(string)
        else: 
            await message.channel.send('thats not a number, try again')  
    # responds with emoji   
    if 'wz' in message.content.lower() or 'warzone' in message.content.lower() or 'cod' in message.content.lower() or 'call of duty' in message.content.lower():
        emoji = client.get_emoji(955552719379251300)
        await message.add_reaction(emoji)
    elif 'shot' in message.content.lower():
        emoji = client.get_emoji(951262317482479667)
        await message.add_reaction(emoji)

client.run(TOKEN)