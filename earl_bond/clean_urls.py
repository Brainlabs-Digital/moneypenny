from url import parse, URL

def clean_and_strip(urls):
	output = set()
	for url in urls:
		url_obj = parse(url).defrag().abspath().canonical()
		output.add(url_obj.utf8())
	return list(output)