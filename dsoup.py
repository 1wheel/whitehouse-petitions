import whitehouse

#iterates over all petition urls in petitions.cvs
petitionSummeries = {}

f = open('new.tsv')
lines = f.readlines()
for l in lines:
	l = l.split('\t')
	whitehouse.proccessPetition(l[0], l[1])