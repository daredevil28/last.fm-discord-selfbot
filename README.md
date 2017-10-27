# last.fm-discord-selfbot
### A discord selfbot that changes your now playing status to the current song you are playing on last.fm

#### In order to use this bot you need the following library:

`python3 -m pip install -U discord.py`

You also need to change the token and the last.fm api key in the code before using it:

```python
#discord token
TOKEN = 'THETOKEN'
about = "Puts the content of a text file as the now playing"
#api key for last.fm
api_key = 'lastfmapi'
```
You can get a lastfm api key here: https://www.last.fm/api/account/create

You also require to whitelist a server where you can use the bot in. I have done this because I am in 44 servers and the selfbot used 30% of my CPU constantly.

```python
'''server whitelist where various servers
can be put in. The bot wil only check in
these servers for messages
format: whitelist = ["serverID1", serverID2", ETC]
'''
whitelist = ["paste a server ID in here"]
```

Run the bot using `python3 "LastfmSelfbot.py" [your discord username] (-p prepend) (-a append) (-d delay)`

You can use the following commands:

```
>>lfm on #turns on last.fm
>>lfm off #turns off last.fm
>>lfm shutdown #Shuts the bot down
```

This bot uses the NowPlayingToTxt code: https://github.com/alecksphillips/NowPlayingToTxt

Big thanks to my friend DJPadbit who helped me a ton with ~copy pasting~ coding this.
