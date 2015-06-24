import sys
import requests
import json
import random
import datetime


def cont2map(content):
	ids = {}
	for elm in content:
		ids[elm[u'Id']] = elm
	return ids

start_cont = json.load(open(sys.argv[1]))
end_cont = open(sys.argv[2])

stats2 = cont2map( json.load(end_cont) )

diffs = []
for data in start_cont:
	url = data[u'Id']
	if stats2.has_key(url):
		data2 = stats2[url]
		res = {}

		archdl1 = data[u'Meta'][u'stats'][u'ArchiveDownload']
		archdl2 = data2[u'Meta'][u'stats'][u'ArchiveDownload']

		arch_dl = {}
		arch_dl[u'Day'] = archdl2[u'Day'] - archdl1[u'Day']
		arch_dl[u'Week'] = archdl2[u'Week'] - archdl1[u'Week']
		arch_dl[u'Month'] = archdl2[u'Month'] - archdl1[u'Month']
		arch_dl[u'Total'] = archdl2[u'Total'] - archdl1[u'Total']

		archdl1 = data[u'Meta'][u'stats'][u'ArchiveDownloadAllRevisions']
		archdl2 = data2[u'Meta'][u'stats'][u'ArchiveDownloadAllRevisions']

		arch_rev = {}
		arch_rev[u'Day'] = archdl2[u'Day'] - archdl1[u'Day']
		arch_rev[u'Week'] = archdl2[u'Week'] - archdl1[u'Week']
		arch_rev[u'Month'] = archdl2[u'Month'] - archdl1[u'Month']
		arch_rev[u'Total'] = archdl2[u'Total'] - archdl1[u'Total']

		arch_count = data2[u'Meta'][u'stats'][u'ArchiveDownloadCount'] - data[u'Meta'][u'stats'][u'ArchiveDownloadCount']

		statsdiff = {}
		statsdiff[u'ArchiveDownload'] = arch_dl
		statsdiff[u'ArchiveDownloadAllRevisions'] = arch_rev
		statsdiff[u'ArchiveDownloadCount'] = arch_count

		res[u'Id'] = url
		res[u'Meta'] = {}
		res[u'Meta'][u'stats'] = statsdiff
		res[u'day'] = data[u'day']
		res[u'day2'] = data2[u'day']

		diffs.append(res)

print json.dumps(diffs, indent=4, sort_keys=True)

