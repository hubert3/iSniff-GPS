iSniff GPS
==========

iSniff GPS passively sniffs for SSID probes, ARPs and MDNS (Bonjour) packets broadcast by nearby iPhones, iPads and other wireless devices.
The aim is to collect data which can be used to identify each device and determine previous geographical locations, based solely on information each device discloses about previously joined WiFi networks.

iOS devices transmit ARPs which sometimes contain MAC addresses (BSSIDs) of previously joined WiFi networks, as described in [[1]][ars]. iSniff GPS captures these ARPs and submits MAC addresses to Apple's WiFi location service (masquerading as an iOS device) to obtain GPS coordinates for a given BSSID. If only SSID probes have been captured for a particular device, iSniff GPS can query network names on wigle.net and visualise possible locations.

By geo-locating multiple SSIDs and WiFi router MAC addresses, it is possible to determine where a device (and by implication its owner) is likely to have been.

Components
----------

iSniff GPS contains 2 major components and further python modules:
* iSniff_import.py uses [Scapy](http://www.secdev.org/projects/scapy/) to extract data from a live capture or pcap file and inserts it into a database (iSniff_GPS.sqlite3 by default).

* A Django web application provides a browser-based interface to view and analyse the data collected. This includes views of all detected devices and the SSIDs / BSSIDs each has probed for, a view by network, Google Maps views for visualising possible locations of a given BSSID or SSID, and a pie chart view showing a breakdown of the most popular device manufacturers based on client MAC address Ethernet OUIs.

* __wloc.py__ provides a _QueryBSSID()_ function which looks up a given BSSID (AP MAC address) on Apple's WiFi location service. It will return the coordinates of the MAC queried for and usually an additional 400 nearby BSSIDs and their coordinates.

* __wigle.py__ provides a _getLocation()_ function for querying a given SSID on the wigle.net database and returns GPS coordinates. It must be configured with a valid wigle.net auth cookie. Please respect the wigle.net ToS in using this module.

Instructions
------------

1. Install Django 1.5+, Scapy and all required Python modules.
2. Initialise an empty database by running `./manage.py syncdb`.
3. Import data from a pcap by running `./run.sh -r <chan11.pcap>` or start live sniffing with `./run.sh -i mon0`. 
4. Start the web interface by running `./manage.py runserver ip:port`.

To solicit ARPs from iOS devices, set up an access point with DHCP disabled (e.g. using airbase-ng) and configure your sniffing interface to the same channel. 

Once associated, iOS devices will send up to three ARPs destined for the MAC address of the DHCP server on previously joined networks. On typical home WiFi routers, the DHCP server MAC address is the same as the WiFi interface MAC address, which can be used for accurate geolocation. On larger corporate WiFi networks, the MAC of the DHCP server may be different and thus cannot be used for geolocation.

Dependencies
------------

iSniff GPS was developed and tested on a Ubuntu 12.04 (32-bit) VM with Python 2.7.3, Django 1.5.1 and Scapy 2.2.0-dev.
Additional Python modules are required which can generally be installed by running `pip install <module>`:

* dnslib
* netaddr
* requests
* BeautifulSoup4
* protobuf (Google Protocol Buffers)

Credits
-------

Written by @hubert3 / hubert(at)pentest.com. Presented at Blackhat USA July 2012, code published on Github 2012-08-31.

The implementation of wloc.py is based on work by François-Xavier Aguessy and Côme Demoustier [[2]][paper].

Mark Wuergler of Immunity, Inc. provided helpful information through mailing list posts and Twitter replies.

Includes Bluff JS chart library by James Coglan.

1. http://arstechnica.com/apple/2012/03/anatomy-of-an-iphone-leak/
2. http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/

[ars]: http://arstechnica.com/apple/2012/03/anatomy-of-an-iphone-leak/
[paper]: http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/
