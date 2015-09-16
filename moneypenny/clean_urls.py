from url import parse, URL
from urlparse import urlparse

def clean_and_strip_singular(url):
	"""Uses the SEOMoz URL library to normalise and strip the URLs of extraneous information, 
	and the urlparse library to ensure it is not a blank URL."""
	if url[:4] != 'http':
		url = 'http://'+url
	url = url.lower()
	url_parts = urlparse(url)
	if url_parts.netloc:
		url_obj = parse(url).defrag().abspath().canonical()
		return url_obj.utf8()


def clean_and_strip(urls):
	"""Applies clean_and_strip_singular to a list"""
	output = set()
	for url in urls:
		output.add(clean_and_strip_singular(url))
	return list(output)