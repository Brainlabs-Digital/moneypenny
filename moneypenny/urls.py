import tldextract

from url import parse
from urlparse import urlparse
from collections import namedtuple


def normalize(url):
    """ Uses the Moz URL library to normalise and strip the URLs of
        extraneous information, and the urlparse library to ensure it
        is not a blank URL.
    """

    if url[:4] != 'http':
        url = 'http://'+url
    url = url.lower()
    url_parts = urlparse(url)
    if url_parts.netloc:
        url_obj = parse(url).defrag().abspath().canonical().punycode()
        return url_obj.utf8()


def normalize_and_dedupe(urls):
    """ Applies normalize to a list."""

    if isinstance(urls, list):
        output = set()
        for url in urls:
            output.add(normalize(url))
        return list(output)
    else:
        return normalize(urls)


def normalize_and_dedupe_with_counts(dirty_urls):
    """ Takes a list of URLs, takes a count of them, sanitises them and
        returns a count of the sanitised URLs.  Output is namedtuple of count
        pre-cleaning, count post-cleaning, and then the list of URLs.
    """

    urls_entered = len(dirty_urls)
    clean_urls = normalize_and_dedupe(dirty_urls)
    unique_urls_entered = len(clean_urls)
    clean_urls_with_counts = namedtuple('clean_urls_with_counts',
                                        'urls_entered unique_urls_entered clean_urls')

    return clean_urls_with_counts(urls_entered, unique_urls_entered, clean_urls)


def dedupe(urls):
    """ Gets rid of duplicates in a list (and returns a list).
    """
    output = set()
    for url in urls:
        output.add(url)
    return list(output)


def rootdomain(url):
    """ Using tldextract, returns the rootdomain domain of a URL.
    """
    extract = tldextract.extract(url)
    reg_dom = extract.registered_domain

    return reg_dom


def subdomain(url):
    """ Extract the subdomain of a given URL.
    """
    extract = tldextract.extract(url)
    stem = extract.registered_domain
    if extract.subdomain:
        stem = extract.subdomain + '.' + stem

    return stem


def subdomains(urls, dupes=True):
    """ Takes a list of sanitised URLs and returns a list of the subdomains.
        For example, www.foo.com from http://www.foo.com.
    """
    domains = []
    for url in urls:
        domains.append(subdomain(url))

    if not dupes:
        return dedupe(domains)

    return domains
