from django.http import HttpResponse, HttpRequest
from django.core.exceptions import *
from django.shortcuts import render
from django.views.generic import *
from django.db.models import Count
from models import *
import wigle
import wloc
import re
from netaddr import EUI

def get_manuf(apdict):
	manufdict = {}
	for m in apdict.keys():
		try:
	                mac = EUI(m)
        	        manufdict[m] = mac.oui.records[0]['org']
			#.split(' ')[0].replace(',','')
        	        #.replace(', Inc','').replace(' Inc.','')
	        except:
                	manufdict[m] = 'unknown'
        return manufdict

class ClientList(ListView):
	model = Client
	template_name = 'client_list.html'
        def get_queryset(self):
          return Client.objects.order_by('manufacturer','mac')
        def get_context_data(self, **kwargs):
	       	context = super(ClientList, self).get_context_data(**kwargs)
		probedict = {}
		for client in Client.objects.all():
			probedict[client] = AP.objects.filter(client=client)
		context['probedict'] = probedict
		context['apcount'] = len(AP.objects.all())
		context['devicecount'] = len(Client.objects.all())
	        return context

class ClientDetail(DetailView):
	model = Client
	slug_field = 'mac'
	template_name = 'client_detail.html'
        def get_context_data(self, **kwargs):
	       	context = super(ClientDetail, self).get_context_data(**kwargs)
		context['APs'] = AP.objects.filter(client=self.object)
	        return context

class APList(ListView):
	model = AP
	template_name = 'ap_list.html'
        def get_queryset(self):
        	return AP.objects.annotate(num_clients=Count('client')).order_by('-num_clients')
        def get_context_data(self, **kwargs):
			context = super(APList, self).get_context_data(**kwargs)
			context['apcount'] = len(AP.objects.all())
			context['devicecount'] = len(Client.objects.all())
			#context['Clients'] = self.object.client
			return context

class APDetail(DetailView):
	model = AP
	template_name = 'ap_detail.html'
	def get_object(self):
		lookup = self.kwargs['ssid_or_bssid']
		if re.match(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',lookup):
			a=AP.objects.get(BSSID=lookup)
		else:
			a=AP.objects.get(SSID=lookup)
		return a

	def get_context_data(self, **kwargs):
		print self.kwargs
		context = super(APDetail, self).get_context_data(**kwargs)
		context['Clients'] = self.object.client.all()
		return context

class Home(TemplateView):
    template_name = "home.html"
 
class stats(TemplateView):
    template_name = "stats.html"
    def get_context_data(self, **kwargs):
        from operator import itemgetter
        context = super(stats, self).get_context_data(**kwargs)
        manuf = {}
	for m in Client.objects.values_list('manufacturer',flat=True).distinct():
		m = m[0].upper()+(m[1:].lower())
        	manuf[m] = len(Client.objects.filter(manufacturer__iexact=m))
	l = []
	for m in manuf.items():
        	l.append(m)		
	context['manuf']=sorted(l, key=itemgetter(1), reverse=True)[:10]
	context['devicecount'] = len(Client.objects.all())
        return context


def getCenter(apdict):
	numresults = len(apdict)
	latCenter = 0.0
	lonCenter = 0.0	
	for (lat,lon) in apdict.values():
		latCenter += lat
		lonCenter += lon
	return( ((latCenter / numresults),(lonCenter / numresults)) )
	
def AppleWloc(request,bssid=None):
	if bssid:
		apdict = wloc.QueryBSSID(bssid)
		numresults = len(apdict)
		if numresults == 0 or (-180.0, -180.0) in apdict.values():
			return HttpResponse('0 results.')
		if bssid in apdict.keys():
			try:
				a = AP.objects.get(BSSID=bssid)
				(a.lat,a.lon) = apdict[bssid]
				a.save() #if Apple returns a match for BSSID we save this as location
				print 'Updated %s location to %s' % (a,(a.lat,a.lon))
			except ObjectDoesNotExist:
				pass
		return render(request,'apple-wloc.html',{'bssid':bssid,'hits':len(apdict),'center':getCenter(apdict),'bssids':apdict.keys(),'apdict':apdict,'manufdict':get_manuf(apdict)})
	else:
		return render(request,'apple-wloc.html',{'bssid':'00:1b:2f:3d:a9:32'})

def locateSSID(request,ssid=None):
	if ssid:
		apdict = wigle.getLocation(SSID=ssid)
		numresults = len(apdict)
		if numresults == 0:
			return HttpResponse('0 results.')
		return render(request,'wigle-wloc.html',{'ssid':ssid,'hits':len(apdict),'center':getCenter(apdict),'bssids':apdict.keys(),'apdict':apdict})
	else:
		return render(request,'wigle-wloc.html',{'ssid':'','center':(56.97518158, 24.17274475)})
		
def updateSSID(request):
	try:
		ssid = request.POST['ssid']
		(lat,lon) = request.POST['position'].replace('(','').replace(')','').split(',')
		lat = float(lat)
		lon = float(lon)
		a = AP.objects.get(SSID=ssid)
		(a.lat,a.lon) = (lat,lon)
		a.save()
		return HttpResponse('Updated %s location to %s' % (a,(a.lat,a.lon)))
	except ObjectDoesNotExist:
		return HttpResponse('Not found in db.')



