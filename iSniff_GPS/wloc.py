# -*- coding: utf-8 -*-
#!/usr/bin/python

# Mostly taken from paper by François-Xavier Aguessy and Côme Demoustier
# http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/

import sys
import code
import requests
import BSSIDApple_pb2
#import simplekml

def padBSSID(bssid):
	result = ''
	for e in bssid.split(':'):
		if len(e) == 1:
			e='0%s'%e
		result += e+':'
	return result.strip(':')

def ListWifiDepuisApple(wifi_list):
	apdict = {}
	#kml = simplekml.Kml()
	for wifi in wifi_list.wifi:
		#print "Wifi BSSID : ", wifi.bssid 
		if wifi.HasField('location'):
			lat=wifi.location.latitude*pow(10,-8)
			lon=wifi.location.longitude*pow(10,-8)
			#kml.newpoint(name=wifi.bssid, coords=[(lon,lat)])
			mac=padBSSID(wifi.bssid)
			apdict[mac] = (lat,lon)
		if wifi_list.HasField('valeur_inconnue1'):
			print 'Inconnu1 : ', '%X' % wifi_list.valeur_inconnue1
		if wifi_list.HasField('valeur_inconnue2'):
			print 'Inconnu2 : ', '%X' % wifi_list.valeur_inconnue1
		if wifi_list.HasField('APIName'):
			print 'APIName : ', wifi_list.APIName
	#kml.save("test.kml")
	return apdict

def QueryBSSID(bssid):
	liste_wifi = BSSIDApple_pb2.BlockBSSIDApple()
	wifi = liste_wifi.wifi.add()
	wifi.bssid = bssid
	liste_wifi.valeur_inconnue1 = 0
	liste_wifi.valeur_inconnue2 = 0
	liste_wifi.APIName= "com.apple.Maps"
	chaine_liste_wifi = liste_wifi.SerializeToString()
	longueur_chaine_liste_wifi = len(chaine_liste_wifi)
	headers = { 	'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*', "Accept-Charset": "utf-8","Accept-Encoding": "gzip, deflate",\
			"Accept-Language":"en-us", 'User-Agent':'locationd (unknown version) CFNetwork/548.1.4 Darwin/11.0.0'}
	data = "\x00\x01\x00\x05"+"en_US"+"\x00\x00\x00\x09"+"5.1.9B176"+"\x00\x00\x00\x01\x00\x00\x00" + chr(longueur_chaine_liste_wifi) + chaine_liste_wifi;
	r = requests.post('https://gs-loc.apple.com/clls/wloc',headers=headers,data=data)
	liste_wifi = BSSIDApple_pb2.BlockBSSIDApple() 
	liste_wifi.ParseFromString(r.content[10:])
	return ListWifiDepuisApple(liste_wifi)

