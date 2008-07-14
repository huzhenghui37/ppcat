from django.conf.urls.defaults import *

urlpatterns = patterns('',

#	(r'^$', include('ppcat.ing.urls')),
#	(r'^ing/', include('ppcat.ing.urls')),
	(r'^shell/', include('ppcat.shell.urls')),
	(r'^admin/', include('django.contrib.admin.urls')),
)
