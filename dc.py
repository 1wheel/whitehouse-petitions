import whitehouse
import sys
import json

while True:
	#iterates over all petition urls in petitions.cvs
	petitionSummeries = {}

	f = open('petitions.tsv')
	lines = f.readlines()
	print sys.argv[1]
	for l in lines[int(sys.argv[1]):int(sys.argv[1])+5]:
		l = l.split('\t')
		petitionSummeries = whitehouse.proccessPetition(l[0], l[1], petitionSummeries)

	json.dump(petitionSummeries, open('webpage\\data\\petitionSummeries.json', 'wb'))