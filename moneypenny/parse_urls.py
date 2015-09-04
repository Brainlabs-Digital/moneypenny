import tldextract
from import_helpers import import_urls_from_text_file
from clean_urls import clean_and_strip
from helper import dedupe

def list_of_component(urls, component='registered_domain'):
	"""Returns a list of the required components from a list of URLs"""
	return [
		getattr(tldextract.extract(url), component)
		for url in urls 
	]


def individual_components_from_file(text_file, component='registered_domain', dupes=True):
	"""Can extract a list of sub-parts of URLs from a text file.  For instance, with http://www.foo.com,
	one can access 'www' using component = 'subdomain', 'foo' using component = 'domain' and '.com' using
	component = 'suffix'.  Defaults to registered domain which is domain + suffix (ie 'foo.com').  Duplicates
	can be removed.""" 
	urls = import_urls_from_text_file(text_file)
	urls = clean_and_strip(urls)
	domains = list_of_component(urls, component=component)
	if not dupes:
		return dedupe(domains)
	return domains


def sub_plus_registered_domain(url):
	"""Concatenates the subdomain and the registred domain of a given URL"""
	extract = tldextract.extract(url)
	stem = extract.registered_domain
	if extract.subdomain:
		stem = extract.subdomain + '.' + stem
	return stem