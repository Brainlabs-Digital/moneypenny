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
	

def full_urls_from_file(text_file):
	urls = import_urls_from_text_file(text_file)
	return clean_and_strip(urls)


def original_and_unique_counts(text_file):
	original_urls = import_urls_from_text_file(text_file)
	original_count = len(original_urls)
	unique_urls = clean_and_strip(original_urls)
	unique_count = len(unique_urls)
	return (original_count, unique_count)


def sub_plus_reg_from_list(urls, dupes=True):
	domains = []
	for url in urls:
		domains.append(sub_plus_registered_domain(url))
	if not dupes:
		return dedupe(domains)
	return domains


def apply_domain_limit(clean_urls, dirty_urls, domain_limit):
	new_url_set = set()
	exceeded_domains = set()
	domains_seen = set()
	domains_count = dict()
	domains_disavowed = 0
	links_disavowed = 0
	for url in clean_urls:
		if url not in domains_seen:
			domains_seen.add(url)
			domains_count[url] = 1
		else:
			domains_count[url] += 1

	for url in clean_urls:
		if domains_count[url] >= domain_limit:
			new_url_set.add('domain: ' + url)
			exceeded_domains.add(url)
	
	domains_disavowed = len(new_url_set)

	for dirty in dirty_urls:
		if sub_plus_registered_domain(dirty) not in exceeded_domains:
			new_url_set.add(dirty)
			links_disavowed += 1

	return (list(new_url_set), domains_disavowed, links_disavowed)
