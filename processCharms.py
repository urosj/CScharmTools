#!/usr/bin/python

import os
import sys
from subprocess import call
import requests
import json
import random
import bisect
import threading

def getAllCharmRepositories():
	repos = {
		"mediawiki": "lp:~charmers/charms/precise/mediawiki/trunk",
		"haproxy": "lp:~charmers/charms/precise/haproxy/trunk",
		"mysql": "lp:~charmers/charms/precise/mysql/trunk",
		"apache2": "lp:~charmers/charms/precise/apache2/trunk",
		"cassandra": "lp:~charmers/charms/precise/cassandra/trunk",
		"elasticsearch": "lp:~charmers/charms/precise/elasticsearch/trunk",
		"drupal6": "lp:~lynxman/charms/precise/drupal6/trunk",
		"jujugui": "lp:~juju-gui-charmers/charms/precise/juju-gui/trunk",
		#"memcached": "lp:~charmers/charms/precise/memcached/trunk",
		#"rabbitmqserver": "lp:~charmers/charms/precise/rabbitmq-server/trunk",
		#"solr": "lp:~charmers/charms/precise/solr/trunk",
		#"tomcat7": "lp:~charmers/charms/precise/tomcat7/trunk",
		##"websphere-libery": "lp:~ibm-demo/charms/trusty/websphere-liberty/trunk",
		#"wordpress": "lp:~charmers/charms/precise/wordpress/trunk",
		#"zookeeper": "lp:~charmers/charms/precise/zookeeper/trunk"
	}
	return repos

def getCharmProbabilities():
	probs = {
		"mediawiki.zip": 10,
		"haproxy.zip": 10,
		"mysql.zip": 10,
		"apache2.zip": 10,
		"cassandra.zip": 10,
		"elasticsearch.zip": 3,
		"drupal6.zip": 10,
		#"jujugui.zip": 3,
		"memcached.zip": 10,
		"rabbitmqserver.zip": 10,
		"solr.zip": 10,
		"tomcat7.zip": 10,
		#"websphere-libery.zip": 1,
		"wordpress.zip": 10,
		"zookeeper.zip": 10
	}
	return probs

def getAllBundleRepositories():
	bundles = {
		#"mediawikibundle": "lp:~charmers/charms/bundles/mediawiki-scalable/bundle"
	}
	return bundles

def processCharmRepository(name, repository):
	cmd = "./getCharmAndZip.sh " + name + " " + repository
	print cmd
	ret_code = call(cmd, shell=True)	
	return ret_code

def processBundleRepository(name, repository):
        cmd = "./getBundleAndZip.sh " + name + " " + repository
        print cmd
        ret_code = call(cmd, shell=True)
        return ret_code

def printHelp():
	print "missing parameters"
	print "usage: " + sys.argv[0] + " ACTION + CS_URL"
	print "- ACTION: download, upload, checkSize, "
	print " 	uploadmonkey, downloadmonkey, revisionmonkey"
	print "- CS_URL is the URL:PORT of the charmstore"
	print "- revisionmonkey needs two additional parameters: minRevision and maxRevision"

def getAllCharmZips():
	zips = []
	for root, dirs, files in os.walk("./charmZips"):
		for file in files:
			if file.endswith(".zip"):
				fileName = os.path.join(root, file)
				zips.append(fileName)
	return zips

def prepareNameForZip(zipName):
	params = []
	name = zipName.replace("./charmZips/", "")
	name = name.replace(".zip", "")
	params.append("~csqaprocess1/precise/"+name)

	charmZip = zipName.replace("./", "")
	params.append(charmZip)

	return params

def uploadCharm(zipName, CS_URL):
	params = prepareNameForZip(zipName)
	print params
	cmd = "./upload-charm.sh "+CS_URL+" "+params[0]+" "+params[1]
	print cmd
	ret_code = call(cmd, shell=True)
	return ret_code


def uploadAllCharms(zips, CS_URL):
	for zipName in zips:
		#print "uploading"+zipName
		uploadCharm(zipName, CS_URL)

def getCharmArchiveSize(charmName, CS_URL):
	url = "http://"+CS_URL+"/v4/"+charmName+"/meta/archive-size"
	#print url
	r = requests.get(url)
	if(r.status_code == 200):
		json_data = json.loads(r.content)
		size = json_data[u'Size']
		return size
	return -1

def getFileSize(zipName):
	return os.path.getsize(zipName)

