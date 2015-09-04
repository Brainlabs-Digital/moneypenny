import re

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

