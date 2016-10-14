# coding: utf-8

import pycurl
from django.utils.translation import ugettext as _
from django.db import models
from StringIO import StringIO

from boites.models import Boite, App

    
#Parse the google map infobox string, made of inbricked bracket arrays
def boxStringToArray(dataS):
    retval = []
    curVal = ""
    ind = 0
    while ind < len(dataS):
    	char = dataS[ind]
    	if char == '[':
    		opened = 0
    		closingInd = ind +1
    		while dataS[closingInd] != ']' or opened != 0:
    			if dataS[closingInd] == '[':
    				opened += 1
    			elif dataS[closingInd] == ']':
    				opened -= 1
    			closingInd += 1
    
    		retval.append(boxStringToArray(dataS[ind+1:closingInd + 1])) 
    		ind = closingInd 
    	elif char == ',':
    		if len(curVal) > 0:
    			retval.append(curVal)
    		curVal = ""
    	elif char != ']':
    		curVal += char
        ind += 1
    
    if len(curVal) > 0:
        retval.append(curVal)
    
    return retval

def queryTimes(start, dest):

    RESPONSE_KEY = "        cacheResponse"

    retval = {}
    boxedData = ""

    #Remove spaces in addresses
    start = start.replace(' ', '+')
    dest = dest.replace(' ', '+')

    
    #Format the target URL
    base_url = "https://www.google.com/maps/dir/?"
    source_address_key = "saddr="
    destination_address_key = "daddr="
    end_parameters = "&dg=dbrw&newdg=1"

    url =  base_url
    url += source_address_key
    url += start
    url += "&"
    url += destination_address_key
    url += dest
    url += end_parameters
    
    #Request
    buf = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url.encode('utf-8'))
    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
    c.setopt(c.WRITEDATA, buf)
    
    c.perform()
    c.close()
    
    body = buf.getvalue()

    # Parse the response, and extract the code correponding to the info box
    for line in body.splitlines():
    	if RESPONSE_KEY in line:
    		boxedData = line[line.index('['):]
                break
   
    # Convert that string to an array
    infobox = boxStringToArray(boxedData)
    
    for traj in infobox[0][11][0]:
    	info = traj[0]
    	name = info[0]
        name = name.replace('"', '')
    	dist = info[1][1]
	if len(info[6][0]) == 2:
        	duration_s, duration = info[6][0]
                retval[name] = int(duration_s)

    return retval


class AppTraffic(App):
    start = models.CharField(_(u"Starting Point"), max_length = 1024,  null=True, default=None)
    dest = models.CharField(_(u"Destination"), max_length = 1024,null=True, default=None)
    trajectory_name = models.CharField((u"Itineray Name"), max_length = 128,null=True, default=None)
    trip_duration = models.PositiveSmallIntegerField((u"Duration"),null=True, default=None)

    def get_app_dictionary(self):

        if self.enabled:
            durations = queryTimes(self.start, self.dest)
                
            self.trajectory_name = min(durations, key = lambda x : durations[x])
            self.trip_duration = durations[self.trajectory_name] / 60

            self.save()

        return {'start': self.start, 'dest' : self.dest, 'trajectory_name':self.trajectory_name, 'trip_duration':self.trip_duration}

    class Meta:
        verbose_name = _("Configuration : traffic")
        verbose_name_plural = _("Configurations : traffic")
