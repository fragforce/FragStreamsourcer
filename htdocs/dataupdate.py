import urllib.request
import threading

# teamID - the ID of the team you are watching
teamID = '38642'

# personID - the ID of your campaign page
personID = '298779'

# pingSeconds - Number of seconds between server pings
pingSeconds = 60.0

def getdata():
	threading.Timer(pingSeconds, getdata).start()
	response = urllib.request.urlopen('https://www.extra-life.org/api/teams/' + teamID + '/donations')
	html = response.read()
	fout = open("teamdonations.json","w")
	fout.write(html.decode("utf-8"))
	fout.close()
	
	response2 = urllib.request.urlopen('https://www.extra-life.org/api/participants/' + personID + '/donations')
	html2 = response2.read()
	fout2 = open("persondonations.json","w")
	fout2.write(html2.decode("utf-8"))
	fout2.close()
	
	print("server PING")
	
getdata()