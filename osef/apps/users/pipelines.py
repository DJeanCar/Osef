

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
	url = None
	if backend.name == 'facebook':
		url = 'https://graph.facebook.com/%s/picture?type=large' % response['id']
	if url is not None:
		user.url_photo = url
		user.save()