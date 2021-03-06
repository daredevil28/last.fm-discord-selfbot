#libraries related to last.fm
try:
	from urllib.request import urlopen
	import urllib.error
except ImportError:
	from urllib2 import urlopen
from xml.dom import minidom
import sys
import argparse
import codecs
import threading
import json
#libraries related to discord
import discord
import asyncio

#JSON
data = json.load(open('token.json'))

#discord token
TOKEN = data["token"]
#api key for last.fm
api_key = data["api"]

whitelist = data["whitelist"]

#The last.fm stuff happens under here

#Putting defaults and shortcuts at top of the file
defaults = dict()
defaults['prepend'] = ''
defaults['append'] = ''
defaults['delay'] = 5
args = dict()
prefix = ">>lfm" #prefix can be changed to anything
bot = discord.Client()
local_copy = 'nowplaying.xml'

def get_parameters():
	parser = argparse.ArgumentParser(prog='LastfmSelfbot',description="description")
	parser.add_argument('username')
	parser.add_argument('-p', '--prepend', dest = 'prepend', default = defaults['prepend'])
	parser.add_argument('-a', '--append', dest = 'append', default = defaults['append'])
	parser.add_argument('-d', '--delay', dest = 'delay', default = defaults['delay'], type=int)
	
	input = parser.parse_args()
	
	args['username'] = input.username
	args['prepend'] = input.prepend
	args['append'] = input.append
	if input.delay < 1:
		print('#'*20)
		print('Delay must be AT LEAST 1 second, setting to 1 second')
		print('#'*20)
		args['delay'] = 1
	else:
		args['delay'] = input.delay

#Download xml as binary
def download(url,filename):
	try:
		instream=urlopen(url)
		outfile=open(filename,'wb')
		for chunk in instream:
			outfile.write(chunk)
		instream.close()
		outfile.close()
	except Exception as e:
		print(e)

#print out information about the bot.
@bot.event
async def on_ready():
	print(bot.user.id)
	print(bot.user)
	print('Line them up, knock em down! last.fm bot ready for action.')
	await bot.change_presence(status=discord.Status.invisible)
	print('--------')
	asyncio.run_coroutine_threadsafe(lastfm_coro(),bot.loop)
	#Launch the cororoutine in discord.py's event loop. It's probably a lot safer than the jenky ass thread way

enabled = True #set to True if you want the last.fm script to start at boot, set to false if you want to manually start the script
alive = True # Coro's life

async def lastfm_coro():
	global enabled,alive
	print('Starting with arguments:')
	print('Username: ' + args['username'])
	print('Prepended text: ' + args['prepend'])
	print('Appended text: ' + args['append'])
	print('Delay between updates: ' + str(args['delay']))
	print('--------')
	
	#Keeping track of the last track that was playing using track url
	last_track = ''
	track_data = ""
	
	feed_url = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
		+ args['username'] + '&api_key=' + api_key + '&limit=1')

	while alive:
		if enabled:
			download(feed_url,local_copy)
			
			data=open(local_copy,'rb')
			xmldoc=minidom.parse(data)
			data.close()
			
			item = xmldoc.getElementsByTagName('track')[0]
			
			#If track playing
			if (item.attributes.item(0)):
			
				current_track = item.getElementsByTagName('url')[0].firstChild.data
				
				#If track changed
				if (current_track != last_track):
				
					last_track = current_track
					artist = item.getElementsByTagName('artist')[0].firstChild.data
					track = item.getElementsByTagName('name')[0].firstChild.data
					
					track_data= args['prepend'] + track + ' by ' + artist + args['append']
					
					print(track_data)
					await bot.change_presence(game=discord.Game(name=track_data))
					
					#Else, nothing playing
			else:
				#If only just stopped playing
				if(last_track != ''):
					
					last_track = ''
					track_data = ''
					await bot.change_presence()
		#Need to wait at least 1 second for another API call
		await asyncio.sleep(args['delay'])

#actual bot stuff happens under here	
	
@bot.event
async def on_message(message):
	global enabled,alive
	if message.server.id in whitelist: #check in the whitelist list if the server ID is in it
		if message.author == bot.user: #checks if the message is from the user
			if message.content.startswith(prefix + ' on'):
				if not enabled: #is it already enabled?
					enabled = True
					print("Enabled")
					await bot.change_presence(status=discord.Status.online)
					await bot.delete_message(message)
				else: 
					await bot.edit_message(message, new_content="last.fm bot is already enabled!")
					await asyncio.sleep(1)
					await bot.delete_message(message)

			elif message.content.startswith(prefix + ' off'):
				if enabled:
					enabled = False
					await bot.change_presence(status=discord.Status.invisible)
					print("Disabled")
					await bot.delete_message(message)
				else:
					await bot.edit_message(message, new_content="last.fm bot is already disabled!")
					await asyncio.sleep(1)
					await bot.delete_message(message)

			elif message.content.startswith(prefix + ' shutdown'):
				await bot.delete_message(message)
				await bot.change_presence(status=discord.Status.invisible)
				alive = False
				await asyncio.sleep(args['delay']*2)
				await bot.logout()
				await bot.close()

if __name__=="__main__":
	get_parameters()
	bot.run(TOKEN, bot=False)