def compareZipAndUploadedCharmSize(zips, CS_URL):
	for zipFile in zips:
		params = prepareNameForZip(zipFile)
		print "processing " + params[0]
		sizeOnDisk = getFileSize(zipFile)
		sizeInCharmstore = getCharmArchiveSize(params[0], CS_URL)
		if sizeOnDisk == sizeInCharmstore:
			print params[0] + " is properly uploaded"
		else:
			print params[0] + " size on disk is " + sizeOnDisk + " in store is " + sizeInCharmstore

def prepareProbabilityDistribution(probs):
	sum = 0
	itemPoints = []
	itemNames = []
	items = probs.keys()
	for i in items:
		sum += probs[i]
		itemPoints.append(sum)
		itemNames.append(i)
	return itemPoints, itemNames

def getRandomItem(breakpoints, items):
    score = random.random() * breakpoints[-1]
    i = bisect.bisect(breakpoints, score)
    return items[i]

class UploadThread(threading.Thread):
	def __init__(self, zipName, CS_URL):
		super(UploadThread, self).__init__()
		self.zipName = zipName
		self.csUrl = CS_URL

	def run(self):
		print "starting upload task for ", self.zipName
		uploadCharm(self.zipName, self.csUrl)
		print "done uploading task for ", self.zipName

class RevisionUploadThread(threading.Thread):
	def __init__(self, zipName, CS_URL):
		super(RevisionUploadThread, self).__init__()
		self.zipName = zipName
		self.csUrl = CS_URL

	def run(self):
		print "zipname: ", self.zipName[0]
		cmd = "./upload-revision.sh "+self.csUrl+" "+self.zipName[1]+" "+self.zipName[0]
		print cmd
		ret_code = call(cmd, shell=True)


def uploadMonkeyTasks(zips, CS_URL):
	print "starting upload monkeys"
	probs = getCharmProbabilities()
	#print probs
	probsDistribution, items = prepareProbabilityDistribution(probs)
	#print probsDistribution
	#print items

	for _ in range(10):
		selected = []
		threads = []
		for _ in range(20):
			# select a charm
			print "select random"
			randZip = getRandomItem(probsDistribution, items)
			selected.append(randZip)
			print "selected: ", randZip
			#print "complete set: ", selected

			thread = UploadThread(randZip, CS_URL)
			threads.append(thread)

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

def generateCharmRevisions(zipPrefix, minR, maxR):
	revisions = []
	for r in range(minR, maxR):
		cmd = "./makeCharmRevision.sh " + zipPrefix + " " + str(r) + " " + str((r / 2)*2)
		print cmd
		ret_code = call(cmd, shell=True)
		revisions.append(zipPrefix+"-"+str(r))
	return revisions

def uploadCharmNameFromRevName(revName):
	splits = revName.split("-")
	name = "~csqaprocess1/precise/"+splits[0]
	return name

def generateRevisionsForCharms(minR, maxR, CS_URL):
	repos = getAllCharmRepositories()
	charms = repos.keys()
	revisions = []
	for charm in charms:
		cr = generateCharmRevisions(charm, minR, maxR)
		for r in cr:
			revisions.append(r)
	#print revisions
	zips = []
	for rev in revisions:
		zipname = "./charmRevisions/"+rev+".zip"
		name = uploadCharmNameFromRevName(rev)
		zips.append([zipname, name])
	print zips

	threads = []

	# TODO: needs to be broken in chunks
	for charm in zips:
		thread = RevisionUploadThread(charm, CS_URL)
		threads.append(thread)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()



class DownloadThread(threading.Thread):
	def __init__(self, charmName, CS_URL, fileName):
			super(DownloadThread, self).__init__()
			self.charmName = charmName
			self.csURL = CS_URL
			self.fileName = fileName

	def run(self):
		print "starting download task for ", self.charmName
		cmd = "http get "+self.csURL+"/v4/"+self.charmName+"/archive > "+self.fileName
		print cmd
		ret_code = call(cmd, shell=True)
		return ret_code		

def checkDownloadSize(downloadCounter, CS_URL):
	errorCount = 0
	errorList = []
	for charm in downloadCounter.keys():
		print charm
		size = getCharmArchiveSize(charm+"-0", CS_URL)
		print size
		last = downloadCounter[charm]
		zipFileBase = charm.replace("~csqaprocess1/precise/", "")
		zipFileBase = "./temp/" + zipFileBase
		for i in range(last):
			zipFile = zipFileBase + "-" + str(i+1) + ".zip"
			sizeOnDisk = getFileSize(zipFile)
			if sizeOnDisk != size:
				print zipFile + " is not properly downloaded"
				errorCount = errorCount + 1
				errorList.append(zipFile)
	return errorCount, errorList


