from bs4 import BeautifulSoup
import math

f = open('dist.male.first.txt')
lines = f.readlines()
male = {}
for l in lines:
	name = l.split(' ')[0]
	male[name] = float(l[15:20])

f = open('dist.female.first.txt')
lines = f.readlines()
female = {}
for l in lines:
	name = l.split(' ')[0]
	female[name] = float(l[15:20])

def chanceMale(name):
	name = name.upper()
	if name in male:
		m = male[name]
	else:
		m = 0

	if name in female:
		f = female[name]
	else:
		f = 0

	if m == 0 and f == 0:
		return .5
	else:
		return m/(f+m)

f = open('lifeTable.htm')
soup = BeautifulSoup(f)
rows = soup.find_all('tr')
maleYears = {}
femaleYears = {}
for row in rows:
	data = row.get_text().split('\n')
	maleYears[int(data[1])] = float(data[3].replace(',',''))*math.pow(1-float(data[2].replace(',','')),5) 
	femaleYears[int(data[1])] = float(data[6].replace(',',''))*math.pow(1-float(data[5].replace(',','')),5)

maleNameAge = {}
femaleNameAge = {}
for age in range(13, 70):
	birthYear = 2012 - age;
	f = open('birthNames\\yob' + str(birthYear) + '.txt')
	lines = f.readlines()
	for l in lines:
		data = l.split(',')
		name = data[0].upper()
		num = float(data[2])
		if data[1] == 'M':
			if not name in maleNameAge:				
				maleNameAge[name] = {}
			maleNameAge[name][age] = num*maleYears[age]
		else:
			if not name in femaleNameAge:				
				femaleNameAge[name] = {}
			femaleNameAge[name][age] = num*femaleYears[age]

def meanAge(name):
	name = name.upper()
	num = 0
	denom = 0
	for age in range(13, 70):
		try:
			num = num + age*femaleNameAge[name][age]
			denom = denom + femaleNameAge[name][age]
		except Exception:
			True
		try:
			num = num + age*maleNameAge[name][age]
			denom = denom + maleNameAge[name][age]
		except Exception:
			True
	if num != 0 and denom != 0:
		if num / denom < 13:
			print num / denom
			dogs = hair
		return num / denom
	else:
		return -1