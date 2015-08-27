import tldextract

def list_of_component(urls, component='registered_domain'):
	return [
		getattr(tldextract.extract(url), component)
		for url in urls 
	]

def sub_plus_registered_domain(urls):
	output = []
	for url in urls:
		extract = tldextract.extract(url)
		stem = extract.registered_domain
		if extract.subdomain:
			stem = extract.subdomain + '.' + stem
		output.append(stem)
	return output