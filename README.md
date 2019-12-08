# Discord Music Bot
**Description**\
Music bot for discord users\
Coded in Python
Libraries used can be found in requirements.txt

**Requirements**\
Do not that the song bot can only play songs with English title\
Do note that user has to install FFPMEG for this code to work together with youtube-dl\
Do note that user has to generate his/her token from discord developer portal\
File locations where songs are stored can be changed via the following command:
```
os.path.isfile() --> os.path.isfile(<path>)
```
**Commands**
```
.join: Calls for bot to enter the voice channel that user is in
.leave: Calls for bot to leave channel that it is in
.queue: Queue songs for bot to play
.play: Calls for bot to start playing song
.skip: skip the next song in list
.clear: clear all queued songs
.list: List all the songs on queue
.stop : Stop song from playing and clears the queue
```

**Installation**
```
RUN git clone https://github.com/joelczk/Discord-Music-Bot.git in your terminal
NOTE: Make sure that yur FFMPEG environment variables is set up properly
```
**Acknowledgements**\
The songs are streamed and donwloaded from ©Youtube
