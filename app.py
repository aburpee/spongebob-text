import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(command_prefix = 'sponge', intents = discord.Intents.all())

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')
client.run(TOKEN)