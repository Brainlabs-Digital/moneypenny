# Introduction

Moneypenny is a library for normalising and handling lists of URLs. It was originally built for the purposes of cleaning and generating [disavow files](https://support.google.com/webmasters/answer/2648487?hl=en) for use with Google.

For example, you may have a file containing a list of URLs or a mix of URLs and 'domain:' entries (i.e. a disavow file), but having been aggregated from various sources you may want to remove duplicates and superfluous entries:

First convert it to a string and parse out the URL and 'domain:' entries using:

	import_from_file('<your_filename>.txt')

Then call:

	normalize_and_dedupe(<import_from_file_output>) 

On the 'urls' or 'domains' list output as you see fit.

Moneypenny currently handles the creation/modification of a disavow file (including maintaining comments in their
original place) and the testing of a disavow file against a separate list of URLs, showing which of these would be 
disavowed or not, were the disavow file to be applied.

# Using Moneypenny

Simply install with pip:

	pip install moneypenny

To create / modify an existing disavow file, 

First call:	
	
	extract_file_contents('<your_filename>.txt')

To convert your file to a string, then pass that to:

	disavow_file_to_dict(<extract_file_contents_output>)

With an optional argument for domain_limit, in case you want to disavow all links originating from a 
certain domain that exceeds your limit.

For example, 
‘www.example.com/a/spam’, ‘www.example.com/#spam’ and ‘www.example.com/a/c/?spam’ can be replaced with
a single 'domain:www.example.com' entry.

The output gives some summary statistics to do with the number of links/domains entered/disavowed along
with 'domain_entries' - which contain the new domains from applying a domain limit and the domains from the 
original disavow file, and 'link_entries' - the individual links to be disavowed.

To modify your existing file, pass your original file to extract_file_contents(), and use this as 
the first parameter to:

	combine_with_original_disavow('<your_filename>.txt', 
	<disavow_file_to_dict_output>)

With the dictionary output of disavow_file_to_dict() as the second parameter.  This function will 
maintain the order (and comments) of your original disavow file.

For testing an existing disavow file against a file containing a list of URLs, simply call:

	apply_disavow_files(<your_disavow_filename>.txt,
		<your_urls_to_test_filename>.txt)

With your disavow file as the first parameter, and your URLs file to test as the second.  The output is a dictionary, 
the most relevant keys of which are 'disavowed' and 'non_disavowed'; the rest are statistics summarising the input files
and output files.  

# To Do

- Port in functionality to parse files from various sources (Majestic, Kerboo, LinkResearchTools) from our older code.

# Why Moneypenny?

Moneypenny disavows secret agents, we are disavowing links … geddit?

# Contributing

See CONTRIBUTING file.

# License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License

See LICENSE file.