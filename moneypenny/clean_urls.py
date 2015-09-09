from url import parse, URL
from urlparse import urlparse

def prepend_with_protocol(entries):
	prepended_entries = []
	for entry in entries:
		if entry[:4] != 'http':
			prepended_entries.append('http://'+entry)
		else:
			prepended_entries.append(entry)
	return prepended_entries


def clean_and_strip(urls):
	"""Uses the SEOMoz URL library to normalise and strip the URLs of extraneous information"""
	output = set()
	urls = prepend_with_protocol(urls)
	for url in urls:
		url = url.lower()
		url_parts = urlparse(url)
		if url_parts.netloc:
			url_obj = parse(url).defrag().abspath().canonical()
			output.add(url_obj.utf8())
	return list(output)