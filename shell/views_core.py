from django.shortcuts import render_to_response, get_object_or_404
#from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required

from ppcat.shell.settings import PHOTO_SIZE, PHOTO_THUMBNAIL_SIZE, PHOTO_NUM_PER_PAGE, ALBUM_NUM_PER_PAGE
from ppcat.shell.models import Photo, Comment, Album
from ppcat.shell.forms import AlbumAddForm, AlbumEditForm, AlbumPhotoAddForm, PhotoAddForm, PhotoUploadEditForm, PhotoEditForm, CommentForm
from ppcat.shell.lib import EXIF

#from tempfile import TemporaryFile
from StringIO import StringIO
import os, Image, ImageFile

# Create your views here.
def index(request, page=1):
	template = 'index.django.html'
	photoAll = Photo.objects.order_by('-date_create')
	if not photoAll:
		photo = None
		return render_to_response(template, {
			'photo':photo
		}, context_instance=RequestContext(request))
	
	p = Paginator(photoAll, 1)
	
	try:
		page = int(page)
		currentPage = p.page(page)
	except InvalidPage:
		raise Http404
	photo = currentPage.object_list[0]
	
	return render_to_response(template, {
		'photo':photo,
		'currentPage':currentPage,
		#'currentPageNum':page,
		#'pageRange':p.page_range,
	}, context_instance=RequestContext(request))

def random(request):
	photoNum = Photo.objects.count()
	
	if photoNum == 0:
		return HttpResponseRedirect(reverse('index'))
	
	from random import randint
	page = randint(1, photoNum)
	
	return HttpResponseRedirect(reverse('index-page', args=[page]))

#################################################################################################
def photo(request, photoid=None):
	template = 'photo_single.django.html'
	photo = get_object_or_404(Photo, id=photoid)
	
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment()
			for k, v in form.cleaned_data.items():
				if hasattr(comment, k): setattr(comment, k, v)
			comment.photo = photo
			comment.save()
			form = CommentForm()
	else:
		form = CommentForm()

	photoComment = photo.comments.order_by('-date_create')
	
	return render_to_response(template, {
		'photo':photo,
		'photoComment':photoComment,
		'form':form
	}, context_instance=RequestContext(request))

def photoall(request, page=1):
	template = 'photo_all.django.html'
	photoAll = Photo.objects.order_by('-date_create')
	if not photoAll:	
		currentPage = None
		return render_to_response(template, {
			'currentPage':currentPage
		}, context_instance=RequestContext(request))
	
	p = Paginator(photoAll, PHOTO_NUM_PER_PAGE)
	page = int(page)
	
	try:
		currentPage = p.page(page)
	except InvalidPage:
		raise Http404
	
	return render_to_response(template, {
		'currentPage':currentPage,
		'currentPageNum':page,
		'pageRange':p.page_range,
	}, context_instance=RequestContext(request))

#######################################################################################################
def album(request, albumid=None):
	template = 'album_single.django.html'
	album = get_object_or_404(Album, id=albumid)
	
	return render_to_response(template, {
		'album':album
	}, context_instance=RequestContext(request))
	
def albumall(request, page=1):
	template = 'album_all.django.html'
	albumAll = Album.objects.order_by('-date_create')
	if not albumAll:
		currentPage = None
		return render_to_response(template, {
			'currentPage':currentPage
		}, context_instance=RequestContext(request))
	
	p = Paginator(albumAll, ALBUM_NUM_PER_PAGE)
	page = int(page)
	
	try:
		currentPage = p.page(page)
	except InvalidPage:
		raise Http404
	
	return render_to_response(template, {
		'currentPage':currentPage,
		'currentPageNum':page,
		'pageRange':p.page_range
	}, context_instance=RequestContext(request))

@login_required
def album_add(request):
	template = 'album_add.django.html'
	
	return render_to_response(template, {
		'form':AlbumAddForm()
	}, context_instance=RequestContext(request))
	
@login_required
def album_edit(request, albumid=None):
	template_album_edit = 'album_edit.django.html'
	
	album = get_object_or_404(Album, id=albumid)
	form = AlbumEditForm({
						'title':album.title,
						'description':album.description,
					})
	return render_to_response(template_album_edit, {
		'form':form,
		'album':album,
	}, context_instance=RequestContext(request))			

