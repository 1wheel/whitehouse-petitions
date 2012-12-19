import json

f = open('US.txt')
lines = f.readlines()
countyArray = []
for l in lines:
	l = l.split('\t')
	countyArray.append({'name': l[2], 'state': l[4], 'countyName': l[5], 'countyCode': l[6]})

f = open('population.txt')
countyPop = {}
lines = f.readlines()
for l in lines:
	l = l.split(',')
	countyPop[l[0]] = l[1]

stateCodes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}

cityByState = {}
countyCodes = {}

for state in stateCodes:
	cityByState[state] = {}

for city in countyArray:
	try:
		countyCode = stateCodes[city['state']] + city['countyCode']
		if city['countyCode'] != '':
			countyCodes[countyCode] = city['countyName']
			if city['name'] in cityByState[city['state']]:
				if not countyCode in cityByState[city['state']][city['name']]:
					cityByState[city['state']][city['name']].append(countyCode)									
			else:
				cityByState[city['state']][city['name']] = [countyCode]
	#city doesn't have a country code
	except Exception:
		nothing = 0

def findCountyCode(city, state):
	try: 
		return cityByState[state][city][0]
	except Exception:
		#print city + ", " + state
		return -1

f = open('2008PresByCounty.csv')
countyPres = {}
lines = f.readlines()
for l in lines:
	l = l.replace('\"','').split(',')
	try:
		countyPres[l[0]] = float(l[1])/(float(l[1])+float(l[2]))
	except Exception:
		print l

json.dump(countyPop, open('countyPop.json', 'wb'))
#data = json.load(open(filename))
