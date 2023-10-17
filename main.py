# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
import os
from datetime import datetime
import pytz
from discord import Embed
from discord.ext import commands
import threading
import requests
import time
import requesta
import sqlite3
from PIL import Image
import urllib.request
import json
from discord import File

bot = commands.Bot(command_prefix='$')

discordIDs = puuids = {'plumyum':'367844010271834123','Taevion':'362297684746305536','blum':'387381219605610498','Silly Baby':'416608736950485003','bruce':'496813919000723467','HenHen':'484911988003045378','NUT Hunter40':'481656296165212171','mwe':'388513313736228864','Icydog':'105037070187130880','TrendUniverse':'332209831866007554','Zammey':'328971640618876950','JojoTheDodo':'298139332986798080','Scoxy':'384422291301335051'}
@bot.event
async def on_ready():
    print('We have logged in as {0.user} #BONER ACTIVE'.format(bot))

#ecos leaderboard
@bot.command()
async def ecos(ctx):
  players = {}
  #connect to SQL db
  conn = sqlite3.connect('user_data.db')
  cursor = conn.cursor()
  #fetch username and eco kills
  cursor.execute('SELECT * FROM users')
  #fetch rows from dataset
  rows = cursor.fetchall()
  #insert into player dict
  for row in rows:
    players[row[1]] = row[3]
  #sort player dict
  players = dict(sorted(players.items(), key=lambda item: item[1], reverse=True))
  #switch out player username into discord IDs
  embed_dict = {discordIDs[key]: value for key,value in players.items()}
  #grab current time
  utc_now = datetime.now(pytz.utc)
  central_time = utc_now.astimezone(pytz.timezone('US/Central'))
  formatted_time = central_time.strftime('%I:%M %p')
  # Format the sorted data into the desired string format
  leaderboard_entries = [f"**{index + 1}.** <@{key}>: `{value}`" for index, (key, value) in enumerate(embed_dict.items())]
# Join the leaderboard entries together
  leaderboard_string = "\n".join(leaderboard_entries)

  #creates last eco image
  last_eco = requesta.most_recent_eco
  urllib.request.urlretrieve(last_eco[2], 'gun1.png')
  image1 = Image.open('gun1.png')
  image1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
  urllib.request.urlretrieve(last_eco[5], 'gun2.png')
  image2 = Image.open('gun2.png')
  versus = Image.open('versus.png')
  image1 = image1.resize((400, 300))
  image2 = image2.resize((400, 300))
  merged_image = Image.new('RGB',(2*image1.size[0]+versus.size[0], image1.size[1]), (250,250,250))
  merged_image.paste(image1,(0,0))
  merged_image.paste(image2,(image1.size[0]+versus.size[0],0))
  merged_image.paste(versus,(int((image1.size[0])),0))
  merged_image.save('merged_image.jpg', 'JPEG')
  file = discord.File('merged_image.jpg')
  
  embed = discord.Embed(
        title="💸ECO KILLS LEADERBOARD💸",
        description=f'{leaderboard_string}\n\n**Most Recent ECO Kill** ☠️\n`{last_eco[0]}` killed `{last_eco[3]}` with a `{last_eco[1]}`.\n`{last_eco[3]}` had a `{last_eco[4]}`',
        color=11421116
    )
  embed.set_footer(text=f"guagua3 | {formatted_time}", icon_url="https://i.ibb.co/4NNdYjL/3c28066bb4f2855bddd254d8516aa149.jpg")
  embed.set_image(url='attachment://merged_image.jpg')
  conn.close()
  await ctx.send(embed=embed, file=file)

