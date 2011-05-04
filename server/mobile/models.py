from django.db import models


class Status(models.Model):
  code = models.IntegerField()
  msg = models.TextField()
  
class User(models.Model):
  device_id = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  depart_lat = models.FloatField()
  depart_lng = models.FloatField()
  dest_lat = models.FloatField()
  dest_lng = models.FloatField()
  status = models.ForeignKey(Status)
  
class Follow(models.Model):
  provider = models.ForeignKey(User, related_name='provider')
  follower = models.ForeignKey(User, related_name='follower')

class GPSLog(models.Model):
  user = models.ForeignKey(User)
  lat = models.FloatField()
  lng = models.FloatField()
  reg_date = models.DateTimeField(auto_now_add=True, auto_now=True)
  

  

