from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from ULogin.Uid.models import Account,Website

from urllib2 import urlopen
import re


def home(request):
   if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/login/')
   s=Account.objects.filter(user=request.user)
   return render_to_response("Uid/home.html",{"user":request.user,"accounts":s})



def change_site(site , url):
  if url.endswith('/'):
        url=url.rpartition('/')[0]
  if(not('http://' in url) and not('https://' in url)):
       	url='http://'+url
  if site.url == url:
	return site
  try:
        site= Website.objects.get(url=url)
  except:
        site=get_site(url)
  return site



def edit_account(request,sid):
  if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
  account=Account.objects.get(id=sid)
  url=request.GET.get('url','')
  if url=='':
     dict={"url":account.site.url,"accname":account.accname,"uname":account.username,"id":sid}
     return render_to_response("Uid/editsite.html",dict)
  #import pdb;pdb.set_trace()
  account.username=request.GET.get('uname','')
  acnm=request.GET.get('accname','')
  if acnm == '' or acnm == 'Optional-Url used if blank':
        if '://' in url:
        	acnm= url.partition('://')[2].partition('/')[0]
	else:
		acnm=url.partition('/')[0]
  account.accname=acnm
  account.site = change_site(account.site , url)
  pwd = request.GET.get('pwd','')
  if pwd == "Optional to change":
	pwd=''
  if not(pwd==''):
	  account.password = myencrypt(pwd, request.session["MKD1597"])
  account.save()
  return HttpResponseRedirect("/home/")
  



def del_account(request,sid):
  if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
  site=Account.objects.get(id=sid)
  site.delete()
  

def myencrypt(pwd,key):
  from Crypto.Cipher import AES
  from pickle import dumps
  obj=AES.new(key, AES.MODE_ECB)
  pwlen = len(pwd)
  if pwlen < 10:
	pwlen = '0' + str(pwlen)
  pwd= (pwd+"1234567891234567")[:14]+str(pwlen)
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



