
from urllib.parse import urlparse, parse_qs

def get_icid (url):
	"""get_icid function takes one argument - a url and returns its ICID part."""
	query = urlparse(url).query
	path_list = parse_qs(query)['ICID']
	return path_list[0]