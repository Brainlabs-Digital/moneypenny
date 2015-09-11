from helper import dedupe
from clean_urls import clean_and_strip, clean_and_strip_singular
from parse_urls import sub_plus_registered_domain
from import_helpers import *


def sub_plus_reg_from_list(urls, dupes=True):
	"""Takes a list of sanitised URLs and returns a list of the subdomain plus registered domain
	of all entries.  For example, www.foo.com from http://www.foo.com."""
	domains = []
	for url in urls:
		domains.append(sub_plus_registered_domain(url))
	if not dupes:
		return dedupe(domains)
	return domains


def cleaning_urls_with_counts(dirty_urls):
	"""Takes a list of URLs, takes a count of them, sanitises them and returns a count of the 
	sanitised URLs.  Output is count pre-cleaning, count post-cleaning, and then the list of URLs."""
	urls_entered = len(dirty_urls)
	clean_urls = clean_and_strip(dirty_urls)
	unique_urls_entered = len(clean_urls)
	return (urls_entered, unique_urls_entered, clean_urls)


def apply_domain_limit(entries, domain_limit):
	"""Takes a list of sanitised URLs and looks at their domains.  If a domain count exceeds the limit,
	the urls from that domain are removed and replaced with a single 'domain: url' entry.
	The counts of the new 'domain:' entries, and the remaining links are also returned."""
	stripped_urls = sub_plus_reg_from_list(entries)
	new_url_set = set()
	exceeded_domains = set()
	domains_seen = set()
	domains_count = dict()
	for url in stripped_urls:
		if url not in domains_seen:
			domains_seen.add(url)
			domains_count[url] = 1
		else:
			domains_count[url] += 1

	for url in stripped_urls:
		if domains_count[url] >= domain_limit:
			exceeded_domains.add(url)
	
	for entry in entries:
		if sub_plus_registered_domain(entry) not in exceeded_domains:
			new_url_set.add(entry)

	return (list(new_url_set), list(exceeded_domains))


def disavow_from_existing_domains(**entries_dict):
	urls = clean_and_strip(entries_dict['urls'])
	domains = sub_plus_reg_from_list(entries_dict['domains'])
	new_url_set = set()
	for url in urls:
		if sub_plus_registered_domain(url) not in domains:
			new_url_set.add(url)
	return list(new_url_set)


def disavow_both_ways(disavow_file, list_of_urls):
	open_file = extract_file_contents(disavow_file)
	disavow_entries = import_file_contents(open_file)
	disavow_links = clean_and_strip(disavow_entries['urls'])
	disavow_domains = disavow_entries['domains']
	urls = clean_and_strip(list_of_urls)
	disavowed_urls = []
	non_disavowed_urls = []
	for url in urls:
		if (url in disavow_links) or (sub_plus_registered_domain(url) in sub_plus_reg_from_list(disavow_domains)):
			disavowed_urls.append(url)
		else:
			non_disavowed_urls.append(url)

	return {'disavowed': disavowed_urls, 'non_disavowed': non_disavowed_urls}


def disavow_to_comments(disavow_file, domain_limit=False):
	extract = extract_file_contents(disavow_file)
	entries_dict = import_file_contents(extract)
	link_entries = clean_and_strip(entries_dict['urls'])
	links_entered = len(entries_dict['urls'])
	unique_links_entered = len(link_entries)
	domain_entries = entries_dict['domains']
	domains_entered = len(domain_entries)
	if domain_entries:
		link_entries = disavow_from_existing_domains(**entries_dict)
	new_domain_entries = []
	if domain_limit:
		link_entries, new_domain_entries = apply_domain_limit(link_entries, domain_limit)
	domain_entries = sub_plus_reg_from_list(domain_entries)
	new_domain_entries = sub_plus_reg_from_list(new_domain_entries)
	total_domains_disavowed = len(domain_entries + new_domain_entries)
	links_disavowed = len(link_entries)
	return {'old_domains': domain_entries, 'new_domains': new_domain_entries,
			'links_entered': links_entered, 'unique_links_entered': unique_links_entered,
			'domains_entered': domains_entered, 
			'total_domains_disavowed': total_domains_disavowed, 'links_disavowed': links_disavowed}


def combine_with_original_disavow(disavow_file, **domains):
	output = []
	extract = extract_file_contents(disavow_file)
	file_contents = extract.splitlines()
	already_converted_to_domain = []
	for lineraw in file_contents:

		if (not lineraw.isspace()) and (lineraw != ""):

			if lineraw.startswith('"') and lineraw.endswith('"'):
				lineraw = lineraw[1:-1]

			if lineraw[0] == '#':
				# line is a comment 
				output.append(lineraw)
				continue

			if lineraw[:7] == 'domain:':
				# line is an existing domain entry
				output.append('domain:' + sub_plus_registered_domain(clean_and_strip_singular(lineraw[7:])))
				continue

			else:
				line = sub_plus_registered_domain(clean_and_strip_singular(lineraw))
				
				if line in domains['new_domains']:
					
					if line not in already_converted_to_domain:
						already_converted_to_domain.append(line)
						output.append('domain:' + clean_and_strip_singular(lineraw))

					else:
						output.append('# link now disavowed via domain entry')
				
				elif line in domains['old_domains']:
					output.append('# link now disavowed via domain entry')
				
				else:
					output.append(clean_and_strip_singular(lineraw))
	return output
