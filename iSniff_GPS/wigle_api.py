#!/usr/bin/python
import settings
import requests
from requests.auth import HTTPBasicAuth
# parse lat/lon from hrefs in results page like
# <a href="/gps/gps/Map/onlinemap2/?maplat=39.89233017&maplon=-86.15497589&mapzoom=17&ssid=NETGEAR&netid=00:00:85:E7:0C:01">Get Map</a>
def getLocation(BSSID='',SSID=''):
	payload = {'first': '0', 'freenet': 'false', 'paynet': 'false', 'ssid': SSID, 'api_key': (settings.wigle_username + settings.wigle_password).encode('base64','strict')}
	results = requests.get(url='https://api.wigle.net/api/v2/network/search', params=payload, auth=HTTPBasicAuth(settings.wigle_username, settings.wigle_password)).json()
	apdict={}
	count=1
	for result in results['results']:
		lat = float(result['trilat'])
		lon = float(result['trilong'])
		ssid_result = result['ssid'] #match any number of non-& characters
		bssid_result = result['netid']
		if SSID and ssid_result==SSID: # exact case sensitive match
			id = '%s [%s] [%s]' % (SSID,bssid_result,count)
			apdict[id]=(lat,lon)
			count+=1
	return apdict
