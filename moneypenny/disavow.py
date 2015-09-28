import re

from collections import namedtuple

from urls import normalize, normalize_and_dedupe, normalize_and_dedupe_with_counts
from urls import subdomain, rootdomain, subdomains


def apply_domain_limit(entries, domain_limit):
    """ Takes a list of sanitised URLs and looks at their domains.  If a
        domain count exceeds the limit, the urls from that domain are
        removed and replaced with a single 'domain: url' entry. The counts
        of the new 'domain:' entries, and the remaining links are also
        returned.
    """

    stripped_urls = subdomains(entries)
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
        if (subdomain(entry) not in exceeded_domains and
                rootdomain(entry) not in exceeded_domains):
            new_url_set.add(entry)

    applied_domain_limit = namedtuple('applied_domain_limit', 'remaining_urls exceeded_domains')

    return applied_domain_limit(new_url_set, exceeded_domains)


def apply_disavow_files(disavow_file, urls_to_test_file):
    """ NBED
    """

    disavow_entries = import_from_file(disavow_file)
    urls_list = import_from_file(urls_to_test_file)['urls']

    return apply_disavow(disavow_entries, urls_list)


def apply_disavow(disavow_entries, urls_list):
    """ Using a disavow file, tests which of a file of urls would be
        disavowed and which wouldn't.
    """

    disavow_links = []
    disavow_domains = []
    output_dict = {}

    if 'urls' in disavow_entries:
        disavow_links_details = normalize_and_dedupe_with_counts(disavow_entries['urls'])
        disavow_links = disavow_links_details.clean_urls
        output_dict['disavow_links_entered'] = disavow_links_details.urls_entered
        output_dict['unique_disavow_links_entered'] = disavow_links_details.unique_urls_entered
    if 'domains' in disavow_entries:
        disavow_domains_details = normalize_and_dedupe_with_counts(disavow_entries['domains'])
        disavow_domains = subdomains(disavow_domains_details.clean_urls)

    urls_to_test_details = normalize_and_dedupe_with_counts(urls_list)
    urls = urls_to_test_details.clean_urls

    disavowed_urls = []
    non_disavowed_urls = []

    for url in urls:
        if (url in disavow_links) or (subdomain(url) in disavow_domains):
            disavowed_urls.append(url)
        else:
            non_disavowed_urls.append(url)

    total_disavowed_links = len(disavowed_urls)
    total_remaining_links = len(non_disavowed_urls)

    output_dict.update({
        'disavowed': disavowed_urls,
        'non_disavowed': non_disavowed_urls,
        'domains_entered': disavow_domains_details.urls_entered,
        'unique_domains_entered': disavow_domains_details.unique_urls_entered,
        'urls_entered_to_test': urls_to_test_details.urls_entered,
        'unique_urls_entered_to_test': urls_to_test_details.unique_urls_entered,
        'total_disavowed_links': total_disavowed_links,
        'total_remaining_links': total_remaining_links
    })

    return output_dict


def remove_redundant_domains(old_domains, new_domains):
    """ Checks whether any domains that have been newly created
    conflict with any existing domain entries and removes any
    such conflict.
    """

    non_redundant_old_domains = set()
    non_redundant_new_domains = set()
    for old_domain in old_domains:
        if rootdomain(old_domain) not in new_domains:
            non_redundant_old_domains.add(old_domain)
    for new_domain in new_domains:
        if new_domain not in old_domains:
            non_redundant_new_domains.add(new_domain)
    return (list(non_redundant_old_domains), list(non_redundant_new_domains))


def disavow_file_to_dict(file_contents, domain_limit=False):
    """ Takes a disavow file and applies many helper functions,
        outputting a dictionary with old and new domain entries,
        the individual links to be disavowed, as well as useful counts.
    """

    entries_dict = import_from_file_contents(file_contents)
    link_entries_details = normalize_and_dedupe_with_counts(entries_dict['urls'])
    link_entries = link_entries_details.clean_urls
    domain_entries_details = normalize_and_dedupe_with_counts(entries_dict['domains'])
    domain_entries = subdomains(domain_entries_details.clean_urls)

    if domain_entries:
        applied_disavow = apply_disavow({"domains": entries_dict['domains']}, entries_dict['urls'])
        link_entries = applied_disavow['non_disavowed']

    final_domain_entries = set()
    final_domain_entries.update(domain_entries)

    if domain_limit:
        link_entries, new_domain_entries = apply_domain_limit(link_entries, domain_limit)
        final_domain_entries.update(new_domain_entries)

    if domain_entries and domain_limit:
        domain_entries, new_domain_entries = remove_redundant_domains(domain_entries,
                                                                      new_domain_entries)
    # total_domains_disavowed = len(domain_entries + new_domain_entries)
    links_disavowed = len(link_entries)

    return {
        'domain_entries': list(final_domain_entries),
        'url_entries': link_entries,

        'urls_entered_count': link_entries_details.urls_entered,
        'urls_disavowed_count': links_disavowed,
        'unique_urls_entered_count': link_entries_details.unique_urls_entered,
        'domain_entries_entered_count': domain_entries_details.urls_entered,
    }


