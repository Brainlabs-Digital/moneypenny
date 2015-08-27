def dedupe(urls):
	output = set()
	for url in urls:
		output.add(url)
	return list(output)

def export_as_txt(filename, urls):
	line_ending = '\n'
	with open(filename, 'w') as f:
		for line in urls:
			f.write(line + line_ending)




