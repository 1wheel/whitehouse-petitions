from bs4 import BeautifulSoup
import urllib                                       
import pickle
from cStringIO import StringIO
import json
from sets import Set
import datetime
import time
from time import mktime
import code
from sys import stdout
import sys

import formatUS
import names

#finds API page from petition page
def findAPIurl(petitionURL):
	f = urllib.urlopen(petitionURL)
	soup = BeautifulSoup(f)
	nextNum = soup.select(".load-next")[0]['href'].split('=')[2]
	baseURL = 'https://petitions.whitehouse.gov/signatures/more/' + soup.select(".load-next")[0]['rel'][0] + '/2/'
	return {'baseURL': baseURL, 'nextNum':nextNum}

#retuns name, date, and location of everyone who has signed the petition
def downloadSigs(baseURL, nextNum, lastDate):
	error_count = 0
	print lastDate
	sigList = []
	lastNum = ""
	workingNum = ""
	while lastNum != nextNum:
		#print baseURL + nextNum 
		#print len(sigList)
		try:
			f = urllib.urlopen(baseURL + nextNum)
			lastNum = nextNum
			soup = BeautifulSoup(f)
			if len(soup.select("a")) == 1:
				nextNum = findNextNum(soup)
				sigList.extend(scrapePage(soup))
				lastTimeString = sigList[-1]['date']
				lastTime = time.strptime(lastTimeString, "%B %d, %Y")  

				workingNum = lastNum

				if mktime(lastTime) - lastDate < -25*3600:
					print "\nDate indicates data already downloaded"
					return {'list': sigList, 'nextNum':workingNum, 'lastDate': time.mktime(time.gmtime())}
			else:
				print "\nNo next API page"
				print baseURL + nextNum 
				return {'list': sigList, 'nextNum':workingNum, 'lastDate': time.mktime(time.gmtime())}
			
			#writes number downloaded in one place   
			stdout.write("\r%d" % len(sigList))
			stdout.flush()

		except Exception:
			print "    IO error?  " + str(error_count) + "  "
			error_count = error_count + 1
			if error_count > 10:
				return {'list': sigList, 'nextNum':workingNum, 'lastDate': time.mktime(time.gmtime())}

	print "Nothing to return"
	return {'list': sigList, 'nextNum':"workingNum", 'lastDate': time.mktime(time.gmtime())}

#finds the next API page from current api page
def findNextNum(soup):
	str = soup.select("a")[0].get_text()
	strTokens = str.split('a>  ')
	j = 0
	while strTokens[1][j] != '<':
		j = j + 1
	return strTokens[1][0:j]

#scrapes API page
def scrapePage(soup):
	str = soup.get_text().replace(' ', '')
	strTokens = soup.get_text().split("     \\n    \\n     \\n      \\n        \\n    ")	
	rv = []
	for i in range(1, len(strTokens)):
		j = 0
		while strTokens[i][j] != '<':
			j = j + 1
		name = strTokens[i][0:j].replace('\\n','')
		j = j + 17 + 9 + 1
		start = j
		while strTokens[i][j] != '\\':
			j = j + 1
		loc = strTokens[i][start:j]
		j = j + 2 + 6
		start = j
		while strTokens[i][j] != '\\':
			j = j + 1
		date = strTokens[i][start:j]
		rv.append({'name':name, 'loc': loc, 'date':date})
	return rv

#takes old and new sigs, returns combined list without duplicates
def mergeSigList(old, new):
	old.extend(new)
	result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in old)]
	return result
	# for newsig in new:
	# 	appendSig = True
	# 	for oldsig in old:
	# 		if oldsig['name'] == newsig['name']:
	# 		 	if oldsig['loc'] == newsig['loc']:
	# 		 		if oldsig['date'] == newsig['date']:
	# 					appendSig = False
	# 	if appendSig:
	# 		old.append(newsig) 
	# return old

