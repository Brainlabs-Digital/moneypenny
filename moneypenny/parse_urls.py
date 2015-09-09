import tldextract
from helper import dedupe

def list_of_components(urls, component='registered_domain', dupes=True):
	"""Returns a list of the required components from a list of URLs.  For instance, with http://www.foo.com,
	one can access 'www' using component = 'subdomain', 'foo' using component = 'domain' and '.com' using
	component = 'suffix'.  Defaults to registered domain which is domain + suffix (ie 'foo.com').  Duplicates
	can be removed."""
	components = [
		getattr(tldextract.extract(url), component)
		for url in urls 
	]
	if not dupes:
		return dedupe(components)
	return components


def sub_plus_registered_domain(url):
	"""Concatenates the subdomain and the registered domain of a given URL"""
	extract = tldextract.extract(url)
	stem = extract.registered_domain
	if extract.subdomain:
		stem = extract.subdomain + '.' + stem
	return stem