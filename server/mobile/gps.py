from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from forms import *
from models import *


import urllib2
from BeautifulSoup import BeautifulSoup

import json

def getDirections(request):
  slat=request.GET.get('slat','36.364835')
  slng=request.GET.get('slng','127.363901')
  
  elat=request.GET.get('elat','36.36649376238311')
  elng=request.GET.get('elng','127.30965600488275')
  
  url="http://map.daum.net/congsoa/route/getSearchRoute.service?inputCoordSystem=WGS84&x="+slng+"&y="+slat
  url+="&x="+elng+"&y="+elat+"&method=realtime"
  xml = urllib2.urlopen(url)
  soup = BeautifulSoup(xml)
  nodes = soup.findAll('rout:points')
  result=''
  for idx, node in enumerate(nodes):
    result+=node.string
  result=(result.strip()).split(' ')
  
  resultSet=list()
  tempr=''
  print url
  for coord in result:
    coordSet=coord.split(',')
    temp=changeCoordinates(coordSet[0],coordSet[1],"CONGNAMUL","WGS84")
    resultSet.append(temp)
      #localhost:8000/gps/direction?&slat=36.364835&slng=127.363901&elng=36.36473132617699&elng=127.35270009515375
  response=HttpResponse(json.dumps(resultSet, indent=4))
  response['Content-Type'] = "application/json"
  return response
  
#WGS84, CONGNAMUL
def changeCoordinates(lat,lng, fromCoord, toCoord):
  result=dict()
  url = "http://apis.daum.net/maps/transcoord?apikey=DAUM_MAPS_DEMO_APIKEY&x="+lat+"&y="+lng
  url+="&fromCoord="+fromCoord+"&toCoord="+toCoord+"&output=xml"
  xml = urllib2.urlopen(url)
  soup = BeautifulSoup(xml)
  node=soup.findAll('result')[0]
  #print "/"+url
  if toCoord == "CONGNAMUL":
    result['x']=node['x']
    result['y']=node['y']
  else:
    result['lng']=node['x']
    result['lat']=node['y']
  return result  