def downloadMonkeyTasks(CS_URL):
	probs = getCharmProbabilities()
	probsDistribution, items = prepareProbabilityDistribution(probs)

	downloadCounter = {}

	for _ in range(20):
		tasks = []
		for _ in range(50):
			randZip = getRandomItem(probsDistribution, items)
			charmName = randZip.replace(".zip", "")
			charmName = "~csqaprocess1/precise/"+charmName
			#print charmName
			if not charmName in downloadCounter:
				downloadCounter[charmName] = 1
			else:
				downloadCounter[charmName] += 1
			taskParams = [charmName, "./temp/"+randZip.replace(".zip","")+"-"+str(downloadCounter[charmName])+".zip"]
			tasks.append(taskParams)

		#print tasks
		#print downloadCounter

		threads = []
		for task in tasks:
			thread = DownloadThread(task[0], CS_URL, task[1])
			threads.append(thread)

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

	errorCount, errorList = checkDownloadSize(downloadCounter, CS_URL)
	print errorList
	print "num errors while downloading: " + str(errorCount)


def getAllLatestRevisionsIDs(CS_URL, limit):
	qall = "http://" + CS_URL + "/v4/search?text=&limit=" + str(limit)
	print "getting conntent with: ", qall
	r = requests.get(qall)
	json_data = json.loads(r.content)
	results = json_data["Results"]
	ids = []
	for res in results:
		csid = res["Id"]
		csid = csid.replace("cs:", "")
		ids.append(csid)
	return ids

def getAllRevisionsForId(csid, CS_URL):
	expUrl = "http://" + CS_URL + "/v4/" + csid + "/expand-id"
	r = requests.get(expUrl)
	json_data = json.loads(r.content)
	ids = []
	for res in json_data:
		csid = res["Id"]
		csid = csid.replace("cs:", "")
		ids.append(csid)
	return ids

def getArchiveForId(csid, CS_URL):
	archUrl = "http://" + CS_URL + "/v4/" + csid + "/archive"
	r = requests.get(archUrl)
	conlen = r.headers["content-length"]
	status = r.status_code
	if status == 200:
		sizeUrl = "http://" + CS_URL + "/v4/" + csid + "/meta/archive-size"
		rs = requests.get(sizeUrl)
		json_data = json.loads(rs.content)
		size = json_data["Size"]
		if int(size) != int(conlen):
			print "size ", size, " vs conlen ", conlen
			return 1
		return 0
	return -1

def validateStoreUploads(CS_URL):
	print "validating uploaded content"
	#first, get all the latest revisions of charms and bundles
	ids = getAllLatestRevisionsIDs(CS_URL, 100000)

	errorArchSizeIds = []
	missingArchIds = []
	#for each charm, use expand id to get all possible revisions
	for csid in ids:
		newids = getAllRevisionsForId(csid, CS_URL)
		#check what get on archive returns 
		for expid in newids:
			print "Checking ", expid
			res = getArchiveForId(expid, CS_URL)
			if res == -1:
				print "ERROR: missing archive in ID: ", expid
				missingArchIds.append(expid)
			elif res == 1:
				print "ERROR: archive not complete for ID: ", expid
				errorArchSizeIds.append(expid)

	print "Charms with errors sizes:"
	for errid in errorArchSizeIds:
		print errid

	print "Charms with missing archives: "
	for errid in missingArchIds:
		print errid

def main():
	if len(sys.argv) < 2:
		printHelp()
		sys.exit()

	ACTION = sys.argv[1]

	if ACTION == "download":
		repos =  getAllCharmRepositories()
		for name, repo in repos.items():
			print "processing " + name + " in " + repo
			processCharmRepository(name, repo)
		bundles = getAllBundleRepositories()
                for name, repo in bundles.items():
                        print "processing " + name + " in " + repo
                        processBundleRepository(name, repo)
	else:
		if len(sys.argv) < 3:
			printHelp()
			sys.exit()

		CS_URL = sys.argv[2] 

		zips = getAllCharmZips()

		if ACTION == "upload":
			uploadAllCharms(zips, CS_URL)
		elif ACTION == "checkSize":
			compareZipAndUploadedCharmSize(zips, CS_URL)
		elif ACTION == "uploadmonkey":
			uploadMonkeyTasks(zips, CS_URL)
		elif ACTION == "downloadmonkey":
			downloadMonkeyTasks(CS_URL)
		elif ACTION == "revisionmonkey":
			if len(sys.argv) < 5:
				printHelp()
				sys.exit()
			generateRevisionsForCharms(int(sys.argv[3]), int(sys.argv[4]), CS_URL)
		elif ACTION == "verifycontent":
			validateStoreUploads(CS_URL)
		else:
			print "unknown command"
			printHelp()

if __name__ == '__main__': 
	main()