@login_required
def album_delete(request, albumid=None):
	album = get_object_or_404(Album, id=albumid)
	album.delete()
	# album.owner BUG
	return HttpResponseRedirect(reverse('albumall'))

@login_required
def album_save(request, albumid=None):
	template_album_add = 'album_add.django.html'
	template_album_edit = 'album_edit.django.html'
	
	if request.method != 'POST':
		if albumid:
			return HttpResponseRedirect(reverse('album', args=[albumid]))
		else:
			return HttpResponseRedirect(reverse('albumall'))
	
	if albumid:
		if request.POST.get('cancel', None):
			return HttpResponseRedirect(reverse('album', args=[albumid]))
	
		album = get_object_or_404(Album, id=albumid)
		form = AlbumEditForm(request.POST)
		if not form.is_valid():
			return render_to_response(template_album_edit, {
				'form':form,
				'album':album
			}, context_instance=RequestContext(request))
		
		for k, v in form.cleaned_data.items():
			if hasattr(album, k): setattr(album, k, v)
		album.save()
		return HttpResponseRedirect(reverse('album', args=[albumid]))
	else:
		if request.POST.get('cancel', None):
			return HttpResponseRedirect(reverse('albumall'))
		
		form = AlbumAddForm(request.POST)
		if not form.is_valid():
			return render_to_response(template_album_add, {
				'form':form
				}, context_instance=RequestContext(request))			
		album = Album()	
		for k, v in form.cleaned_data.items():
			if hasattr(album, k): setattr(album, k, v)
		album.save()
		return HttpResponseRedirect(reverse('album', args=[album.id]))

@login_required
def album_photo_add(request, albumid=None):
	template = 'album_photo_add.django.html'
	
	album = get_object_or_404(Album, id=albumid)
	
	return render_to_response(template, {
		'form':AlbumPhotoAddForm(),
		'album':album
	}, context_instance=RequestContext(request))
	
#######################################################################################################
@login_required
def photo_add(request):
	template = 'photo_add.django.html'
	
	#albumAll = Album.objects.order_by('-date_create')
	albumCount = Album.objects.count()
	
	return render_to_response(template, {
		'form':PhotoAddForm(),
		'albumCount':albumCount
	}, context_instance=RequestContext(request))

@login_required
def photo_upload_edit(request):
	template = 'photo_upload_edit.django.html'
	template_album_photo_add = 'album_photo_add.django.html'
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	if request.POST.get('cancel', None):
		return HttpResponseRedirect(reverse('album', args=[request.POST.get('albumid')]))
	
	form = AlbumPhotoAddForm({}, request.FILES)
	
	if not form.is_valid() or request.FILES['image']['content-type']!='image/jpeg':
		album = get_object_or_404(Album, id=request.POST.get('albumid'))
		return render_to_response(template_album_photo_add, {
			'form':form,
			'album':album
		}, context_instance=RequestContext(request))
	
		#if request.FILES and request.FILES['image']['content-type']=='image/jpeg':
	image = request.FILES['image']
	photo = Photo()
	
	# Extract EXIF info..read(num_bytes=None)['content']
	buffImageRaw = StringIO(image['content'])
	exif = {
		'Image Make':'manufacturer',
		'Image Model':'model',
		'EXIF DateTimeDigitized':'date_time',
		'EXIF ExposureTime':'exposure_time',
		'EXIF FNumber':'apeture',
		'EXIF FocalLength':'focal_length',
		'EXIF ISOSpeedRatings':'iso'
	}
	
	tags = EXIF.process_file(buffImageRaw, details=False)
	for t, p in exif.items():
		if t in tags:
			setattr(photo, p, tags[t])
		else:
			setattr(photo, p, 'N/A')
	photo.album = get_object_or_404(Album, id=request.POST.get('albumid'))
	photo.user = request.user
	photo.save()
	
	# Create a Image object to save photo & thumbnail.
	p = ImageFile.Parser()
	p.feed(image['content'])
	i = p.close()
	
	width, height = i.size # Get the size of original image.
	# Resize and save a photo.
	if width <= PHOTO_SIZE[0] and height <= PHOTO_SIZE[1]:
		photo.save_image_file(image['filename'], image['content'])
	else:
		buffImage = StringIO()
		i.thumbnail(PHOTO_SIZE, Image.ANTIALIAS)
		i.save(buffImage, 'JPEG', quality=95)
		photo.save_image_file(image['filename'], buffImage.getvalue())
	
	width, height = i.size # Get image size again in case the resize.
	# Crop, resize and save a photo thumbnail.
	if width == height:
		i.thumbnail(PHOTO_THUMBNAIL_SIZE, Image.ANTIALIAS)
	# horizontal photo
	elif width > height:
		i=i.crop(((width-height)/2, 0, (width-height)/2+height, height))
		i.thumbnail(PHOTO_THUMBNAIL_SIZE, Image.ANTIALIAS)
	# vertical photo
	else:
		i=i.crop((0, (height-width)/2, width, (height-width)/2+width))
		i.thumbnail(PHOTO_THUMBNAIL_SIZE, Image.ANTIALIAS)
		
	buffImageThumbnail = StringIO()
	i.save(buffImageThumbnail, 'JPEG', quality=95)
	filename, ext = os.path.splitext(image['filename'])
	photo.save_image_thumbnail_file(filename +'.thumbnail' + '.jpg', buffImageThumbnail.getvalue())
	
	return render_to_response(template, {
		'photo':photo,
		'form':PhotoUploadEditForm(),
		#'imageName':request.FILES['image']['filename'],
		#'tags':tags
	}, context_instance=RequestContext(request))


