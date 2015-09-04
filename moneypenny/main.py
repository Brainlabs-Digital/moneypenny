from helper import dedupe
from clean_urls import clean_and_strip
from parse_urls import sub_plus_registered_domain


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
	domains_disavowed = 0
	links_disavowed = 0
	for url in stripped_urls:
		if url not in domains_seen:
			domains_seen.add(url)
			domains_count[url] = 1
		else:
			domains_count[url] += 1

	for url in stripped_urls:
		if domains_count[url] >= domain_limit:
			new_url_set.add('domain: ' + url)
			exceeded_domains.add(url)
	
	domains_disavowed = len(new_url_set)

	for entry in entries:
		if sub_plus_registered_domain(entry) not in exceeded_domains:
			new_url_set.add(entry)
			links_disavowed += 1

	return (list(new_url_set), domains_disavowed, links_disavowed)
