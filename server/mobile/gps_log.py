from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from forms import *
from models import *

import json

def main(request):
  result=dict()

  result['register_result']=register_gps(request)  
  
  result['data']=following_data(request)
  
  return HttpResponse(json.dumps(result, indent=4))

def following_data(request):
  """
  result Dictionary
    -error
      - code 
        0: no error
        1: post error
        2: internal server error
      - message
    -following
      - user *
  """
  result=dict()
  result['error']=dict()
  result['error']['code']=0
  result['error']['message']='success'
  result['following']=list()
  print '--------------------'
  print 'Get GPS Logs following'
  device_id=request.POST['device_id']
  if device_id:
    request_user=''
    try:
      request_user=User.objects.get(device_id=device_id)
    except:
      result['error']['code']=1
      result['error']['message']='No such user: '+device_id
      return result
    
    users=Follow.objects.filter(follower=request_user)
    for user in users:
      user_info=dict()
      user_info['device_id']=user.provider.device_id
      user_info['name']=user.provider.name
      user_info['status_code']=user.provider.status.code
      user_info['status_msg']=user.provider.status.msg
      logs=GPSLog.objects.filter(user=user.provider).order_by('reg_date')
      if logs.count():
        last_log=logs[0]
        user_info['lat']=last_log.lat
        user_info['lng']=last_log.lng
      result['following'].append(user_info)
      
  else:
    result['error']['code']=1
    result['error']['message']='empty device_id'
    return result
  print '--------------------'
  
  
  print '--------------------'
  
  return result

def register_gps(request):
  """
  result Dictionary
  - code 
    0: no error
    1: post error
    2: internal server error
  - message
  """
  result=dict()
  result['code']=0
  result['message']='success'
  
  print '--------------------'
  print 'Register GPS'
  if request.method == 'POST':
    check = ['device_id','lat','lng']
    inputs = dict() 
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print 'Error: * '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return result
        print '--------------------'
  print '--------------------'
  try:
    user=User.objects.get(device_id=inputs['device_id'])
    gps_log=GPSLog(user=user,lat=inputs['lat'],lng=inputs['lng'])
    gps_log.save()
    print 'saved log user: '+user.name
  except:
    print 'no such user'
    result['code']=1
    result['message']='Error: No such user: '+inputs['device_id']
    return result
  
  print '--------------------'
  return result