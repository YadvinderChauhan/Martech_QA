
def get_url(url):
	""" get_url function takes one argument - a url and returns the url with the redirection part removed."""
	head, sep, tail = url.partition('&redirectTo')
	return head