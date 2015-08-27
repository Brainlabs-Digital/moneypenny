from import_helpers import import_urls_from_text_file
from helper import dedupe
from clean_urls import clean_and_strip
from parse_urls import list_of_component, sub_plus_registered_domain

def individual_components_from_file(text_file, component='registered_domain', dupes=True):
	urls = import_urls_from_text_file(text_file)
	urls = clean_and_strip(urls)
	domains = list_of_component(urls, component=component)
	if not dupes:
		return dedupe(domains)
	return domains


def sub_plus_reg_from_file(text_file, dupes=True):
	urls = import_urls_from_text_file(text_file)
	urls = clean_and_strip(urls)
	domains = sub_plus_registered_domain(urls)
	if not dupes:
		return dedupe(domains)
	return domains


def apply_domain_limit(urls, domain_limit=3):
	new_url_set = set()
	domains_seen = set()
	domains_count = dict()
	for url in urls:
		if url not in domains_seen:
			domains_seen.add(url)
			domains_count[url] = 1
		else:
			domains_count[url] += 1

	for url in urls:
		if domains_count[url] >= domain_limit:
			new_url_set.add('domain: ' + url)
		else:
			new_url_set.add(url)

	return list(new_url_set)
