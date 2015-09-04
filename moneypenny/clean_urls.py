from url import parse, URL

def clean_and_strip(urls):
	"""Uses the SEOMoz URL library to normalise and strip the URLs of extraneous information"""
	output = set()
	for url in urls:
		url = url.lower()
		url_obj = parse(url).defrag().abspath().canonical()
		output.add(url_obj.utf8())
	return list(output)