#converts raw sig download into .json ready for display
def saveSigStats(name, sigs, url, petitionSummeries):
	petitionSummeries[name] = {}

	countySums = {}
	for county in formatUS.countyCodes:
		countySums[county] = 0

	#finds the number of sigs in each county and gender distubution
	genderSum = .5
	genderNum = 1
	ageSum = 40
	ageNum = 1
	numDelta = 0
	demSum = .5
	demNum = 1
	dates = {}
	for sig in sigs:
		try:		
			gender = names.chanceMale(sig['name'][:-2])
			if gender != -1:
				genderSum = genderSum + gender
				genderNum = genderNum + 1

			age = names.meanAge(sig['name'][:-2])
			if age != -1:
				ageSum = ageSum + age
				ageNum = ageNum + 1
				if age < 13:
					print age 
					dogs = haiss

			countyCode = formatUS.findCountyCode(sig['loc'][:-4], sig['loc'][-2:])
			if countyCode != -1:
				countySums[countyCode] = countySums[countyCode] + 1
			
			if countyCode in formatUS.countyPres:
				demSum = demSum + formatUS.countyPres[countyCode]
				demNum = demNum + 1			

			if time.mktime(time.gmtime()) - mktime(time.strptime(sig['date'], "%B %d, %Y")) < 49*60*60:
				numDelta = numDelta + 1

			date = mktime(time.strptime(sig['date'], "%B %d, %Y"))
			if date in dates:
				dates[date] = dates[date] + 1
			else:
				dates[date] = 1

		except Exception:
			print sig

	sumDates = {}
	maxDate = 0
	secoundDate = 0
	for date in dates:
		sumDates[date] = 0
		for date1 in dates:
			if date >= date1:
				sumDates[date] = sumDates[date] + dates[date1]
		if date > maxDate:			
			secoundDate = maxDate
			maxDate = date

	petitionSummeries[name]['name'] = name
	petitionSummeries[name]['gender'] = float(round(1 - genderSum/genderNum*100, 1)) + 0.0
	petitionSummeries[name]['party'] = round(demSum/demNum*100, 1)
	petitionSummeries[name]['age'] = round(ageSum/ageNum, 1)
	petitionSummeries[name]['total'] = len(sigs)
	petitionSummeries[name]['delta'] = dates[secoundDate]
	petitionSummeries[name]['dates'] = dates 
	petitionSummeries[name]['sumDates'] = sumDates
	petitionSummeries[name]['url'] = url
	petitionSummeries[name]['html'] = str(BeautifulSoup(urllib.urlopen(url)).find(class_ = "petition-detail petition-detail-margin-right"))

	#normalizes the number of sigs by population
	countySumsNormalized = {}
	countyValues = []
	for county in countySums:
		countySumsNormalized[county] = countySums[county]/float(formatUS.countyPop[county])
		countyValues.append(countySumsNormalized[county])

	#sorts normalized sigs and finds index of last zero
	countyValues.sort()
	lastZeroIndex = 0
	for i in range(len(countyValues)):
		if countyValues[i] == 0:
			lastZeroIndex = i

	#countyDisplay saves the percentile of normalized sigs each county is in
	#doesn't count counties with 0 sigs
	countyDisplay = {}
	for county in countySumsNormalized:
		countyDisplay[county] = {}
		value = countySumsNormalized[county]
		if value == 0:
			countyDisplay[county]['normalized'] = 0
			countyDisplay[county]['sum'] = 0
		else:
			countyDisplay[county]['normalized'] = (countyValues.index(value) - lastZeroIndex) / float((len(countyValues) - lastZeroIndex))
			countyDisplay[county]['sum'] = countySums[county]

	json.dump(countyDisplay, open('webpage\\data\\' + name + '_countyDisplay.json', 'wb'))

	return petitionSummeries

def proccessPetition(name, url, petitionSummeries, update, searchForOld):	
	print url
	print name

	#check old download first
	print "load last run"
	try:
		pkl_file = open("webpage\\data\\" + name + ".pickle", 'rb')
		old_output = pickle.load(pkl_file)
		print "file loaded, getting date"
		lastDate = old_output['lastDate']
		print "got date"
		print len(old_output['list'])
	except Exception:
		lastDate = 0
		old_output = {'list':[], 'nextNum':0}

	if update:
		apiURL = findAPIurl(url)
		output = downloadSigs(apiURL['baseURL'], apiURL['nextNum'], lastDate)
		print "staring error output"
		print apiURL['baseURL'] + str(old_output['nextNum'])
		error_output = downloadSigs(apiURL['baseURL'], old_output['nextNum'], 0)

		#pdb.set_trace()

		#combine new info with old
		output['list'] = mergeSigList(old_output['list'], output['list'])
		output['list'] = mergeSigList(output['list'], error_output['list'])

		output['nextNum'] = error_output['nextNum']

		pickle.dump(output, open('webpage\\data\\' + name + ".pickle", 'wb'))

	else:
		output = old_output

	petitionSummeries = saveSigStats(name, output['list'], url, petitionSummeries)

	return petitionSummeries