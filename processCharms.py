#!/usr/bin/python

import os
import sys
from fnmatch import fnmatch
from subprocess import call
import requests
import json

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
		"memcached": "lp:~charmers/charms/precise/memcached/trunk",
		"rabbitmqserver": "lp:~charmers/charms/precise/rabbitmq-server/trunk",
		"solr": "lp:~charmers/charms/precise/solr/trunk",
		"tomcat7": "lp:~charmers/charms/precise/tomcat7/trunk",
		"websphere-libery": "lp:~ibm-demo/charms/trusty/websphere-liberty/trunk",
		"wordpress": "lp:~charmers/charms/precise/wordpress/trunk",
		"zookeeper": "lp:~charmers/charms/precise/zookeeper/trunk"
	}
	return repos

def getAllBundleRepositories():
	bundles = {
		"mediawikibundle": "lp:~charmers/charms/bundles/mediawiki-scalable/bundle"
	}
	return bundles

def processCharmRepository(name, repository):
	cmd = "./getCharmAndZip.sh " + name + " " + repository
	print cmd
	ret_code = call(cmd, shell=True)	

def processBundleRepository(name, repository):
        cmd = "./getBundleAndZip.sh " + name + " " + repository
        print cmd
        ret_code = call(cmd, shell=True)

def printHelp():
	print "missing parameters"
	print "usage: " + sys.argv[0] + " ACTION + CS_URL"
	print "- ACTION: download, upload, checkSize"
	print "- CS_URL is the URL:PORT of the charmstore"

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
	params.append("precise/"+name)

	charmZip = zipName.replace("./", "")
	params.append(charmZip)

	return params

def uploadCharm(zipName, CS_URL):
	params = prepareNameForZip(zipName)
	print params
	cmd = "./upload-charm.sh "+CS_URL+" "+params[0]+" "+params[1]
	print cmd
	ret_code = call(cmd, shell=True)


def uploadAllCharms(zips, CS_URL):
	for zipName in zips:
		#print "uploading"+zipName
		uploadCharm(zipName, CS_URL)

def getCharmArchiveSize(charmName, CS_URL):
	r = requests.get("http://"+CS_URL+"/v4/~csqaprocess"+charmName+"/meta/archive-size")
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
		else:
			print "unknown command"
			printHelp()

if __name__ == '__main__': 
	main()