@login_required
def photo_upload_save(request, photoid=None):
	template_upload_edit = 'photo_upload_edit.django.html'
	
	photo = get_object_or_404(Photo, id=photoid)
	
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	if request.POST.get('cancel', None):
		if photo.user == request.user:
			photo.delete()
			return HttpResponseRedirect(reverse('album-photo-add', args=[request.POST.get('albumid')]))
	
	form = PhotoUploadEditForm(request.POST)
	if not form.is_valid():
		return render_to_response(template_upload_edit, {
			'form':form,
			'photo':photo
		}, context_instance=RequestContext(request))
	
	album = get_object_or_404(Album, id=int(request.POST.get('albumid'))) #BUG: Inital photo upload.
	if request.POST.get('isAlbumCover', ''): album.cover = photo
	album.save()
	
	for k, v in form.cleaned_data.items():
		if hasattr(photo, k): setattr(photo, k, v)
	photo.save()
	return HttpResponseRedirect(reverse('photo', args=[photoid]))

@login_required
def photo_edit(request, photoid=None):
	template = 'photo_edit.django.html'
	
	photo = get_object_or_404(Photo, id=photoid)
	if photo == photo.album.cover:
		isAlbumCover = True
	else:
		isAlbumCover = False
		
	form = PhotoEditForm({
		'caption':photo.caption,
		'description':photo.description,
		'isAlbumCover':isAlbumCover
	})
	
	return render_to_response(template, {
		'photo':photo,
		'form':form
	}, context_instance=RequestContext(request))

@login_required
def photo_save(request, photoid=None):
	template_edit = 'photo_edit.django.html'
	
	photo = get_object_or_404(Photo, id=photoid)
	
	if request.method != 'POST' or request.POST.get('cancel', None):
		return HttpResponseRedirect(reverse('photo', args=[photoid]))
	
	form = PhotoEditForm(request.POST)
	if not form.is_valid():
		return render_to_response(template_edit, {
			'form':form,
			'photo':photo
		}, context_instance=RequestContext(request))
	
	album = get_object_or_404(Album, id=int(request.POST.get('albumid')))
	if request.POST.get('isAlbumCover', ''):
		album.cover = photo
	else:
		album.cover = None
	album.save()
	
	for k, v in form.cleaned_data.items():
		if hasattr(photo, k): setattr(photo, k, v)
	photo.save()
	return HttpResponseRedirect(reverse('photo', args=[photoid]))


@login_required
def photo_delete(request, photoid=None):
	photo = get_object_or_404(Photo, id=photoid)
	albumid = photo.album.id
	
	if photo == photo.album.cover:
		photo.album.cover = None
		photo.album.save()
	
	if photo.user == request.user:
		photo.delete()
	
	return HttpResponseRedirect(reverse('album', args=[albumid]))
#	return HttpResponseRedirect(reverse('albumall'))

#def photo_comment_save(request, photoid=None):
#	photo = get_object_or_404(Photo, id=photoid)
#	comment = Comment()
#	for k, v in request.REQUEST.items():
#		if hasattr(comment, k): setattr(comment, k, v)
#	comment.photo = photo
#	comment.save()
#	
#	return HttpResponseRedirect(reverse('photo', args=[photoid]))