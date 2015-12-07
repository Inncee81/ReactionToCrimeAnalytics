from lxml import etree
from datetime import datetime
import sys
import os
from os import listdir
import gzip
import random
import time

raceWords = {'black':1,'white':1,'african american':1,'caucasian':1,'race':1,'ethnicity':1,'minority':1, "racisim":1, "racist":1, "racial":1,"profiling":1, "prejudice":1, "discrimination":1}

crimeWords = {'crime':1,'police':1,'cop':1,'shooting':1,'fatal':1,'murder':1,'criminal':1,'dead':1,'killed':1,'died':1,'shot':1,'gun':1,'kill':1,'die':1,"jail":1, }

trialWords = {"justice":1, "case":1, "shoot":1, "guilty":1, "trial":1, "defense":1, "prosecution":1, "jury":1, "witness":1, "witnesses":1, "dna":1, "evidence":1}

sigWords = {"ferguson":1,"trayvon martin":1,"trayvon":1, "black lives matter":1, "blacklivesmatter":1, "michael brown":1, "garner":1, "eric garner":1, "zimmerman":1, "george zimmerman":1, "hands up":1,"protest":1, "protesters":1}

def checkForKeywords(text):
        race = 0
        crime = 0
        sig = 0
        trial = 0
        for word in text.split(" "):
                #print word
                w = word.lower()
                if w in raceWords:
                        race+=1
                if w in crimeWords:
                        crime+=1
                if w in sigWords:
                        sig+=1
                if w in trialWords:
                        trial+=1
        if race >= 1 and crime >=1:     
                #print text
                return True
	if race >= 2:
		#print text
		return True
	if crime >= 2:
		#print text
		return True
        if sig >= 1:
                #print text
                return True
        if trial >= 2:
                #print text
                return True
        return False

def checkForI(text):
	if 'i' in text.lower() or 'i\'m' in text.lower():
		return True


def getDay(f):
	if f[4] == 't':
		return '0' + f[3]
	else:
		return f[3:5]


def writeOutput(d,f,day):
	#print d
	for (key,value) in d.iteritems():
		f.write(day + ' ' + str(key) + ' ' + str(value[0]) + ' ' + str(value[1]) + '\n')



places = ["Uniondale","uniondale","windsor hills","Windsor Hills","woodmore","Woodmore","fort washington","fort Washington","Newark", "newark","buffalo", "Buffalo", "Baltimore", "baltimore","vanceburg", "Vanceburg", "sneedville", "Sneedville","Mansfield","mansfield", "Mitchellville", "mitchellville","Hillcrest","hillcrest","Short Hills","short hills","Weston","weston", "Mesa", "mesa","Oklahoma City","oklahoma city","virginia beach","Virginia Beach","Seattle","seattle","oakland","Oakland","Boston","boston","Ladera Heights","ladera heights"]




output = open('output2.txt', 'w')

for year in ['2013','2014']:
	print year
	months = os.listdir(year+'/')
	for month in months:
		print month
		files = os.listdir(year + '/' + month + '/')
		for f in files:
			if 'xml' in f:
				d = {'newark':[0,0], 'buffalo':[0,0], 'baltimore':[0,0], 'baltimore':[0,0], 'vanceburg':[0,0], 'sneedville':[0,0], 'mansfield':[0,0], 'mitchellville':[0,0], 'hillcrest':[0,0],
	'short hills':[0,0],'weston':[0,0],'mesa':[0,0],'oklahoma city':[0,0],'seattle':[0,0],'oakland':[0,0],'boston':[0,0],'ladera heights':[0,0],'virginia beach':[0,0],
	"uniondale":[0,0],"windsor hills":[0,0],"woodmore":[0,0],"fort washington":[0,0]}

				fname = year + '/' + month + '/' + f

				for event,elem in etree.iterparse(fname,events=["end"],tag="{http://www.bid.berkeley.edu/statuses}status",recover=True):
					userElem = elem.find("{http://www.bid.berkeley.edu/statuses}user")
					if userElem is not None:
						locationElem = userElem.find("{http://www.bid.berkeley.edu/statuses}location")
						tweetText = elem.find("{http://www.bid.berkeley.edu/statuses}text")
						if locationElem is not None:
							if isinstance(locationElem.text,str):
								for place in places:
									if place in locationElem.text:
										d[place.lower()][1]+=1
										if checkForI(tweetText.text):
											d[place.lower()][0]+=1
							if locationElem.text is None:
								placeElem = locationElem.find("{http://www.bid.berkeley.edu/statuses}place")
								if placeElem is not None:
									nameText = placeElem.find("{http://www.bid.berkeley.edu/statuses}name").text
									if nameText is not None and isinstance(nameText, str):
										for place in places:
											if place in nameText:
												d[place.lower()][1]+=1
												if checkForI(tweetText.text):
													d[place.lower()][0]+=1
		
					elem.clear()
				#print d
				writeOutput(d,output,month+getDay(f)+year)
output.close()
