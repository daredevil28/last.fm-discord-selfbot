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

Run the bot using `python3 "lastfm selfbot.py" [your discord username] (-p prepend) (-a append) (-d delay)`
