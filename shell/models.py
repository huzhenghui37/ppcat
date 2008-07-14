from django.db import models
from django.contrib.auth.models import User
#from django.db.models import permalink

from settings import PHOTO_UPLOAD_TO, PHOTO_THUMBNAIL_UPLOAD_TO, ALBUM_COVER_UPLOAD_TO

# Create your models here.
class Photo(models.Model):
	date_create = models.DateTimeField('Create Date', auto_now_add=True)
	image = models.ImageField(upload_to=PHOTO_UPLOAD_TO)
	image_thumbnail = models.ImageField(upload_to=PHOTO_THUMBNAIL_UPLOAD_TO, height_field='32', width_field='32', null=True, blank=True)
	
	manufacturer = models.CharField('Camera Manufacturer', max_length=25, blank=True)
	model = models.CharField('Camera Model', max_length=35, blank=True)
	date_time = models.CharField('Photo Date',max_length=20, blank=True)
	exposure_time = models.CharField('Exposure Time', max_length=10, blank=True)
	apeture = models.CharField('Apeture Value(FNumber)', max_length=10, blank=True)
	focal_length = models.CharField('Focal lenght', max_length=10, blank=True)
	iso = models.CharField('ISO', max_length=5, blank=True)
	HOLD_CHOICES = (('h','Handheld'), ('t', 'Tripod'))
	hold = models.CharField(max_length=10, choices=HOLD_CHOICES, blank=True)
	
	caption = models.CharField('Caption', max_length=50)
	description = models.TextField('Description', blank=True)
	
	album = models.ForeignKey('Album', related_name='photos')
	user = models.ForeignKey(User, related_name='owner')
	
	@models.permalink
	def get_absolute_url(self):
		return ('ppcat.shell.views_core.photo', [str(self.id)])

	def __unicode__(self):
		return u'%s %s %s %s' % (self.id, self.date_time, self.caption, self.description)

	class Admin:
		list_display = ('id', 'date_create', 'date_time', 'caption', 'description', 'album', 'user')
	
	class Meta:
		#get_latest_by = 'date_time'
		get_latest_by = 'date_create'


class Album(models.Model):
	date_create = models.DateTimeField('Create Date', auto_now_add=True)
	title = models.CharField('Album Title', max_length=50)
	description = models.TextField('Album Description', blank=True)
	cover = models.ForeignKey(Photo, related_name='album_cover', null=True, blank=True)
	#user = models.ForeignKey(User, related_name='owner')

	@models.permalink
	def get_absolute_url(self):
		return ('ppcat.shell.views_core.album', [str(self.id)])
	
	def __unicode__(self):
		return self.title
	
	class Admin:
		list_display = ('id', 'date_create', 'title', 'description')

	class Meta:
		get_latest_by = 'date_create'


class Comment(models.Model):
	date_create = models.DateTimeField('Create Date', auto_now_add=True)
	name = models.CharField(max_length=30)
	email = models.EmailField()
	website = models.URLField(blank=True)
	content = models.TextField(max_length=1000, blank=True)
	photo = models.ForeignKey(Photo, related_name='comments')
	
	class Admin:
		list_display = ('id', 'date_create', 'name', 'email', 'photo')
	
	class Meta:
		get_latest_by = 'date_create'	