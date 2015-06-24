import sys
import requests
import json
import random
import datetime
import pymongo

server_name = "jujucharms"
server_url = "https://api.jujucharms.com/charmstore/v4"
#server_url = "http://juju.mycomiclife.net/charmstore/v4"

def panic_on_error(msg):
	print msg
	sys.exit()

print "checking elasticsearch"
search_url = server_url + "/search?text=&limit=4000&include=stats"
stats = []
daystamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
r = requests.get(search_url)
if (r.status_code == 200):
	search_data = json.loads(r.content)
	results = search_data[u'Results']
	for r in results:
		r[u'day'] = daystamp
		stats.append(r)
	if len(stats) == 0:
		panic_on_error("no results in elasticearch")
else:
	panic_on_error("elasticsearch is down")

print "dumping to file", server_name+"_"+daystamp+".json"
f = open(server_name+"_"+daystamp+".json", 'w')
f.write(json.dumps(stats, indent=4, sort_keys=True))
f.close()
