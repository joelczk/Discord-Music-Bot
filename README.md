# Discord Music Bot

## Introduction
This is a bot created to play songs on the `Discord` platform. Click [here](https://discord.com/) if you would like to learn more about `Discord`.

## Bot Requirements:
1. FFMPEG
2. Discord Token
3. Python3

## Setting up the bot:
### FFMPEG
1. Download the `FFMPEG` file from [here](https://ffmpeg.org/download.html#build-windows), according to your operating system.
2. Unzip the file to your desired location. 

### Discord Token
Before creating a discord token, please make sure that you have a working discord account. 

If you do not have a `DISCORD` account, you can sign up for one [here](https://discord.com/register).

Follow the guide [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) on how to set up your own discord token.

## Running the bot
1. Git clone the bot into your desired directory
```console
joelczk@home/<directory-name>:~$ git clone https://github.com/joelczk/Discord-Music-Bot
```
2. Install required python modules
```console
joelczk@home/<directory-name>:~$ pip install > requirements.txt
```
3. Run the bot
```console
joelczk@home/<directory-name>:~$ python3 music.py
```

4. The music bot is now ready to be deployed in `Discord`

Alternatively, the bot could be hosted on other sites and the bots can be run anytime.

## Bot Commands
- `.join`: Calls for the bot to enter the voice channel that the user is in
- `.leave`: Calls for bot to leave channel that it is currently in
- `.queue`: Queue songs for the bot to play
- `.play` : Calls for the bot to start playing songs
- `.skip` : Calls for the bot to skip the next song in its queued list
- `.clear` : Clears all queued songs
- `.list` : List all queued songs
- `.stop`: Stops songs from playing and clears the queued list

## Sources
All songs that are used are streamed and downloaded from `Youtube`. All credits and acknowledgements for the songs goes to the song creators.
