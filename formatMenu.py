import json

f = open('petitions.tsv')
w = open('menu.html', 'w')

w.write('<select>\n')
lines = f.readlines()
for l in lines:
	l = l.split('\t')
	w.write('<option>' + l[0] + '</option>\Wn')
w.write('</select>')

f = open('Cousub_comparability_tab.txt')
w = open('countyFIPSupdate.txt', 'w')

updateCounty = {}
countyNames = {}
lines = f.readlines()
for l in lines:
	s = l.split('\t')
	name = s[6].split(",")[1][1:]
	countyNames[s[0][:5]] = name 
	if s[0][:5] != s[7][:5]:
		w.write(l)
		updateCounty[s[7][:5]] = s[0][:5]


w = open('countyFIPSupdateNumbers.txt', 'w')
for county in updateCounty:
	w.write(county + " " + updateCounty[county] +'\n')

w = open('countyNames', 'w')
for county in countyNames:
	w.write(county + "\t" + countyNames[county] + '\n')