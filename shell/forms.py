from django import newforms as forms
from ppcat.shell.models import Album


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)

################################################################
class AlbumForm(forms.Form):
	title = forms.CharField(max_length=50)
	description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'6', 'cols':'50'}))

class AlbumAddForm(AlbumForm):
	pass

class AlbumEditForm(AlbumForm):
	pass

#################################################################
class AlbumPhotoAddForm(forms.Form):
	image = forms.ImageField()


albumAll = Album.objects.order_by('-date_create')
albumAllList = [ (a.id, a.title) for a in albumAll ]

class PhotoAddForm(forms.Form):
	image = forms.ImageField()
	albumid = forms.ChoiceField(required=False, widget=forms.Select, choices=albumAllList)

class PhotoEditForm(forms.Form):
	caption = forms.CharField(max_length=50)
	description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'6', 'cols':'50'}))
	isAlbumCover = forms.BooleanField(label='As album cover', required=False)

class PhotoUploadEditForm(PhotoEditForm):
	hold = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=(('h','Handheld'), ('t','Tripod')))
	
############################################################
class CommentForm(forms.Form):
	name = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=75)
	website = forms.URLField(max_length=200, required=False)
	content = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'40'}))