def combine_with_original_disavow(file_contents, disavow_entries):
    """ Takes the disavow file passed to disavow_file_to_dict() and it's
        resulting output and combines them to create a .txt file with the
        relevant 'domain:' entries and individual links to be disavowed,
        while maintaining the order and the comments from the original
        document.
     """

    output = []
    # extract = extract_file_contents(disavow_file)
    file_contents = file_contents.splitlines()
    urls_encountered = set()
    domains_encountered = set()
    for raw_entry in file_contents:

        if (not raw_entry.isspace()) and (raw_entry != ""):

            # Strip quotes for lines wrapped in quotes
            if raw_entry.startswith('"') and raw_entry.endswith('"'):
                raw_entry = raw_entry[1:-1]

            if raw_entry[0] == '#':
                # line is a comment, so we just keep it
                output.append(raw_entry)
                continue

            if raw_entry[:7] == 'domain:':
                # line is an domain entry

                # clean the domain entry
                domain_normalized = normalize(raw_entry[7:])

                # check if it is valid, if not then include it is a comment
                if not domain_normalized:
                    output.append('# invalid entry - ' + raw_entry)

                else:
                    clean_domain = subdomain(domain_normalized)
                    if clean_domain in disavow_entries['domain_entries']:
                        if clean_domain not in domains_encountered:
                            output.append('domain:' + clean_domain)
                            domains_encountered.add(clean_domain)
                        else:
                            output.append('# domain entry already present - ' + clean_domain)
            else:
                # line is a url entry

                # clean the url entry
                url_normalized = normalize(raw_entry)

                # check if link entry is valid
                if not url_normalized:
                    output.append('# invalid entry - ' + raw_entry)

                else:
                    url_subdomain = subdomain(url_normalized)
                    url_rootdomain = rootdomain(url_normalized)

                    if url_subdomain in disavow_entries['domain_entries']:

                        if url_subdomain not in domains_encountered:
                            domains_encountered.add(url_subdomain)
                            output.append('domain:' + url_subdomain)

                        else:
                            output.append('# link now disavowed via new domain entry - ' + raw_entry)

                    elif url_rootdomain in disavow_entries['domain_entries']:

                        if url_rootdomain not in domains_encountered:
                            domains_encountered.add(url_rootdomain)
                            output.append('domain:' + url_rootdomain)

                        else:
                            output.append('# link now disavowed via new domain entry - ' + raw_entry)

                    elif url_normalized in disavow_entries['url_entries']:
                        if url_normalized not in urls_encountered:
                            output.append(url_normalized)
                            urls_encountered.add(url_normalized)
                        else:
                            output.append('# link entry already present')

                    else:
                        output.append('# error occurred, not sure what to do with this - ' + raw_entry)
    return output


def extract_file_contents(filename):
    """ The first step in importing, takes a file and converts to
        a string.
    """
    disavow_contents = ""

    with open(filename, "r") as disavow_file:

        file_contents = disavow_file.read()

        try:
            disavow_contents = file_contents.decode("utf-8-sig")
        except UnicodeDecodeError:
            disavow_contents = file_contents.decode("utf-16")

    return disavow_contents


def import_from_file_contents(file_contents):
    """ Takes a string, such as that from extract_file_contents(), splits
        on new lines, and returns a dictionary of 'domain:' entries, and
        standalone URL entries.  Handles comments by ignoring them.
    """
    urls = []
    domains = []

    file_contents = file_contents.splitlines()

    for lineraw in file_contents:
        if (not lineraw.isspace()) and (lineraw != ""):

            if lineraw.startswith('"') and lineraw.endswith('"'):
                lineraw = lineraw[1:-1]

            if lineraw[0] == '#':
                # comment entry
                continue

            # checking if url is valid
            if not normalize(lineraw):
                continue

            else:

                if lineraw[:7] == "domain:":
                    # domain entry

                    line = re.sub("\n", "", lineraw[7:])

                    # checking if domain url is valid
                    if not normalize(line):
                        continue

                    else:
                        if line.startswith('"') and line.endswith('"'):
                            line = line[1:-1]

                        # We run the domain extract here, as sometimes people accidentally
                        # put full URLs in domain entries. We assume they mean to exclude
                        # the domain (which is often now recommended anyway - "no good
                        # links from bad domains").
                        domain = subdomain(line)
                        domains.append(domain)

                else:
                    # not a domain entry
                    line = re.sub("\n", "", lineraw)
                    urls.append(line)

    return {'urls': urls, 'domains': domains}


def import_from_file(filename):

    file_contents = extract_file_contents(filename)
    return import_from_file_contents(file_contents)
