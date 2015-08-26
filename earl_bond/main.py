from helper import import_urls_from_text_file, dedupe
from clean_urls import clean_and_strip
from parse_urls import list_of_component

def domains_from_file(text_file, domain='registered_domain', dupes=True):
	urls = import_urls_from_text_file(text_file)
	urls = clean_and_strip(urls)
	domains = list_of_component(urls, component=domain)
	if not dupes:
		return dedupe(domains)
	return domains

