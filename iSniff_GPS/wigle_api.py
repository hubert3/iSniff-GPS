#!/usr/bin/python
import settings
from wigle import Wigle
# parse lat/lon from hrefs in results page like
# <a href="/gps/gps/Map/onlinemap2/?maplat=39.89233017&maplon=-86.15497589&mapzoom=17&ssid=NETGEAR&netid=00:00:85:E7:0C:01">Get Map</a>
def getLocation(BSSID='',SSID=''):
	wigle = Wigle(settings.wigle_username, settings.wigle_password)
	results = wigle.search(ssid=SSID) 
	apdict={}
	count=1
	for result in results:
		lat = float(result['trilat'])     
		lon = float(result['trilong'])  
		ssid_result = result['ssid'] #match any number of non-& characters
		bssid_result = result['netid']
		if SSID and ssid_result==SSID: # exact case sensitive match
			id = '%s [%s] [%s]' % (SSID,bssid_result,count)
			apdict[id]=(lat,lon)
			count+=1
	return apdict
