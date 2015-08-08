from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from ULogin.Uid.models import Account,Website

from urllib2 import urlopen
import re


#new in V3

def change_site(site , url):
  if url.endswith('/'):
        url=url.rpartition('/')[0]
  upref='http://'
  if(not(upref in url)):
        url=upref+url
  if site.url == url:
	return site
  try:
        site= Website.objects.get(url=url)
  except:
        site=get_site(url)
  return site



def edit_account(request,sid):
  if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/login/')
  account=Account.objects.get(id=sid)
  url=request.GET.get('url','')
  if url=='':
     dict={"url":account.site.url,"accname":account.accname,"uname":account.username,"id":sid}
     return render_to_response("Uid/uid_edit.html",dict)
  #import pdb;pdb.set_trace()
  account.username=request.GET.get('uname','')
  account.accname=request.GET.get('accname','')
  account.site = change_site(account.site , url)
  pwd = request.GET.get('pwd','')
  account.password = myencrypt(pwd, request.session["MKD1597"])
  account.save()
  return HttpResponseRedirect("/home/")
  



def del_account(request,sid):
  if not(request.user.is_authenticated()):
         return HttpResponseRedirect('/login/')
  site=Account.objects.get(id=sid)
  site.delete()
  

def myencrypt(pwd,key):
  from Crypto.Cipher import AES
  from pickle import dumps
  obj=AES.new(key, AES.MODE_ECB)
  #import pdb;pdb.set_trace()
  pwlen = len(pwd)
  if pwlen < 10:
	pwlen = '0' + str(pwlen)
  pwd= (pwd+"1234567891234567")[:14]+pwlen
  pwd= obj.encrypt((pwd))
  pwd = dumps(pwd)
  #pwd= unicode(pwd)
  return pwd
  

def mydecrypt(key,pwd):
  #key=request.COOKIES["MKD1597"]
  from Crypto.Cipher import AES
  from pickle import loads
  obj = AES.new(key, AES.MODE_ECB)
  pwd = loads(str(pwd))
  pwd = obj.decrypt(pwd)
  pwlen = int(pwd[len(pwd)-2] + pwd[len(pwd)-1])
  return pwd[:pwlen]



#V3 
def autologin(request,sid):
  #import pdb;pdb.set_trace()
  acc=Account.objects.get(id=sid)
  f=acc.site.subform;
  un=acc.username;pw=mydecrypt(request.session["MKD1597"],acc.password)
  t1=f.partition('"text"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'.*?<input.*?text.*?value="".*?>',re.DOTALL)
  #patch
  r1=re.compile(r'<input[^>]*?text[^>]*?value=""[^>]*?/>',re.DOTALL)
  if(r1.match(p)):
     s=re.sub('value=""','value="'+un+'"',p,1)
     p=t2[0]+s
  else:
     p=t2[0]+t2[1]+' value="'+un+'"'+t2[2]+t1[1]+t1[2]
  #t1=p.partition('"password"')
  t1=p.partition('type="password"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'<input[^>]*?password[^>]*?value=""[^>]*?/>',re.DOTALL)
  r1=re.compile(r'<input[^>]*?type="password"[^>]*?value=""[^>]*?/>',re.DOTALL)
  #not perfect the above value="" may cause prblm
  if(r1.match(p)):
     s=re.sub('value=""','value="'+pw+'"',p,1)
     html=t2[0]+s
  else:
     html=t2[0]+t2[1]+' value="'+pw+'"'+t2[2]+t1[1]+t1[2]
  #html='<div style="visibility:hidden">'+html+'</div>'
  return HttpResponse(html)




#V3
def add_account(request):
  if not(request.user.is_authenticated()):
         return HttpResponseRedirect('/login/')
  url=request.GET.get('url','')
  #to rem trail 
  if url.endswith('/'):
        url=url.rpartition('/')[0]
  upref='http://'
  if(not(upref in url)):
        url=upref+url
  try:
	site= Website.objects.get(url=url)
  except:
  	site=get_site(url)
  if site==None:
  	return HttpResponseRedirect('/home/')
  user=request.user
  acnm  = request.GET.get('accname','')
  if acnm == '':
	acnm=url
  uname = request.GET.get('uname','')
  pwd=request.GET.get('pwd','')
  pwd=myencrypt(pwd, request.session["MKD1597"])
  st=Account(user=user,accname=acnm,site=site,username=uname,password=pwd)
  st.save()
  return HttpResponseRedirect('/home/')

#new V4
def convert2asci(f):
  r = ' '
  for i in f:
    if ord(i)<129:
        r+=i
  return r


#new
def get_site(url):
  try:
	s=urlopen(url).read()
  except IOError:
	return None
  # rediff fix
  #s=s.lower()
  psplit='type="password"'
  if not(psplit in s):
	psplit='type=password'
  	if not(psplit in s):
		psplit="type=PASSWORD"
		if not(psplit in s):
			pssplit='type=PASSWORD'
			if not(psplit in s):
				pssplit="type = password"
  				if not(psplit in s):
					pssplit='type = password'
  #till here
  t1=s.partition(psplit)
  #generelizing new
  frmstrt="<form"
  if not(frmstrt in t1[0]):
	frmstrt="<FORM"
	if not(frmstrt in t1[0]):
		frmstrt="<Form"
  frmend="/form>"
  if not(frmend in t1[2]):
	frmend="/FORM>"
  #till here 


  f=frmstrt+(t1[0].rpartition(frmstrt)[2]+t1[1]+t1[2]).partition(frmend)[0]+frmend
  #newly added code to check for relative url in action
  actn='action="'
  if not (actn in f):
	actn='action ="'
	if not(actn in f):
		actn='action= "'
		if not( actn in f):
			actn='action = "'

  s=f.partition(actn)
  t1=s[2].partition('"')
  if not t1[0].startswith('/'):
	tmp='/'+t1[0]
  else:
	tmp=t1[0]
  if not("http" in t1[0]):
	f=s[0]+s[1]+url+tmp+t1[1]+t1[2]

  #generalising of algn
  if "INPUT" in f:
        f=re.sub("INPUT","input",f)
  if "TEXT" in f:
        f=re.sub("TEXT","text",f)
  if "PASSWORD" in f:
        f=re.sub("PASSWORD","password",f)
  if "VALUE" in f:
        f=re.sub("VALUE","value",f)

  site=Website(url=url,subform=convert2asci(f))
  site.save()
  return site 

#new
def show_sites(request):
  if not(request.user.is_authenticated()):
         return HttpResponseRedirect('/login/')
  s=Account.objects.filter(user=request.user)
  return render_to_response("Uid/sites.html",{"accounts":s})


