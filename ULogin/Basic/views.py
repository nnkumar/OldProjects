# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.auth.models import User,auth, get_hexdigest, check_password

from ULogin.Uid.models import Recovery
from ULogin.Uid.views import myencrypt, mydecrypt

from ULogin.Basic.models import DeletedUser


#delete all accounts of the user first
def delete_account(request):
   if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
   cncl=request.GET.get('cancel','')
   if (not(cncl =="goahead")):
	return HttpResponseRedirect('/home/')
   usr=request.user
   deluser= DeletedUser()
   deluser.username=usr
   deluser.email=usr.email
   deluser.save()
   usr.delete()
   return render_to_response("login.html",{'Errstatus':"Your account and all the data has been successfully deleted"})



def genkey16():
   from random import randint
   return str(randint(1000000000000000, 9999999999999999))

def mymail(frmaddr,toaddr,mail):
   import smtplib
   server = smtplib.SMTP('smtp5.webfaction.com')
   server.login('vivekcse','9995219690')
   server.sendmail(frmaddr,toaddr,mail)
   server.quit()

def red2login(request):
  return HttpResponseRedirect('/login/')

def red2home(request):
  return HttpResponseRedirect('/home/')

def accrecv(request):
   uname = request.GET.get('uname','')
   rkey = request.GET.get('rkey','')
   if not(len(rkey)==16):
	return HttpResponse("Error")
   try:
	user = User.objects.get(username=uname)
   except:
	return HttpResponse("Error")
   Rec  = Recovery.objects.get(user=user)
   if not(check_password(rkey,Rec.mailhashkey)):
	return HttpResponse("Error")
   pwd = mydecrypt(rkey,Rec.mailencpass)
   body = 'Your password is "'+pwd+'". Login using this password'
   mymail('accounts@usingin.com',user.email,body)
   return HttpResponse("Send")


	

def setrecv(request):
   if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
   user = request.user
   pwd = request.GET.get('pwd','')
   tomail = request.GET.get('email','')
   if pwd == '':
	return render_to_response("SET/set_recv.html",{"mailid":user.email})
   if not(user.check_password(pwd)):
        return HttpResponse("Error")
   #pass ok, now gen key and mail
   key = genkey16()
   try:
	Rec = Recovery.objects.get(user=user)
   except:
   	Rec = Recovery()
   Rec.user = user
   Rec.mailhashkey = myhash(key)
   Rec.mailencpass = myencrypt(pwd,key)
   Rec.save()
   user.email = tomail
   user.save()
   body="Your recovery key is"+key+".Keep it safe for future use"
   mymail('accounts@usignin.com',tomail,body)
   #body="The key have been sent to your email"
   return HttpResponse("Send")	
   







        
""" Moved to Uid-->
def home(request):
   if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/login/')
   s=Account.objects.filter(user=request.user)
   return render_to_response("Uid/home.html",{"user":request.user,"accounts":s})	
"""

def validate(request,user=''):
        if  User.objects.filter(username=user):
             return  HttpResponse("Sorry, Username taken")
	else:
	     return HttpResponse("avail")



def signup(request):
	errstatus=''
        user = request.POST.get('un','')
        pwd  = request.POST.get('pw','')
        capchl = request.POST.get('recaptcha_challenge_field',''
)
        capresp =request.POST.get('recaptcha_response_field','')
        remoteip = request.META.get('REMOTE_ADDR')
        PRVKEY='6LcGVAMAAAAAAJKUBJ1p5rJGBI3Zq_R3AGU--vD9'
        if user:
          from ULogin.Basic.captcha import checkcaptcha
          if  User.objects.filter(username=user):
                errstatus="Username exists"
          elif (not(checkcaptcha(capchl,capresp,PRVKEY,remoteip))
):
                errstatus = "Wrong matching in Humanness test"
	  else:
                u = User.objects.create_user(user,'',pwd)
                u.save()
		return mylogin(request,user,pwd)
        dic = {"un":user,"pw":pwd,"Errstatus":errstatus}
        return render_to_response("signup.html",dic)







