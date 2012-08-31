iSniff GPS
==========

This tool performs passive WiFi sniffing for SSID probes, ARPs and MDNS (Bonjour) packets broadcast by nearby iPhones, iPads and other wireless devices.
The aim is to collect data which can be used to identify each device and determine previous geographical locations, based solely on information each device discloses about WiFi networks it has previously joined.

iOS devices transmit ARPs which sometimes contain WiFi AP MAC addresses (BSSIDs) of previously joined networks (see [1]). This is believed to be an implementation of RFC 4436.
If such an ARP is detected, iSniff GPS is able to submit this MAC address to Apple's WiFi location service (masquerading as an iOS device) and visualise the location returned through a Google Maps embed.
This is often highly accurate. If only standard SSID probes have been captured for a particular device, iSniff GPS can query each SSID on wigle.net and visualise possible locations.
By geo-locating multiple SSIDs and WiFi router MAC addresses disclosed by a particular device, it is possible to determine where a device (and by implication its owner) is likely to have been.

Components
----------

iSniff GPS contains 2 major components and further python modules:
* A python script (iSniff_import.py) uses scapy to extract data from a live capture or pcap file and inserts it into a database (iSniff_GPS.sqlite3 by default).
* A Django web application provides a browser-based interface to view and analyse the data collected. 

* wloc.py provides functionality for querying a given BSSID (AP MAC address) on Apple's WiFi location service. It will return the coordinates of the specific MAC queried for and usually an additional 400 nearby BSSIDs and their coordinates.

* wigle.py provides a function for querying a given SSID on the wigle.net database and returns GPS coordinates. It must be configured with a valid wigle.net auth cookie. Please respect the wigle.net ToS in using this module.

Instructions
------------

Install Django, Scapy and all required Python modules.
Initialise an empty database by running `./manage.py syncdb`.
Import data from a pcap by running `./run.sh -r <chan11.pcap>` or start live sniffing with `./run.sh -i mon0`.
Start the web interface by running `./manage.py runserver ip:port`.

Dependencies
------------

iSniff GPS was developed and tested on a Ubuntu 12.04 (32-bit) VM with Python 2.7.3, Django 1.4 and Scapy 2.2.0-dev.
Additional Python modules are required which can generally be installed by running `pip install <module>`:

* dnslib
* netaddr
* requests
* BeautifulSoup4
* protobuf (Google Protocol Buffers)

Credits
-------

Written by @hubert3 / hubert(at)pentest.com
First presented at Blackhat USA July 2012
Code first published on Github 2012-08-31

The implementation of wloc.py which communicates with Apple's WiFi location service to obtain the GPS coordinates of a given BSSID is based on work by François-Xavier Aguessy and Côme Demoustier [2].

Mark Wuergler of Immunity, Inc. provided helpful information through mailing list posts and Twitter replies.

Includes Bluff JS chart library by James Coglan.

1. http://arstechnica.com/apple/2012/03/anatomy-of-an-iphone-leak/
2. http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/
