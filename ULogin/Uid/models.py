from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Website(models.Model):
    url = models.URLField(verify_exists=True)
    subform = models.TextField()
    rank= models.IntegerField(blank=True, null=True)

    class Admin:
	pass

class Account(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Website)
    username = models.CharField(max_length=25)
    accname = models.CharField(max_length=35)
    password = models.CharField(max_length=64)

    #def __unicode__(self):

    class Admin:
	pass

class SLtwo(models.Model):
    user = models.ForeignKey(User,primary_key=True)
    pin = models.CharField(max_length=128)
    enckey = models.CharField(max_length=128)
      

    class Admin:
	pass


class Recovery(models.Model):
    user = models.ForeignKey(User,primary_key=True)
    mailhashkey = models.CharField(max_length=128)
    mailencpass = models.CharField(max_length=64)
    
    class Admin:
	pass

