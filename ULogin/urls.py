from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login,logout

from Uid.views import home,add_account,show_sites,autologin,edit_account,del_account, sites_lookup,public_autologin
from Basic.views import signup,settings,validate, setpass, setrecv, accrecv,red2login,red2home,delete_account
from Dmail.views import search,delmail

urlpatterns = patterns('',
    # Example:
    # (r'^ULogin/', include('ULogin.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/nikhil/MAIN/PRJ/UVL/ULogin/media/'}),

                (r'^tos/$',direct_to_template, {'template':'tos.html' } ),
                (r'^contact/$',direct_to_template, {'template':'contact.html' } ),
		(r'^help/$',direct_to_template, {'template':'help.html' } ),
                (r'^mailrecv/$',setrecv),
		(r'^lookup$',sites_lookup),
		(r'^openuvl',public_autologin),
		(r'^home/openuvl',public_autologin),
		(r'^home/editsite/(\w+)/$',edit_account), #,',direct_to_template,{'template':'Uid/editsite.html'}),
		(r'^home/siteadd',add_account),#direct_to_template,{'template':'Uid/addsite.html'}),
		(r'^delaccount',delete_account),#direct_to_template,{'template':'Uid/addsite.html'}),

                (r'^uidcreate/$',direct_to_template, {'template':'Uid/uid_create.html' } ),
                (r'^siteadd/$',add_account),
                (r'^home/$',home),#direct_to_template,{'template':'Uid/home.html'}),
                (r'^sites/$',show_sites),
                (r'home/ulogin/(\w+)/$',autologin),
                (r'sedit/(\w+)/$',edit_account),
                (r'home/sdel/(\w+)/$',del_account),

                (r'^home/settings/$',settings),
		(r'^setpwd/$',direct_to_template,{'template': 'SET/set_pwd.html'}),
		(r'^setoid/$',direct_to_template,{'template': 'SET/set_oid.html'}),
		(r'^setdelacc/$',direct_to_template,{'template': 'SET/set_delacc.html'}),

		(r'^setrecv/$',setrecv),
		#(r'^setrecv/$',direct_to_template,{'template': 'SET/set_recv.html'}),
		(r'^recvform/$',direct_to_template,{'template': 'SET/accrecv.html'}),
		(r'^accrecv/$',accrecv),
                (r'^settings/$',settings),
                (r'^home/settings/$',settings),
                (r'^setpass/$',setpass),
                (r'^dmail/$',search),#,settings),
		(r'^delmail/(\w+)/',delmail),
                
	
		(r'^login/validate/(\w+)/',validate),
		(r'^signup/validate/(\w+)/',validate),

		(r'^register/$',direct_to_template,{'template': 'register.html'}),
		(r'^what/$',direct_to_template,{'template': 'what.html'}),
		(r'^faq/$',direct_to_template,{'template': 'faq.html'}),
		(r'^loggedout/$',direct_to_template,{'template': 'loggedout.html'}),
                (r'^login/signup1/$',signup),
                (r'^signup/$',signup),
                (r'^login/$',login,{"template_name": "login.html"}),
                (r'^logout/$',logout,{"next_page":"/login/"}),
                (r'^home',red2home),#direct_to_template,{'template':'Uid/home.html'}),
                (r'',red2login),


)
