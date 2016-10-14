# coding: utf-8

import pycurl
from django.utils.translation import ugettext as _
from django.db import models
from StringIO import StringIO

from boites.models import Boite, App

RESP_KEY = "        cacheResponse"
    
def strToArray(dataS):
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
    
    		retval.append(strToArray(dataS[ind+1:closingInd + 1])) 
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

    retval = {}

    url =  "https://www.google.com/maps/dir/"
    url += "?saddr="
    url += start.replace(' ', '+')
    url += "&daddr="
    url += dest.replace(' ', '+')
    url += "&dg=dbrw&newdg=1"
    boxedData = ""
    
    buf = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
    c.setopt(c.WRITEDATA, buf)
    
    c.perform()
    c.close()
    
    body = buf.getvalue()

    for line in body.splitlines():
    	if RESP_KEY in line:
    		boxedData = line[line.index('['):]
    
    trafficVals = strToArray(boxedData)
    
    for traj in trafficVals[0][11][0]:
    	info = traj[0]
    	name = info[0]
    	dist = info[1][1]
	if len(info[6][0]) == 2:
        	duration_s, duration = info[6][0]
                retval[name] = duration_s
	if len(info[6][3]) == 2:
	    baseDuration_s, baseDuration = info[6][3]


    return retval


class AppTraffic(App):
    start = models.CharField(_(u"Starting Point"), max_length = 1024,  null=True, default=None)
    dest = models.CharField(_(u"Destination"), max_length = 1024,null=True, default=None)
    trajectory_name = models.CharField((u"Itineray Name"), max_length = 128,null=True, default=None)
    trip_duration = models.PositiveSmallIntegerField((u"Duration"), max_length = 128,null=True, default=None)

    def get_app_dictionary(self):

        if self.enabled:
            durations = queryTimes(self.start, self.dest)
                
            self.trajectory_name = min(durations, key = lambda x : durations[x]) #checkformt s ?
            self.trip_duration = durations[self.trajectory_name]

            self.save()

        return {'start': self.start, 'dest' : self.dest, 'trajectory_name':self.trajectory_name, 'trip_duration':self.trip_duration}

    class Meta:
        verbose_name = _("Configuration : traffic")
        verbose_name_plural = _("Configurations : traffic")
