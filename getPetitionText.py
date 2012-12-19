from bs4 import BeautifulSoup
import urllib                                       
import json

f = urllib.urlopen('https://petitions.whitehouse.gov/petition/legally-recognize-westboro-baptist-church-hate-group/DYf3pH2d')
soup = BeautifulSoup(f)
ss = str(soup.find(class_ = "petition-detail petition-detail-margin-right"))

json.dump(ss, open('ptext.json', 'wb'))