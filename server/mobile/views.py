from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from forms import *
from models import *

import json

def index(request):
  return HttpResponse("Index")
#direction_test
def direction_test(request):
  t = loader.get_template('google.maps.html')
  context = RequestContext(request)
  return HttpResponse(t.render(context))
  
def test(request):
  t = loader.get_template('test.html')
  context = RequestContext(request)
  context['register_user_form'] = UserRegisterForm()
  context['follow_form'] = FollowForm()
  context['gps_form'] = GPSForm()
  context['delete_log_form'] = DeleteLogForm()
  return HttpResponse(t.render(context))
  
def register_user(request):
  result=dict()
  result['code']=0
  result['message']='success'

  if request.method == 'POST':
    check = ['device_id','name','depart_lat','depart_lng','dest_lat','dest_lng']
    inputs = dict() 
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print '* '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return HttpResponse(json.dumps(result, indent=4))

  try:
    user=User.objects.filter(device_id=inputs['device_id'])
    if not user.count():
      new_user=User(device_id=inputs['device_id'],name=inputs['name'],depart_lat=inputs['depart_lat'],depart_lng=inputs['depart_lng'],dest_lat=inputs['dest_lat'],dest_lng=inputs['dest_lng'],status=Status.objects.get(code=0))
      new_user.save()
      print 'registered user: '+new_user.name
    else:
      print 'already user: '+user[0].name
      result['code']=1
      result['message']='already registered user: '+user[0].name+'(device_id:'+user[0].device_id+')'
      return HttpResponse(json.dumps(result, indent=4))
  except:
      print 'db error'
      result['code']=1
      result['message']='db error'

  return HttpResponse(json.dumps(result, indent=4))

  
def follow(request):
  result=dict()
  result['code']=0
  result['message']='success'
  
  if request.method == 'POST':
    check = ['provider','follower']
    inputs = dict() 
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print '* '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return HttpResponse(json.dumps(result, indent=4))

  try:
    provider=User.objects.get(device_id=inputs['provider'])
    follower=User.objects.get(device_id=inputs['follower'])
    follow=Follow.objects.filter(provider=provider,follower=follower).count()
    if not follow:
      new_follow=Follow(provider=provider,follower=follower)
      new_follow.save()
      print follower.name + ' follows ' + provider.name
    else:
      result['code']=1
      result['message']=follower.device_id + ' already follows ' + provider.device_id
      return HttpResponse(json.dumps(result, indent=4))
  except:
    print 'no such user '+inputs['provider']+' or '+inputs['follower']
    result['code']=1
    result['message']='Error: No such user: '+inputs['provider']+' or '+inputs['follower']
    return HttpResponse(json.dumps(result, indent=4))
  
  return HttpResponse(json.dumps(result, indent=4))

  
def unfollow(request):
  result=dict()
  result['code']=0
  result['message']='success'

  if request.method == 'POST':
    check = ['provider','follower']
    inputs = dict() 
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print '* '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return HttpResponse(json.dumps(result, indent=4))

  print '--------------------'

  try:
    provider=User.objects.get(device_id=inputs['provider'])
    follower=User.objects.get(device_id=inputs['follower'])
    follow=Follow.objects.get(provider=provider,follower=follower)
    follow.delete()
    print follower.name + ' unfollowed ' + provider.name
  except:
    print 'no such following'
    result['code']=1
    result['message']='Error: No such following: '+inputs['provider']+' with '+inputs['follower']
    return HttpResponse(json.dumps(result, indent=4))
    
  return HttpResponse(json.dumps(result, indent=4))
  
  
def delete_log(request):
  result=dict()
  result['code']=0
  result['message']='success'
  
  if request.method == 'POST':
    check = ['device_id']
    inputs = dict()
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print '* '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return HttpResponse(json.dumps(result, indent=4))

  try:
    user=User.objects.get(device_id=inputs['device_id'])
    GPSLog.objects.filter(user=user).delete()
    print 'Deleted Logs: '+user.name
  except:
    print 'no such user'
    result['code']=1
    result['message']='Error: No such user: '+inputs['device_id']
    return HttpResponse(json.dumps(result, indent=4))
    
  return HttpResponse(json.dumps(result, indent=4))
  
  
def delete_user(request):
  result=dict()
  result['code']=0
  result['message']='success'
  
  if request.method == 'POST':
    check = ['device_id']
    inputs = dict()
    for item in check:
      if request.POST[item]:
        value = request.POST[item]
        print item+': '+value
        inputs[item]=value
      else:
        print '* '+item+' is missing'
        result['code']=1
        result['message']='Error: Parameter '+item+' is missing'
        return HttpResponse(json.dumps(result, indent=4))

  try:
    user=User.objects.get(device_id=inputs['device_id'])
    user.delete()
    print 'Deleted User: '+user.name
  except:
    print 'no such user'
    result['code']=1
    result['message']='Error: No such user: '+inputs['device_id']
    return HttpResponse(json.dumps(result, indent=4))
    
  return HttpResponse(json.dumps(result, indent=4))