@bot.command()
async def bob(ctx):
  #list of dicts for each player and stas
  player_list_bob = []
  #connect to SQL db
  conn = sqlite3.connect('user_data.db')
  cursor = conn.cursor()
  #fetch username and eco kills
  cursor.execute('SELECT * FROM users')
  #fetch rows from dataset
  rows = cursor.fetchall()
  for row in rows:
    #create dict for each player
    user_dict = {
      "Username:":row[1],
      "Headshots:":row[4],
      "Bodyshots:":row[5],
      "Legshots:":row[6],
      "Total":(row[4]+row[5]+row[6]),
      #roounding to nearest int, can change if needed
      "Percentage": int((row[5]/(row[4]+row[5]+row[6]))*100)
    }
    player_list_bob.append(user_dict)
  #sort from highest percentage to lowest
  sorted_bob = sorted(player_list_bob, key=lambda x: x['Percentage'], reverse=True)
  #nested loop to switch out usernames into discord IDs for mebed
  for player in sorted_bob:
    username = player['Username:']
    if username in discordIDs:
      player['Username:'] = discordIDs[username]
    #leaderboard text for all players
  leaderboard_entries = [f"**{index + 1}.** <@{item['Username:']}>: `{item['Percentage']}%`" for index, item in enumerate(sorted_bob)]
  leaderboard_string = "\n".join(leaderboard_entries)
  #body shot bob stats
  bob = sorted_bob[0]
  bob_stats = f"**Body Shot BOB**: <@{bob['Username:']}>\n**Headshots**: `{bob['Headshots:']}`\n**Bodyshots**: `{bob['Bodyshots:']}`\n**Legshots**: `{bob['Legshots:']}`"
  #grab current time
  utc_now = datetime.now(pytz.utc)
  central_time = utc_now.astimezone(pytz.timezone('US/Central'))
  formatted_time = central_time.strftime('%I:%M %p')
  embed = discord.Embed(
        title="🧍‍♂️BODY SHOT BOB LEADERBOARD🧍‍♂️",
        description=f"{leaderboard_string}\n\n{bob_stats}",
        color=11421116
    )
  embed.set_footer(text=f"guagua3 | {formatted_time}", icon_url="https://i.ibb.co/4NNdYjL/3c28066bb4f2855bddd254d8516aa149.jpg")
  conn.close()
  await ctx.send(embed=embed)


@bot.command()
async def last_ecos(ctx):
  user_tag = ctx.message.content
  hashtag = user_tag.index('.')
  name = user_tag[11:hashtag]
  tag = user_tag[hashtag+1:]
  puuid = requesta.get_puuid(name,tag)

  player_stats = requesta.fetch_data_from_api(puuid)
  if player_stats is None:
    player_stats = requesta.get_recent_game_stats(requesta.get_by_puuid('id', puuid))

  eco_kills = player_stats[0]['ecoKills']
    
  
  embed = discord.Embed(
        title="ECOS FROM LAST GAME",
        description=f"💰**{name}** got `{eco_kills}` ecos last game💰",
        color=11421116
    )
  icon_url=("https://i.ibb.co/4NNdYjL/3c28066bb4f2855bddd254d8516aa149.jpg")
   #grab current time
  utc_now = datetime.now(pytz.utc)
  central_time = utc_now.astimezone(pytz.timezone('US/Central'))
  formatted_time = central_time.strftime('%I:%M %p')
  embed.set_footer(text=f"guagua3 | {formatted_time}", icon_url="https://i.ibb.co/4NNdYjL/3c28066bb4f2855bddd254d8516aa149.jpg")
  if int(eco_kills) > 10:
      file_path = f"{eco_kills}.png"
  else:
    file_path = f"{eco_kills}.jpg"
  
  file = File(file_path, filename=file_path)
  embed.set_image(url=f"attachment://{file_path}")
  await ctx.send(embed=embed, file=file)



  

"""
@bot.command()
async def lasteco(ctx):
  last_eco = requesta.most_recent_eco
  urllib.request.urlretrieve(last_eco[2], 'gun1.png')
  image1 = Image.open('gun1.png')
  image1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
  urllib.request.urlretrieve(last_eco[5], 'gun2.png')
  image2 = Image.open('gun2.png')
  versus = Image.open('versus.png')
  image1 = image1.resize((400, 300))
  image2 = image2.resize((400, 300))
  merged_image = Image.new('RGB',(2*image1.size[0]+versus.size[0], image1.size[1]), (250,250,250))
  merged_image.paste(image1,(0,0))
  merged_image.paste(image2,(image1.size[0]+versus.size[0],0))
  merged_image.paste(versus,(int((image1.size[0])),0))
  merged_image.save('merged_image.jpg', 'JPEG')
  file = discord.File('merged_image.jpg')
  
  embed = discord.Embed(
        title="LATEST ECO",
        description=f'**{last_eco[0]}** killed **{last_eco[3]}** with a **{last_eco[1]}**. **{last_eco[3]}** had a **{last_eco[4]}**',
        color=11421116
    )
  embed.set_image(url='attachment://merged_image.jpg')
  await ctx.send(embed=embed, file=file)

"""

try:
    bot.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
