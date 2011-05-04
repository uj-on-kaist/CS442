from django import forms 

class UserRegisterForm(forms.Form):
  device_id = forms.CharField(max_length=100,initial='test1')
  name = forms.CharField(max_length=100,initial="hi")
  depart_lat = forms.FloatField(initial=10.0)
  depart_lng = forms.FloatField(initial=10.0)
  dest_lat = forms.FloatField(initial=10.0)
  dest_lng = forms.FloatField(initial=10.0)
  
  
class FollowForm(forms.Form):
  provider = forms.CharField(max_length=100,initial='test1')
  follower = forms.CharField(max_length=100,initial='test2')
  
class GPSForm(forms.Form):
  device_id = forms.CharField(max_length=100,initial='test1')
  lat = forms.FloatField(initial=10.0)
  lng = forms.FloatField(initial=10.0)
  
class DeleteLogForm(forms.Form):
  device_id = forms.CharField(max_length=100,initial='test1')