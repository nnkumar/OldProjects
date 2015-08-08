from django.shortcuts import render_to_response 
import string
import poplib
import email
import email.Parser
import os
import sys
import re
from django.http import HttpResponse
def search(request):
    msg= ''
    msg1=''
    body=''
    query = request.GET.get('q','')  
    x = re.compile('From: [ .\"A-Za-z\',<>0-9]*')
#    y = re.compile('To: '+query+'@uid.co.in[a-z\', ]*')
    y = re.compile('To: [@.\"A-Za-z\',<>0-9 ]*'+query+'@usignin.com[ @.\"A-Za-z\',<>0-9]*')  
    z = re.compile('Subject: [@.\"A-Za-z\',<>0-9]*')
    m = re.compile('=(\n)+')
    k = re.compile('\nhttp://[=/\-@.\"A-Za-z\',<>0-9\?_&]*')
    if query:
	    pop3 = poplib.POP3('mail5.webfaction.com')
	    pop3.user('usignin')
	    pop3.pass_('asdf0987qwe')
	    num = len(pop3.list()[1])
	    if num == 0:	
	        emsg="No Message"
	        print emsg
	        sys.exit(emsg)
	    else:
		num1=0
	    	for i in range(1,num+1):
			inbox=pop3.retr(i)[1]
			t=pop3.retr(i)[1]
			for j in inbox:
				if y.search(j):
					for j in inbox:
						if x.match(j):
							j=j.replace('<',': ')
							j=j.replace('>','')
							msg1=msg1+"<br><HR color="#0000FF">"+j+"<br>"
					for j in inbox:
						if z.match(j):
							j=j.replace('?','')
						        j=j.replace('iso-8859-1q', '')	
		  					msg1=msg1+j+"<br>"+"Body:  "
			
					num1+=1
		#			for i in inbox:
	#					i=m.sub('',i)
#						if k.match(i):
#							tmp=i
							
#							i="<a href="+tmp+">"+tmp+"</a>"
#							return HttpResponse(i)
					msglines='\n'.join(t)
					msg=email.Parser.Parser().parsestr(msglines)					
					if msg.is_multipart():	
						attachmentnum=0
						for part in msg.walk():
							mptype=part.get_content_maintype()
							body=part.get_payload()
					else:
						
						body=msg.get_payload()
				       # body= body.replace('=','')
					msg1=msg1+body
	        delmsg="""<ul id="maintab">
<li><a href="#" onclick="return ajax_fetch('/delmail/"""+query+"""/');" >DELETE ALL</a></li></ul>"""
		if(num1==0):
			delmsg=''
		msg1="You've got "+str(num1)+" messages"+delmsg+msg1+"<HR color="#0000FF">"
#	        msg1+="""<a href="#" onclick="return ajax_fetch('/delmail/"""+query+"""/');" >Dmail</a>"""

		msg1=m.sub('',msg1)		
		msg1=msg1.replace('3D','')
		a=k.search(msg1)
		if a:
		    tmp=a.group(0)
		    i="<a href="+tmp+">"+tmp+"</a>"
		    msg1=k.sub(i,msg1)
		return HttpResponse(msg1)
    else:
	    num=0
    return render_to_response("dmail.html", {
	"query": query,
})




def delmail(request,query):
    msg= ''
    msg1=''
    body=''
    x = re.compile('From: [ .\"A-Za-z\',<>0-9]*')
    y = re.compile('To: [@.\"A-Za-z\',<>0-9 ]*'+query+'@usignin.com[ @.\"A-Za-z\',<>0-9]*')  
    z = re.compile('Subject: [@.\"A-Za-z\',<>0-9]*')
    m = re.compile('=(\n)+')
    k = re.compile('\nhttp://[=/\-@.\"A-Za-z\',<>0-9\?_&]*')
    if query:
	    pop3 = poplib.POP3('mail5.webfaction.com')
	    pop3.user('usignin')
	    pop3.pass_('v3an6420')
	    num = len(pop3.list()[1])
	    if num == 0:	
	        emsg="No Message"
	        print emsg
	        sys.exit(emsg)
	    else:
		num1=0
	    	for i in range(1,num+1):
			inbox=pop3.retr(i)[1]
			t=pop3.retr(i)[1]
			for j in inbox:
				if y.search(j):
					#import pdb;pdb.set_trace()
					pop3.dele(i)
		pop3.quit()
		return HttpResponse("All mails deleted")
    else:
	    num=0
    return render_to_response("dmail.html", {
	"query": query,
})
