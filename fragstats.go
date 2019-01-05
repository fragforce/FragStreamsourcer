package main

//Fragforce Stats grabber/Web Server combo, hacked together by Barry Weisshaar.
//Address all feature enhancements/hate over my kindergarten Go to me.

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

/*
Configuration structure is as follows:
Port is the port number for the web server to launch on
ParticipantID is the user's DonorDrive ID
TeamID is the user's Donordrive Team ID
UpdateInterval is how often the app attempts to refresh json data, in seconds.  30-60 seconds should be plenty.
WebDir is the web root you want served, aka htdocs, aka wwwdata, etc.
VideoPath is the path to videos under your WebDir.
*/
type Configuration struct {
	Port           string
	ParticipantID  string
	TeamID         string
	UpdateInterval int
	WebDir         string
	VideoPath      string
}

var configuration Configuration

//Generic "Bail and error" function.
func check(e error) {
	if e != nil {
		log.Fatal(e)
	}
}

//This is a goroutine that spawns off to update stats
func pollstats() {

	tdjson := "https://www.extra-life.org/api/teams/" + configuration.TeamID + "/donations"
	udjson := "https://www.extra-life.org/api/participants/" + configuration.ParticipantID + "/donations"
	topjson := "https://www.extra-life.org/api/participants/" + configuration.ParticipantID + "/donations?orderBy=amount%20desc&limit=10"
	lastjson := "https://www.extra-life.org/api/participants/" + configuration.ParticipantID + "/donations?orderBy=createdDateUTC%20desc&limit=5"

	var netClient = &http.Client{
		//The default timeout is way too long, hopefully it won't come to this.
		Timeout: time.Second * 10,
	}

	for {
		log.Print("Polling DonorDrive API for updated stats")

		resp, err := netClient.Get(tdjson)
		check(err)
		defer resp.Body.Close()
		body, err := ioutil.ReadAll(resp.Body)
		log.Print("Updating team total. Read ", len(body), " bytes from server.")
		err = ioutil.WriteFile(configuration.WebDir+"/teamdonations.json", body, 0644)

		resp, err = netClient.Get(udjson)
		check(err)
		defer resp.Body.Close()
		body, err = ioutil.ReadAll(resp.Body)
		log.Print("Updating user total. Read ", len(body), " bytes from server.")
		err = ioutil.WriteFile(configuration.WebDir+"/persondonations.json", body, 0644)

		resp, err = netClient.Get(topjson)
		check(err)
		defer resp.Body.Close()
		body, err = ioutil.ReadAll(resp.Body)
		log.Print("Updating top 10 personal donations. Read ", len(body), " bytes from server.")
		err = ioutil.WriteFile(configuration.WebDir+"/top10personal.json", body, 0644)

		resp, err = netClient.Get(lastjson)
		check(err)
		defer resp.Body.Close()
		body, err = ioutil.ReadAll(resp.Body)
		log.Print("Updating last 5 personal donations. Read ", len(body), " bytes from server.")
		err = ioutil.WriteFile(configuration.WebDir+"/last5personal.json", body, 0644)

		//Sleep it off between requests
		time.Sleep(time.Second * time.Duration(configuration.UpdateInterval))
	}
}

func main() {
	log.Print("Server is starting up...")
	var videos []string
	configfilename := "config.json"

	//Read config file
	dat, err := ioutil.ReadFile(configfilename)
	check(err)

	//Load config
	json.Unmarshal(dat, &configuration)

	//Get list of videos
	files, err := ioutil.ReadDir(configuration.WebDir + "/" + configuration.VideoPath)
	check(err)

	for _, file := range files {
		if file.Mode().IsRegular() {
			videos = append(videos, configuration.VideoPath+"/"+file.Name())
		}
	}
	videosjson, err := json.Marshal(videos)
	ioutil.WriteFile(configuration.WebDir+"/videolist.json", videosjson, 0644)

	go pollstats()
	//Launch Go's HTTP Server
	log.Print("and Awaaayyyyy we go!")
	log.Fatal(http.ListenAndServe(":"+configuration.Port, http.FileServer(http.Dir(configuration.WebDir))))

}
