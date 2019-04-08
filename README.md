# Deprecated Project
* Functionality is now built into fragforce.org at https://fragforce.org/static/ffsite/overlays/scrolltext.html
* Code at https://github.com/fragforce/fragforce.org/blob/dev/ffsite/static/ffsite/overlays/scrolltext.html

# FragStreamsourcer
Local web and go frontend to show neat Fragforce things on streams without having to deal with an outside service.  

# Quick Start (All OSes)
1) download everything
2) rename FSSConfig.yml.sample to FSSConfig.yml (or create your own yml config based on that file)
3) double click the fragstats executable for your OS to start the service

# About adding sources
to add any widget from this collection, simply create a new Browser Source widget, and set the url to point to the locally hosted HTML using port 8000 (by default).

Ex: for the scrolling text widget, set the url to "http://localhost:8000/scrollingtext.html"

For information on the individual overlays and what they are, check out index.htm once you've started the server.

# TODOS
Honestly there are lots.  Check the individual html files for some info, or create issues here if you find a missing item you want to request!
