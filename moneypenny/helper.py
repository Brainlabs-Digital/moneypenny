def dedupe(urls):
	"""Gets rid of duplicates in a list (and returns a list)"""
	output = set()
	for url in urls:
		output.add(url)
	return list(output)

def export_as_txt(filename, urls):
	"""Takes an iterable and converts it to a text file, each entry on a new line"""
	line_ending = '\n'
	with open(filename, 'w') as f:
		for line in urls:
			f.write(line + line_ending)

