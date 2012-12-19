import whitehouse
import sys
import json

#iterates over all petition urls in petitions.cvs
petitionSummeries = {}

f = open('petitions.tsv')
lines = f.readlines()
for l in lines:
	l = l.split('\t')
	petitionSummeries = whitehouse.proccessPetition(l[0], l[1], petitionSummeries, False, False)

json.dump(petitionSummeries, open('webpage\\data\\petitionSummeries.json', 'wb'))