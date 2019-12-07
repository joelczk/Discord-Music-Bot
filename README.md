# Discord-Music-Bot
**Description**\
Music bot for discord users\
**Requirements**\
Do not that the song bot can only play songs with English title\
Do note that user has to install FFPMEG for this code to work together with youtube-dl\
Do note that user has to generate his/her token from discord developer portal\
File locations where songs are stored can be changed via the following command:\
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
**Acknowledgements**\
The songs are streamed from ©Youtube
