from moneypenny import *

def test_test_urls():
	adict = disavow_file_to_dict('test_urls.txt')
	assert adict['links_entered'] == 12 and adict['unique_links_entered'] == 10 and adict['old_domains'] == {}