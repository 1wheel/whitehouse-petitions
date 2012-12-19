import whitehouse
import sys
import json

x = 0
while True:
	#downloads spefic petition
	petitionSummeries = {}

	f = open('petitions.tsv')
	lines = f.readlines()
	l = lines[sys.argv[1]]
	print l
	print x
	x = x + 1
	l = l.split('\t')
	petitionSummeries = whitehouse.proccessPetition(l[0], l[1], petitionSummeries, True, True)
