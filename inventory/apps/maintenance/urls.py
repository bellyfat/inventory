#
# maintenance/urls.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#----------------------------------

from django.conf.urls import include, url

from inventory.apps.maintenance.views import purge, confirm, delete


urlpatterns = [
    url(r'^purge/$', purge),
    url(r'^confirm/$', confirm),
    url(r'^delete/$', delete),
    ]
