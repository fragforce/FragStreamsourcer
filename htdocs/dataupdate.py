########
# dataupdate.py - Python script for updating data to local server from EL's API
# 	this script should be running continuously in the background during streaming,
#	as it updates local json records from Extra Life's API.  
#	@dev - Ben Gray
########

#	TODO -- graceful exit for script after ctrl-c, rather than slamming it and waiting till the next update

import urllib.request
import threading

# teamID - the ID of the team you are watching
teamID = '38642'

# personID - the ID of your campaign page
personID = '298779'

# pingSeconds - Number of seconds between server pings
pingSeconds = 60.0

def getdata():

	# Start thread for next call first
	threading.Timer(pingSeconds, getdata).start()

	# Ping api of whole team's donations and write to teamdonations.json
	response = urllib.request.urlopen('https://www.extra-life.org/api/teams/' + teamID + '/donations')
	html = response.read()
	fout = open("teamdonations.json","w")
	fout.write(html.decode("utf-8"))
	fout.close()
	
	# Ping api of individual user and write to persondonations.json
	response2 = urllib.request.urlopen('https://www.extra-life.org/api/participants/' + personID + '/donations')
	html2 = response2.read()
	fout2 = open("persondonations.json","w")
	fout2.write(html2.decode("utf-8"))
	fout2.close()
	
	# Write teminal out line
	print("Data Updated")
	
getdata()