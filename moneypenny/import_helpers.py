import re
from parse_urls import sub_plus_registered_domain
from clean_urls import clean_and_strip


def import_urls_from_text_file(filename, skip_header_row=False):
    """Handles the import from a text file where each entry is on a new line.  Outputs a list"""
    urls = []

    with open(filename, 'r') as input_file:

        if skip_header_row:
            next(input_file)

        for raw_line in input_file:

            if not raw_line.isspace():
                cleaned_line = raw_line.replace("\n", '')
                #cleaned_line = cleaned_line.replace('\x00', '')

                wrapped_in_quotes_matcher = re.search('^"(.*)"$', cleaned_line)

                if wrapped_in_quotes_matcher:
                    if not wrapped_in_quotes_matcher.group(1).isspace():
                        cleaned_line = wrapped_in_quotes_matcher.group(1)
                        urls.append(cleaned_line)

                else:
                    urls.append(cleaned_line)

    return urls

def extract_file_contents(filename):
    """The first step in importing, takes a file and converts to a string"""
    # We don't use readlines() as we need to clean the files potentially.
    # (Sometimes certain link tools output files that we can't seem to decode without doing the manual cleaning
    # that follows - but it is is somewhat dirty/hacky.)

    disavow_contents = ""

    with open (filename, "r") as disavow_file:

        file_contents = disavow_file.read()

        try:
            disavow_contents = file_contents.decode("utf-8-sig")
        except UnicodeDecodeError:
            disavow_contents = file_contents.decode("utf-16")

    return disavow_contents


def import_file_contents(file_contents):
    """Takes a string, such as that from extract_file_contents(), splits on new lines, and returns
    a dictionary of 'domain:' entries, and standalone URL entries.  Handles comments by ignoring them."""
    urls = set()
    domains = set()
    entries = {}

    # file_contents = file_contents.split("\n")
    file_contents = file_contents.splitlines()

    for lineraw in file_contents:
        if (not lineraw.isspace()) and (lineraw != ""):

            if lineraw.startswith('"') and lineraw.endswith('"'):
                lineraw = lineraw[1:-1]

            if lineraw[0] == '#':
                # comment entry
                continue

            if lineraw[:7] == "domain:":
                # domain entry

                line = re.sub("\n", "", lineraw[7:])

                if line.startswith('"') and line.endswith('"'):
                    line = line[1:-1]

                # We run the domain extract here, as sometimes people accidentally
                # put full URLs in domain entries. We assume they mean to exclude
                # the domain (which is often now recommended anyway - "no good
                # links from bad domains").

                domain = sub_plus_registered_domain(line)
                domains.add(domain)

            else:
            #not a domain entry
                line = re.sub("\n", "", lineraw)
                urls.add(line)

    entries['urls'] = (list(urls))
    entries['domains'] = clean_and_strip(list(domains))
    return entries
