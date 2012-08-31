from django.db import models

class Client(models.Model):
	mac = models.CharField(max_length=len('ff:ff:ff:ff:ff:ff'), unique=True) 
	lastseen_date = models.DateTimeField('date last seen')
	name = models.CharField(max_length=200, blank=True)
	comment = models.CharField(max_length=200, blank=True)
	manufacturer = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		return u'%s' % (self.mac)

class AP(models.Model):
	client = models.ManyToManyField(Client)
	SSID = models.CharField(max_length=200, blank=True)
	BSSID = models.CharField(max_length=len('ff:ff:ff:ff:ff:ff'), blank=True)
	name = models.CharField(max_length=200, blank=True)
	comment = models.CharField(max_length=200, blank=True)
	manufacturer = models.CharField(max_length=200, blank=True)
	lastprobed_date = models.DateTimeField('date last probed for')
	lon = models.FloatField(null=True)
	lat = models.FloatField(null=True)
	address = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		if self.SSID and self.BSSID:
			return u'%s [%s]' % (self.SSID,self.BSSID)
		if self.SSID:
			return u'%s' % self.SSID
                if self.BSSID:
                        return u'<font color="red">ARP:%s</font>' % self.BSSID

class Location(models.Model):
	ap = models.ForeignKey(AP)
	lon = models.FloatField()
	lat = models.FloatField()
	name = models.CharField(max_length=200, blank=True)
	source = models.CharField(max_length=20) # Apple or Wigle at present
	comment = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		return u'%s,%s' % (self.lon,self.lat)
