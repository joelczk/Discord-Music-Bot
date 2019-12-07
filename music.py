import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import get
import asyncio
import requests
import re
from bs4 import BeautifulSoup as bs
import youtube_dl
import os

client = commands.Bot(command_prefix = '.')

song_list = {}

def get_title(link):
    content = requests.get(link)
    soup = bs(content.content, "html.parser")
    title = soup.find("span", attrs={"class": "watch-title"}).text.strip()
    return title

def check_url(url):
    link = "https://www.youtube.com/results?search_query=" + str(url)
    page = requests.get(link).content
    data = str(page).split(' ')
    item = 'href="/watch?'
    vids = [line.replace('href="', 'youtube.com') for line in data if item in line]
    if len(vids) == 0:
        return False
    else:
        return vids[0][:-1]

@client.event
async def on_ready():
    print('Bot is online')

@client.command(pass_context = True)
async def join(ctx):
    global voice
    try: 
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild = ctx.guild)
        print(channel)
        if voice and voice.is_connected():
            await voice.move_to(channel)
            print('Bot moved channel')
            print(ctx.message.author)
        else:
            await channel.connect()
            print('Bot Connected')
            print(ctx.message.author)
    except:
        await ctx.send("No users in channel")

@client.command(pass_context = True)
async def leave(ctx):
    global voice
    try:
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected():
            print('Bot disconnected')
            await voice.disconnect()
        else:
            await ctx.send("Bot is not in any channel")
    except:
        await ctx.send("Bot is not in any channel")

@client.command(pass_context = True)
async def queue(ctx):
    channel = ctx.message.guild
    url = ctx.message.content
    url = url[7:]
    link = check_url(url)
    if link != False:
        link = "HTTPS://" + str(check_url(url))
        content = requests.get(link)
        soup = bs(content.content, "html.parser")
        title = soup.find("span", attrs={"class": "watch-title"}).text.strip()
        if channel.id not in song_list.keys():
            store = [url]
            song_list[channel.id] = store
        else:
            store = song_list[channel.id]
            store.append(url)
            song_list[channel.id] = store
        send_message = "`" + str(title) + "` is queued."
        await ctx.send(send_message)
    else:
        ctx.send("Search query cannot be found. Please Try again!")

@client.command(pass_context = True)
async def play(ctx):
    channel = ctx.message.guild
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    voice = get(client.voice_clients, guild = ctx.guild)
    while True:
        try:
            if voice and voice.is_connected():
                # print(song_list)
                # print('There are users in VC')
                if voice.is_playing():
                    await ctx.send ('Bot is currently playing music', delete_after = 1)
                else:
                    url = "https://" + str(check_url(song_list[channel.id][0]))
                    await ctx.send('Preparing to play `'+ str(get_title(url)) + '` ...')
                    rename = (str(song_list[channel.id][0]) + ".mp3").replace(" ","")
                    song_there = os.path.isfile(rename)
                    if song_there == False:
                        print('song_there loop')
                        await ctx.send(str(get_title(url)) + " not found on OS", delete_after = 5)
                        print('message sent')
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                            print('song downloaded')
                            for file in os.listdir("./"):
                                if file.endswith(".mp3"):
                                    name = file
                                    try:
                                        os.rename(file, rename)
                                    except:
                                        continue
                            send_message2 = ("`" + str(get_title(url)) + "` downloaded. Waiting to play song...")
                            await ctx.send(send_message2)
                    else:
                        await ctx.send(str(get_title(url)) + " found on OS", delete_after = 5)
                    player = discord.FFmpegPCMAudio(rename)
                    voice.play(player)
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 1.00
                    song_list[channel.id].pop(0)
            else:
                print('There are no users in VC')
                break
        except:
            await ctx.send('There are no more songs queued')
            break

@client.command(pass_context = True)
async def stop(ctx):
    channel = ctx.message.guild
    song_list[channel.id] = []
    voice = get(client.voice_clients, guild = ctx.guild)
    voice.stop()
    print('Bot stopped')
    
@client.command(pass_context = True)
async def skip(ctx):
    channel = ctx.message.guild
    song = song_list[channel.id][0]
    song_list[channel.id].pop(0)
    send_message = "`" + song + "`" + " skipped"
    await ctx.send(send_message)
    # print(song_list)

@client.command(pass_context = True)
async def clear(ctx):
    channel = ctx.message.guild
    song_list[channel.id] = []
    await ctx.send("Queue purged")
    return song_list

@client.command(pass_context = True)
async def list(ctx):
    channel = ctx.message.guild
    count = 1
    try:
        embed = discord.Embed(color=0x00ff00)
        for i in song_list[channel.id]:
            link = "HTTPS://" + str(check_url(i))
            song_name = get_title(link)
            print_query = 'Song ' + str(count)
            embed.add_field(name = print_query, value =song_name, inline=False)
            count += 1
    except:
        embed = discord.Embed(description="There are currently no songs being queued", color=0x00ff00)
    await ctx.send(embed=embed)

client.run("<token>")
