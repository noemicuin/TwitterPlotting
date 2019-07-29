"""
  Filename: test.py
  Description: Using a Twitter API, this code will stream for
	a certain word or hashtag all throughout Twitter. Once
	the data is gathered, the coordinates from eacth Tweet
	wil be saved into a .csv file. Right after, the 
	program will display a visualization of where the 
	tweets are coming from. The coordinates of the tweet
	will be displayed on a map.
  Authors: Yarely Chino & Noemi Cuin


"""




#import of needed Python Libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
from flask import Flask, Response
import json



#API keys needed to access Twitter API
ckey = ''
csecret = ''
atoken = ''
asecret = ''



# class that streams Twitter and then gathers the coordinates of the tweets and adds them to a csv file.
class listener(StreamListener):

    def on_data(self, data):
	try:
		word = "c++"
		if(word in data):#25
			tweet = data.split('"coordinates":[')[1].split(']},"coordinates"')[0]
			if(len(tweet)<=25):
				print tweet
				#open a file and then import the needed data into the csv file.				
				saveFile = open('world_data4.csv', 'a')
				saveFile.write(tweet)
				saveFile.write('\n')			
				saveFile.close()
		return True
	except BaseException, e:
		print 'failed ondata,', str(e)
		time.sleep(5)

    def on_error(self, status):
        print status



# built in functions that are part of the tweepy
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

 
twitterStream = Stream(auth, listener())



#After coordinates are gathered from the streams, and they are saved into a csv file, then the csv library needs to be imported so that Python can access the file.

import csv

# open the coordinates data file
filename = 'world_data4.csv'

# create empty lists for the latitudes and longitudes
lats, lons = [], []

# read through the entire file, skip the first line,
# and pull out just the lats and lons

with open(filename) as f:
	# create a csv reader object.
	reader = csv.reader(f)

	# ignore the header row
	# next(reader)

	# store the latitudes and longitudes in the appropriate
	# lists
	for row in reader:
		lats.append(float(row[0]))
		lons.append(float(row[1]))


# ---- Build Map ----


#imported libraries to produce the map
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
 
# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
map = Basemap(projection='robin', lat_0=0, lon_0=-100,
              resolution='l', area_thresh=1000.0)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'gray')
map.drawmapboundary()

map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))


# plots the coordinates that were read through the csv file
x,y = map(lons, lats)
map.plot(x,y, 'bo', markersize = 8)


title_string = "Locations of Streamed Tweets"

plt.title(title_string)
 
plt.show()



twitterStream.filter(locations = [-179,-85, 179,85])













