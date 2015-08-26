import tldextract

def list_of_component(urls, component='registered_domain'):
	return [
		getattr(tldextract.extract(url), component)
		for url in urls 
	]

