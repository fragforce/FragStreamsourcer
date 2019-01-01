########
# dataupdate.py - Python script for updating data to local server from EL's API
# 	this script should be running continuously in the background during streaming,
#	as it updates local json records from Extra Life's API.  
#	@dev - Ben Gray
########

#	TODO -- graceful exit for script after ctrl-c, rather than slamming it and waiting till the next update

### Imports

import urllib.request
import threading
import json
from os import listdir
from os.path import isfile, join

### Variables

# teamID - the ID of the team you are watching
teamID = '38642'

# personID - the ID of your campaign page
personID = '298779'

# pingSeconds - Number of seconds between server pings
pingSeconds = 60.0

# videoPath - folder where videos are kept
videoPath = 'videos'

### Support Methods

# refresh All Data that needs regular refreshing
def getdata():

	# Start thread for next call first
	threading.Timer(pingSeconds, getdata).start()

	# Ping api of whole team's donations and write to teamdonations.json
	response = urllib.request.urlopen('https://www.extra-life.org/api/teams/' + teamID + '/donations')
	html = response.read()
	fout = open("teamdonations.json","w", encoding="utf-8")
	fout.write(html.decode("utf-8"))
	fout.close()
	
	# Ping api of individual user and write to persondonations.json
	response2 = urllib.request.urlopen('https://www.extra-life.org/api/participants/' + personID + '/donations')
	html2 = response2.read()
	fout2 = open("persondonations.json","w", encoding="utf-8")
	fout2.write(html2.decode("utf-8"))
	fout2.close()

	# Ping api for top 10 individual donations
	response3 = urllib.request.urlopen('http://extra-life.org/api/participants/' + personID + '/donations?orderBy=amount%20desc&limit=10')
	html3 = response3.read()
	fout3 = open("top10personal.json","w", encoding="utf-8")
	fout3.write(html3.decode("utf-8"))
	fout3.close()

	# Write teminal out line
	print("Data Updated")

### On Run Script Section

# pull folder list and push data to json, only needs to happen once
videoList = [videoPath + '/' + f for f in listdir(videoPath) if isfile(join(videoPath, f))]
pathoutput = json.dumps(videoList)
pout = open("videolist.json","w",encoding="utf-8")
pout.write(pathoutput)
pout.close()

# call data pull method for first time to set schedule
getdata()