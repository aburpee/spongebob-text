import os
import discord
from discord.utils import get
from discord.ext import commands, tasks
from dotenv import load_dotenv
import random
import re
import time
import requests

load_dotenv()
OMDB_KEY = os.getenv('OMDB_KEY')
STREAMING_KEY = os.getenv('STREAMING_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mov"] 

client = discord.Client(command_prefix = 'sponge', intents = discord.Intents.all())

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')
@bot.command(name='shit')
async def random_image(ctx, source_channel_id = 815464674404990988, source_server_id = 735280881664655410, target_server_id = 718995069847470141, target_channel_id = 718995070316970046):
    try:
        
        source_server = discord.utils.get(bot.guilds, id = source_server_id)
        target_server = discord.utils.get(bot.guilds, id = target_server_id)
        source_channel = discord.utils.get(source_server.channels, id = source_channel_id)
        target_channel = discord.utils.get(target_server.channels, id = target_channel_id)

        messages = []
        async for message in source_channel.history(limit = 500):
            messages.append(message)

        image_messages = [message for message in messages if message.attachments]

        if image_messages:

            random_message = random.choice(image_messages)

            attachment = random_message.attachments[0]
            image_url = attachment.url
            sender = random_message.author

            await target_channel.send(image_url)
            await target_channel.send(f'courtesy of {sender}')
        else:
            await ctx.send('no image found')
    except discord.NotFound:
        await ctx.send('source image not found')
            
@bot.command(name = 'problem')
async def ask(ctx):
    await ctx.send('https://tenor.com/view/whattheproblemis-martin-lawrence-nationalsecurity-gif-27064298')

@bot.command(name = 'movie')
async def ask(ctx):
     await ctx.send('What movie would you like to watch?')

     def check(message):
         return message.author == ctx.author and message.channel == ctx.channel

     try:
         user_response = await bot.wait_for('message', check=check, timeout=10.0)
         await ctx.send(f'you want to watch: {user_response.content}')
         response = requests.get(f'http://www.omdbapi.com/?t={user_response.content}&apikey={OMDB_KEY}')
         imdb_id = response.json()['imdbID']
         imdb_title = response.json()['Title']
         imdb_plot = response.json()['Plot']
         url = "https://streaming-availability.p.rapidapi.com/v2/get/basic"

         querystring = {"country":"us",f"imdb_id":f"{imdb_id}","output_language":"en"}

         headers = {
             "X-RapidAPI-Key": "e145409a39mshf509ba14a206131p1acb3ejsnaeb0f27c7eb9",
             "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
         }

         response = requests.get(url, headers=headers, params=querystring)

         example_json = response.json()

         streaming_info = example_json['result']['streamingInfo']['us']

         for i in streaming_info:
             quality = streaming_info[i][0]['quality']
             type_of_stream = streaming_info[i][0]['type']
             link = streaming_info[i][0]['link']
        
             await ctx.send(f'you can {type_of_stream} {imdb_title} on {i} in {quality} \n here is your link: {link}' )


         await ctx.send(f' \n \n the plot is: {imdb_plot}')

     except asyncio.TimeoutError:
         await ctx.send('timeout. you did not send a response quick enough')

bot.run(TOKEN)


# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(f'{client.user} has connected to the following guild:\n'
#           f'{guild.name}(id: {guild.id})')

# @client.event
# async def on_message(message):
#     # if the message is by the bot break the function - this stops endless loops
#     if message.author == client.user:
#         return
#     # sends spongebob-text message
#     if len(message.content) > 35:
#         response = [x for x in message.content]
#         for i in range(len(message.content)):
#             upper_lower = random.randint(0,1)
#             if upper_lower == 1:
#                 response[i] = message.content[i]
#             elif upper_lower == 0:
#                 response[i] = message.content[i].upper()
        
#         await message.channel.send(''.join(response))
#     # looks for /d and number to roll random number generator
#     if '/d' in message.content:
#         num = re.search('(?<=\/d).[0-9]+', message.content)
#         if num.group(0).isnumeric():
#             string = f'{str(random.randrange(1,int(num.group(0))+1))}'

#             await message.channel.send(string)
#         else: 
#             await message.channel.send('thats not a number, try again')  
#     # responds with emoji   
#     if 'wz' in message.content.lower() or 'warzone' in message.content.lower() or 'cod' in message.content.lower() or 'call of duty' in message.content.lower():
#         emoji = client.get_emoji(955552719379251300)
#         await message.add_reaction(emoji)
#     elif 'shot' in message.content.lower():
#         emoji = client.get_emoji(951262317482479667)
#         await message.add_reaction(emoji)
#     for attachment in message.attachments:
#         if any(attachment.filename.lower().endswith(image) for image in image_types):
#             await attachment.save(f'attachments/{attachment.filename}')



# client.run(TOKEN)