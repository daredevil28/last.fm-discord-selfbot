# last.fm-discord-selfbot
### A discord selfbot that changes your now playing status to the current song you are playing on last.fm

#### In order to use this bot you need the following library:

`python3 -m pip install -U discord.py`

Rename `token.json.new` to `token.json`

Open the .json in your favourite text editor

```json
{
	"token": "YOUR_TOKEN", #Your user token
	"whitelist": "YOUR_SERVER_ID", #ID of the server you want to use the selfbot in
	"api": "YOUR_API" #last.fm api
}
```

You can get a lastfm api key here: https://www.last.fm/api/account/create

You also require to whitelist a server where you can use the bot in. I have done this because I am in 44 servers and the selfbot used 30% of my CPU constantly.

Run the bot using `python3 LastfmSelfbot.py [your last.fm username] (-p prepend) (-a append) (-d delay)`

You can use the following commands:

```
>>lfm on #turns on last.fm and sets you online
>>lfm off #turns off last.fm and sets you offline
>>lfm shutdown #Shuts the bot down
```

This bot uses the NowPlayingToTxt code: https://github.com/alecksphillips/NowPlayingToTxt

Big thanks to my friend DJPadbit who helped me a ton with ~copy pasting~ coding this.
