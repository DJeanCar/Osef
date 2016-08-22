from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
	url = None
	if backend.name == 'facebook':
		url = 'https://graph.facebook.com/%s/picture?type=large' % response['id']
	if url is not None:
		user.url_photo = url
		user.save()


@partial
def get_email(backend, strategy, request, 
			  details, response, user=None, 
			  is_new=False, *args, **kwargs):
	if details['email']:
		return
	elif is_new:
		if strategy.session_get('saved_email'):
			details['email'] = strategy.session_pop('saved_email')
		else:
			url = 'https://graph.facebook.com/%s/picture?type=large' % response['id']
			strategy.session_set('fullname', details['fullname'])
			strategy.session_set('url_photo', url)
			strategy.session_set('has_access', True)
			return redirect(reverse('users:get_email'))

