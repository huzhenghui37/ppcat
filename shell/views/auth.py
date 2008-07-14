from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from ppcat.shell.settings import DEFAULT_LOGIN_REDIRECT_URL, DEFAULT_REDIRECT_KEY


def login(request, redirect_to=DEFAULT_LOGIN_REDIRECT_URL, redirect_key=DEFAULT_REDIRECT_KEY):
	template = 'login.django.html'
	
	next = request.REQUEST.get(redirect_key, '/'+redirect_to)
	
	if request.POST:
		user = auth.authenticate(username=request.POST['username'],
								 password=request.POST['password'])
		if user is not None and user.is_active:
			auth.login(request, user)
			#next = request.POST.get(redirect_key, DEFAULT_LOGIN_REDIRECT_URL)
			return HttpResponseRedirect(next)
	
	return render_to_response(template, {'next':next})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('index'))
	#return HttpResponseRedirect(reverse('photo', args=[None]))

#def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
#    "Displays the login form and handles the login action."
#    manipulator = AuthenticationForm(request)
#    redirect_to = request.REQUEST.get(redirect_field_name, '')
#    if request.POST:
#        errors = manipulator.get_validation_errors(request.POST)
#        if not errors:
#            # Light security check -- make sure redirect_to isn't garbage.
#            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
#                from django.conf import settings
#                redirect_to = settings.LOGIN_REDIRECT_URL
#            from django.contrib.auth import login
#            login(request, manipulator.get_user())
#            request.session.delete_test_cookie()
#            return HttpResponseRedirect(redirect_to)
#    else:
#        errors = {}
#    request.session.set_test_cookie()
#
#    if Site._meta.installed:
#        current_site = Site.objects.get_current()
#    else:
#        current_site = RequestSite(request)
#
#    return render_to_response(template_name, {
#        'form': oldforms.FormWrapper(manipulator, request.POST, errors),
#        redirect_field_name: redirect_to,
#        'site_name': current_site.name,
#    }, context_instance=RequestContext(request))

#def logout(request, next_page=None, template_name='registration/logged_out.html'):
#    "Logs out the user and displays 'You are logged out' message."
#    from django.contrib.auth import logout
#    logout(request)
#    if next_page is None:
#        return render_to_response(template_name, {'title': _('Logged out')}, context_instance=RequestContext(request))
#    else:
#        # Redirect to this page until the session has been cleared.
#        return HttpResponseRedirect(next_page or request.path)