#New in V3
def sl2encrypt(pwd,key):
  from Crypto.Cipher import AES
  from pickle import dumps
  obj=AES.new(key, AES.MODE_ECB)
  pwd= obj.encrypt((pwd))
  pwd = dumps(pwd)
  return pwd

def sl2decrypt(key , pin):
  #key=request.COOKIES["MKD1597"]
  from Crypto.Cipher import AES
  from pickle import loads
  from hashlib import md5
  pin = md5(pin).hexdigest()
  obj = AES.new(pin, AES.MODE_ECB)
  key = loads(str(key))
  return obj.decrypt(key)

def myhash(pin):
   import random
   salt = get_hexdigest('sha1', str(random.random()), str(random.random()))[:5]
   #check_password(raw_password, self.password)
   hsh = get_hexdigest('sha1', salt, pin)
   return '%s$%s$%s' % ('sha1', salt, hsh)


def sl2create(user, pin ,key):
  from hashlib import  md5
  #pw = sha1(pw).hexdigest()
  #request.session["MKD1597"]
  try:
        slu=SLtwo.objects.get(user=user)
        slu.pin=myhash(pin)
  except:
        slu=SLtwo(user=user,pin=myhash(pin))
  #key = md5(pw).hexdigest()
  slu.enckey = sl2encrypt(key, md5(pin).hexdigest())
  slu.save()
  return


def settings(request):
  if not(request.user.is_authenticated()):
     return HttpResponseRedirect('/loggedout/')
  user=request.user
  if request.GET.get('Submit','')=='':
     dict={"fn":user.first_name,"ln":user.last_name,"mail":user.email,"pw":user.password,"user":user}
     return render_to_response("SET/settings.html",dict)
  user.first_name=request.GET.get('fn',user.first_name)
  user.last_name=request.GET.get('ln',user.last_name)
  user.email=request.GET.get('mail',user.email)
  user.save()   
  return HttpResponseRedirect("/home/")

""" of no use:
def setprof(request):
  if not(request.user.is_authenticated()):
     return HttpResponseRedirect('/loggedout/')
  user=request.user
  if request.GET.get('Submit','')=='':
     dict={"fn":user.first_name,"ln":user.last_name,"mail":user.email,"pw":user.password}
  return render_to_response("SET/set_prof.html",dict)
"""

#V3 new
def setpass(request):
  if not(request.user.is_authenticated()):
     return HttpResponseRedirect('/loggedout/')
  from ULogin.Uid.views import myencrypt, mydecrypt
  from ULogin.Uid.models import Account
  oldpw= request.GET.get('oldpw','')
  newpw= request.GET.get('pw','')
  pin= request.GET.get('pin','')
  user=request.user
  if not(user.check_password(oldpw)):
	return HttpResponse("Erpass")
  	#return HttpResponseRedirect("/home/")
  from hashlib import md5
  newkey = md5(newpw).hexdigest()
  #new V5
  try:
        slu= SLtwo.objects.get(user=user)
	if not(check_password(pin,slu.pin)):
		return HttpResponse("Erpin")
        slu.enckey=sl2encrypt(newkey, md5(pin).hexdigest())
        slu.save()
  except:
  	#if not(pin=='Only if you have set sl2 pin' or pin=''):
        pass	 #till here

  accounts=Account.objects.filter(user=user)
  for ac in accounts:
  	ac.password= myencrypt(mydecrypt(request.session["MKD1597"],
			ac.password),newkey)
	ac.save()
  request.session["MKD1597"]=newkey
  user.set_password(newpw)
  user.save()
  return HttpResponseRedirect('/home/')

  
def prelogin(request,template_name):
	print "OK"
        pw = request.POST.get('password')
	if(pw=='' or pw==None):
		return auth.login(request,template_name)
        from hashlib import md5
        pw = md5(pw).hexdigest()
        request.session["MKD1597"] = pw
	return auth.login(request,template_name)


#need to change-->

def mylogin(request,username,password):
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/home/")
        else:
                return HttpResponseRedirect("/login/")
    return render_to_response("login.html", {
        "username":username,
        "password":password,
        })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

