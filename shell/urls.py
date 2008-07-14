from django.conf.urls.defaults import *
#from ppcat.ing.feeds import LatestEntries

#feeds = {
#	'latest': LatestEntries,
#}

urlpatterns = patterns('ppcat.shell.views_core',
	url(r'^$',										'index', 				name='index'),
	url(r'^(?P<page>\d*)/$',						'index',				name='index-page'),
	url(r'^random/$',								'random',				name='random'),
	
	url(r'^album/(?P<albumid>\d*)/$',				'album',				name='album'),
	url(r'^albumall/$',								'albumall',				name='albumall'),
	url(r'^albumall/(?P<page>\d*)/$',				'albumall',				name='albumall-page'),
	url(r'^album/add/$',							'album_add',			name='album-add'),
	url(r'^album/(?P<albumid>\d*)/edit/$',			'album_edit',			name='album-edit'),
	url(r'^album/(?P<albumid>\d*)/delete/$',		'album_delete',			name='album-delete'),
	url(r'^album/save/$',							'album_save',			name='album-add-save'),
	url(r'^album/(?P<albumid>\d*)/save/$',			'album_save',			name='album-edit-save'),
	
	url(r'^album/(?P<albumid>\d*)/add/$',			'album_photo_add',		name='album-photo-add'),
	
	url(r'^photo/(?P<photoid>\d*)/$',				'photo', 				name='photo'),
	url(r'^photoall/$',								'photoall',				name='photoall'),
	url(r'^photoall/(?P<page>\d*)/$',				'photoall',				name='photoall-page'),
	
	url(r'^photo/add/$',							'photo_add',			name='photo-add'),
	url(r'^photo/upload/edit/$',					'photo_upload_edit',	name='photo-upload-edit'),
	url(r'^photo/upload/(?P<photoid>\d*)/save/$',	'photo_upload_save',	name='photo-upload-save'),
	
	url(r'^photo/(?P<photoid>\d*)/delete/$',		'photo_delete',			name='photo-delete'),
	url(r'^photo/(?P<photoid>\d*)/edit/$',			'photo_edit',			name='photo-edit'),
	url(r'^photo/(?P<photoid>\d*)/save/$',			'photo_save',			name='photo-save'),
	#url(r'^photo/(?P<photoid>\d*)/comment/save/$',	'photo_comment_save',	name='photo-comment-save')
	
#	(r'^js/latest/$',	'latest'),
)

urlpatterns += patterns('ppcat.shell.views.auth', # for user login/logout
	url(r'^login/(?P<redirect_to>[\w\/]*)$',		'login',				name='login'),
	url(r'^logout/$',								'logout',				name='logout'),
)

#urlpatterns += patterns('',
#	(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
#)
