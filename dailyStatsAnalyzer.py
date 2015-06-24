import sys
import requests
import json
import random
import datetime

cont = open(sys.argv[1])
stats = json.load(cont)

# Daily and weekly deploys from new charm store 
# (does not include legacy charm store). Includes
# all charm and bundle revisions. 
daily_deploys_cs = 0
weekly_deploys_cs = 0
monthly_deploys_cs = 0
total = 0
legacy = 0

max_daily = 0
max_daily_id = ""
max_weekly = 0
max_weekly_id = ""
max_monthly = 0
max_monthly_id = ""
max_total = 0
max_total_id = ""
max_legacy = 0
max_legacy_id = 0

for data in stats:
	st = data[u'Meta'][u'stats']
	#print st
	all_rev = st[u'ArchiveDownloadAllRevisions']
	#print all_rev
	d = all_rev[u'Day']
	daily_deploys_cs += d
	if d > max_daily:
		max_daily = d
		max_daily_id = data[u'Id']

	w = all_rev[u'Week']
	weekly_deploys_cs += w
	if w > max_weekly:
		max_weekly = w
		max_weekly_id = data[u'Id']

	m = all_rev[u'Month']
	monthly_deploys_cs += m
	if m > max_monthly:
		max_monthly = m
		max_monthly_id = data[u'Id']

	t = all_rev[u'Total']
	total += t
	if t > max_total:
		max_total = t
		max_total_id = data[u'Id']

	l = st[u'ArchiveDownloadCount']
	legacy += l
	if l > max_legacy:
		max_legacy = l
		max_legacy_id = data[u'Id']

print "daily deploys: ", daily_deploys_cs
print "max daily: ", max_daily_id, " with ", max_daily, " deploys"
print "weekly deploys: ", weekly_deploys_cs
print "max weekly: ", max_weekly_id, " with ", max_weekly, " deploys"
print "monthly deploys: ", monthly_deploys_cs
print "max monthly: ", max_monthly_id, " with ", max_monthly, " deploys"
if len(sys.argv) > 2:
	print "total deploys: ", total
	print "max total: ", max_total_id, " with ", max_total, " deploys"
	print "total legacy: ", legacy
	print "max legacy: ", max_legacy_id, " with ", max_legacy, " deploys"
