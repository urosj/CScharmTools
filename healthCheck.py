import sys
import requests
import json
import random
import datetime
from StringIO import StringIO

output = {}

def panic_on_error(msg):
	print msg
	output["error"] = msg
	print_output()
	sys.exit()

def print_output():
	io = StringIO()
	json.dump(output, io)

	f = open(sys.argv[1], "a+")
	f.write(io.getvalue())
	f.close()

	f = open(sys.argv[1]+".csv", "a+")
	o = output["start"]
	o = o + "," + output["duration"]
	if "error" in output:
		o = o + "," + output["error"]
	o = o + "\n"

	f.write(o)
	f.close()


server_url = "https://api.jujucharms.com/charmstore/v4"
#server_url = "http://localhost:8080/v4"

start_time = datetime.datetime.now()
print "check started at " + unicode(start_time)
output["start"] = unicode(start_time)

print "checking elasticsearch"
#search_url = server_url + "/search?text=&limit=2000&include=stats"
search_url = server_url + "/search?text=&include=charm-metadata&include=bundle-metadata&include=extra-info/bzr-owner&include=extra-info/commercial&include=bundle-unit-count&include=stats&limit=400&autocomplete=1&sort=-downloads,owner&owner="
ids = []
r = requests.get(search_url)
if (r.status_code == 200):
	search_data = json.loads(r.content)
	results = search_data[u'Results']
	for r in results:
		ids.append(r[u'Id'].replace("cs:", ""))
	if len(ids) == 0:
		panic_on_error("no results in elasticearch")
else:
	panic_on_error("elasticsearch is down")

rand_id = random.choice(ids)
print rand_id

print "checking blobstore"
manifest_url = server_url + "/" + rand_id + "/meta/manifest"
print manifest_url
r = requests.get(manifest_url)
if (r.status_code == 200):
	files = []
	data = json.loads(r.content)
	for d in data:
		files.append(d[u'Name'])
	file_name = random.choice(files)
	print file_name
	file_url = server_url + "/" + rand_id + "/archive/" + file_name
	fr = requests.get(file_url)
	if (fr.status_code != 200):
		panic_on_error("blobstore error: could not access file " + file_url)
else:
	panic_on_error("blobstore error: could not access manifest for " + rand_id)

print "checking entity collection"
exp_ids_url = server_url + "/" + rand_id + "/expand-id"
print exp_ids_url
r = requests.get(exp_ids_url)
if (r.status_code == 200):
	data = json.loads(r.content)
	exp_ids = []
	for d in data:
		exp_ids.append(d[u'Id'].replace("cs:", ""))
	if len(exp_ids) == 0:
		panic_on_error("entity collection error: expand is empty for " + rand_id)
	rand_exp_id = random.choice(exp_ids)
	# check bzr owner 
	rand_exp_id_url = server_url + "/" + rand_exp_id + "/meta/extra-info/bzr-owner"
	rd = requests.get(rand_exp_id_url)
	if (r.status_code != 200):
		panic_on_error("entity error: no bzr-owner info for " + rand_exp_id_url)
	if (len(r.content) == 0):
		panic_on_error("entity error: bzr-owne is empty for " + rand_exp_id_url)
else:
	panic_on_error("entity collection error: expand failed for " + rand_id)

print "checking base entity collection"
promulgated_url = server_url + "/" + rand_id + "/meta/promulgated"
print promulgated_url
r = requests.get(promulgated_url)
if (r.status_code != 200):
	panic_on_error("baseEntity error: could not retrieve information about promulgation")

print "check ok"
end_time = datetime.datetime.now()
duration = end_time - start_time

print "check finished at " + unicode(end_time)
print "duration " + unicode(duration)

output["end"] = unicode(end_time)
output["duration"] = unicode(duration)

print_output()