#V3 session key imp-->handle it 
def autologin(request,sid):
  #do authentication before giving access in all funcs
  acc=Account.objects.get(id=sid)
  f=acc.site.subform;
  un=acc.username;pw=mydecrypt(request.session["MKD1597"],acc.password)
 # import pdb;pdb.set_trace()
  t1=f.partition('type="text"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'.*?<input.*?text.*?value="".*?>',re.DOTALL)
  #patch
  r1=re.compile(r'<input[^>]*?text[^>]*?value=""[^>]*?/>',re.DOTALL)  #use regexp
  if(r1.match(p)):
     s=re.sub('value=""','value="'+un+'"',p,1) #use reg
     p=t2[0]+s
  else:
     p=t2[0]+t2[1]+' value="'+un+'"'+t2[2]+t1[1]+t1[2]
  #t1=p.partition('"password"')
  t1=p.partition('type="password"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'<input[^>]*?password[^>]*?value=""[^>]*?/>',re.DOTALL)
  r1=re.compile(r'<input[^>]*?password[^>]*?value=""[^>]*?/>',re.DOTALL) #reg use
  #not perfect the above value="" may cause prblm
  if(r1.match(p)):
     s=re.sub('value=""','value="'+pw+'"',p,1)  #use regx
     html=t2[0]+s
  else:
     html=t2[0]+t2[1]+' value="'+pw+'"'+t2[2]+t1[1]+t1[2]
  html='<div style="visibility:hidden">'+html+'</div>'
  return HttpResponse(html)


def public_autologin(request):
  url=request.POST.get('url')
  if(url=='' or url==None):
	if 'home' in request.META['PATH_INFO']:
		return render_to_response("Uid/openuvl.html",{"user":request.user})
	return render_to_response("openuvl.html")
  un=request.POST.get('uname')
  pw=request.POST.get('pwd')
  if(un=='' or pw==''):
	return HttpResponse("Enter valid form data")
  #f=url2form(url) #do this
  url=url.rpartition("http://")[2]
  url=url.rpartition("https://")[2]
  url=url.rpartition("www.")[2]

  #if(not('http://' in url) and not('https://' in url)):
  #      url='http://'+url
  try:
        site= Website.objects.get(url=url)
  except:
        site=get_site(url)
  if site==None:
        return HttpResponseRedirect('/home/')

  f=site.subform
  #f=acc.site.subform;
  t1=f.partition('type="text"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'.*?<input.*?text.*?value="".*?>',re.DOTALL)
  #patch
  r1=re.compile(r'<input[^>]*?text[^>]*?value=""[^>]*?/>',re.DOTALL)  #use regexp
  if(r1.match(p)):
     s=re.sub('value=""','value="'+un+'"',p,1) #use reg
     p=t2[0]+s
  else:
     p=t2[0]+t2[1]+' value="'+un+'"'+t2[2]+t1[1]+t1[2]
  #t1=p.partition('"password"')
  t1=p.partition('type="password"')
  t2=t1[0].rpartition("<input")
  p=t2[1]+t2[2]+t1[1]+t1[2]
  #r1=re.compile(r'<input[^>]*?password[^>]*?value=""[^>]*?/>',re.DOTALL)
  r1=re.compile(r'<input[^>]*?password[^>]*?value=""[^>]*?/>',re.DOTALL) #reg use
  #not perfect the above value="" may cause prblm
  if(r1.match(p)):
     s=re.sub('value=""','value="'+pw+'"',p,1)  #use regx
     html=t2[0]+s
  else:
     html=t2[0]+t2[1]+' value="'+pw+'"'+t2[2]+t1[1]+t1[2]
  html='<div style="visibility:hidden">'+html+'</div>'
  return HttpResponse(html)


#V3
def add_account(request):
  if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
  url=request.POST.get('url','')
  if(url==''):
	return render_to_response("Uid/addsite.html",{'user':request.user})
  uname = request.POST.get('uname','')
  pwd=request.POST.get('pwd','')
  if(uname=='' or pwd==''):
	return render_to_response("Uid/addsite.html",{'Errstatus':"Fields should be filled",'url':url,'user':request.user})
  #to rem trail 
  if url.endswith('/'):
        url=url.rpartition('/')[0]
  url=url.rpartition("http://")[2]
  url=url.rpartition("https://")[2]
  url=url.rpartition("www.")[2]
  
  #if(not('http://' in url) and not('https://' in url)):
  #      url='http://'+url

  try:
	site= Website.objects.get(url=url)
  except:
  	site=get_site(url)
  if site==None:
	return render_to_response("Uid/addsite.html",{'Errstatus':"Some error Occured.Check whether the url has a login form",'url':url,'user':request.user})
  	#return HttpResponseRedirect('/home/')
  user=request.user
  acnm  = request.POST.get('accname','')
  if acnm == '' or acnm == 'Optional-Url used if blank':
	acnm=url.partition('://')[2].partition('/')[0]
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


def saveIcon(url,data,contype,sid):
  import re,urlparse
  icourl=''
  if contype.startswith('text/html') or contype.startswith('application/xhtml+xml'):
            # Try to find any links to shortcut icons
            ICONREGEX = """<link rel="shortcut icon" (?:.*)href=(?:['|"])(.[^'|"|\s]{0,})(?:['|"])(?:.*)>"""
            results = re.search(ICONREGEX, data, re.I)
            if results != None:
                # Found the requested URL of the favourite icon
                icourl = results.groups()[0]
		icourl = urlparse.urljoin(url, icourl)
  if icourl=='':
	icourl = urlparse.urljoin(url, '/favicon.ico')
 
  tmp = urlopen(icourl).read()
  if ('html' in tmp) or ('body' in tmp) or ('head' in tmp):
	return 
  fp=open('/tmp/fav'+str(sid)+'.ico','w')
  fp.write(tmp)
  fp.close()
  return


def get_lgnform(site_source):
  #till here
  s = site_source
  #form extraction from site 's'
  reg_pw=re.compile(r"""type( )*=( )*('|")?( )*password('|")?""",re.I)
  reg_fstr=re.compile(r"<( )*form",re.I)
  reg_fend=re.compile(r"<( )*/( )*form( )*>")
  reg_actn=re.compile(r"action( )*=") #Ll
  fnd_pw=re.search(reg_pw,s) ;import pdb;pdb.set_trace()
  if(fnd_pw==None):
        #LFD and report login page not found+return
        print "None"
  fnd_str=re.search(reg_fstr,s[:fnd_pw.start()])
  fnd_end=re.search(reg_fend,s[fnd_pw.end():])
  f=s[fnd_str.start():(fnd_pw.end()+fnd_end.end())]
  return f


def get_lgnform(site_source):
  #till here
  s = site_source
  #form extraction from site 's'
  reg_pw=re.compile(r"""type( )*=( )*('|")?( )*password('|")?""",re.I)
  reg_fstr=re.compile(r"<( )*form",re.I)
  reg_fend=re.compile(r"<( )*/( )*form( )*>")
  reg_actn=re.compile(r"action( )*=") #Ll
  fnd_pw=re.search(reg_pw,s) 
  if(fnd_pw==None):
        #LFD and report login page not found+return
	return None 	# print "None"
  fnd_str=re.search(reg_fstr,s[:fnd_pw.start()])
  fnd_end=re.search(reg_fend,s[fnd_pw.end():])
  f=s[fnd_str.start():(fnd_pw.end()+fnd_end.end())]
  return f

#new
def get_site(url):
  geturl="http://"+url
  for i in range(4):
    try:
        fp=urlopen(geturl)
        break
    except IOError:
        print "IoError" ##do 4 times checking before returning failed(cant trust network)
        fp = None
  if fp==None:
        return None #handle it in calling func 
  #new in V4 for icon
  data=fp.read()
  hdr=fp.headers['content-type']
  endurl=fp.geturl()
  fp.close()
  #till here
  s = data
  f=get_lgnform(s)
  if f==None:
	pass #call LFD here
  

  #generalising of algn
  #generalising using reg exp
  #possible issues--> whn some id attrib(or js) has 'input' or 'value' in its name (not sure if CS)
  reg1=re.compile(r"input",re.I)
  f=re.sub(reg1,'input',f)
  reg1=re.compile(r"value",re.I)
  f=re.sub(reg1,'value',f)
  reg1=re.compile(r"""type( )*=( )*('|")?text('|")?""",re.I)
  f=re.sub(reg1,'type="text"',f)
  reg1=re.compile(r"""type( )*=( )*('|")?password('|")?""",re.I)
  f=re.sub(reg1,'type="password"',f)
  reg1=re.compile(r"""type( )*=( )*('|")?submit('|")?""",re.I)
  f=re.sub(reg1,'type="submit"',f)
  reg1=re.compile(r"""action( )*=( )*("|')""",re.I)
  f=re.sub(reg1,'action="',f)
  

  #newly added code to check for relative url in action
  #todo-> here also use regexp
  actn='action="'
  s=f.partition(actn)
  t1=s[2].partition('"')
  if not t1[0].startswith('/'):
	tmp='/'+t1[0]
  else:
	tmp=t1[0]
  if not("http" in t1[0]):
	f=s[0]+s[1]+endurl+tmp

  #new code to manage uvl_sub
  tysub='type="submit"'
  t1=f.partition(tysub)
  f= t1[0]+t1[1]+' id="uvl_sub" '+t1[2]
  #till here

  site=Website(url=url,subform=convert2asci(f))
  site.save()
  try:
	saveIcon(geturl,data,hdr,site.id)
  except:
	pass
  return site 

##TODO for regexp--> JS being case sensitive try to add space before all regexp

#new
def show_sites(request):
  if not(request.user.is_authenticated()):
          return HttpResponseRedirect('/loggedout/')
  s=Account.objects.filter(user=request.user)
  return render_to_response("Uid/sites.html",{"accounts":s})

def sites_lookup(request):
   # Default return list
  from django.db import connection
  from django.utils import simplejson
  print "OK"
  #import pdb;pdb.set_trace()
  results = []
  if request.method == "GET":
    if request.GET.has_key(u'query'):
          urlstart = request.GET[u'query']
          # Ignore queries shorter than length 3
          #if len(value) > 2:
          cursor = connection.cursor()
 	  cursor.execute("""select url from Uid_website where url like "%"""+urlstart+"""%" limit 12;""")
   	  results= cursor.fetchall()
 	  #cursor.execute("""select url from Uid_website where url like "%http://www."""+urlstart+"""%" limit 12;""")
   	  #results+= cursor.fetchall()
    json = simplejson.dumps(results)
    print results
    return HttpResponse(json, mimetype='application/json')



