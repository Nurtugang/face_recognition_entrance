import datetime
from time import time

from django.db import models

types = [('student','student'), ('okushy', 'okushy')]
st = [('pr', 'pr'), ('abs', 'abs'), ('late', 'late')]
class Profile(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField()
    status = models.CharField(choices=types,max_length=20,null=True,blank=False)
    st = models.CharField(choices=st,max_length=20,null=True,blank=False,default='abs')
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    shift = models.TimeField()
    def __str__(self):
        return self.first_name +' '+self.last_name


class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.last_face

