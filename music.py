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
player_info = {}


def play_song(channel,voice,file_name):
    try:
        player = discord.FFmpegPCMAudio(file_name)
        voice.play(player)
        voice.source.volume = 1.00
        song_list[channel.id].pop(0)
    except:
        print('Song reached end of list')

def get_title(link):
    content = requests.get(link)
    soup = bs(content.content, "html.parser")
    title = soup.find("span", attrs={"class": "watch-title"}).text.strip()
    return title

def download_file(rename, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    song_there = os.path.isfile(rename)
    if song_there == False:
        print('Song not found on OS')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print('Song downloaded')
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    try:
                        os.rename(file,rename)
                        print('File successfully renamed')
                    except:
                        print('File renaming failed for file: ' + str(name))
    else:
        print('Song found on OS')

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
    search_query = ctx.message.content
    search_query = search_query[7:]
    print(search_query)
    url = check_url(search_query)
    url = "https://www." + str(url)
    print(url)
    title = get_title(url)
    title = title + ".mp3"
    print(title)
    download_file(title,url)
    try:
        check = song_list[channel.id]
        song_list[channel.id].append(title)
    except:
        song_list[channel.id] = [title]
    message = "`" + str(title) + "` has been queued"
    await ctx.send(message)

@client.command(pass_context = True)
async def play(ctx):
    channel = ctx.message.guild
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await ctx.send('Bot in channel!Preparing to play music', delete_after = 2)
        title = ''
        while True:
            if voice.is_playing():
                await ctx.send("Bot is currently playing `" + title + "`", delete_after = 2)
            else:
                print('Bot is not playing any music')
                title = str(song_list[channel.id][0])
                play_song(channel,voice,song_list[channel.id][0])
                print('title is: ', title)
                print(song_list)
    else:
        await ctx.send('Bot not in Channel. Please allow bot to join channel...', delete_after = 2)

@client.command(pass_context = True)
async def stop(ctx):
    channel = ctx.message.guild
    song_list[channel.id] = []
    voice = get(client.voice_clients, guild = ctx.guild)
    voice.stop()
    await ctx.send('Bot has been stopped', delete_after = 2)
    
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
        if song_list[channel.id] is None:
            embed = discord.Embed(description="There are currently no songs being queued", color=0x00ff00)
        else:
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

client.run(<token>)
