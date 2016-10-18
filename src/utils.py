import defines as constants

import os

def get_full_path(project, version):
	version_str = '' if version == None else ('_' + str(version))
	return str(project) + version_str
	
	
def replace_strings(text, tags):
	for tag in tags:
		text = text.replace(tag[0], tag[1])
	return text
	
	
def version_greater(vers1, vers2):
	return (StrictVersion(vers2) < StrictVersion(vers1))
	
def order_versions(version_list):
	ordered_versions = []
	
	while len(version_list) > 0:
		for version in version_list:
			min_version = version
			for cmp_version in version_list:
				if LooseVersion(cmp_version) < LooseVersion(min_version):
					min_version = cmp_version
		version_list.remove(min_version)
		ordered_versions.append(min_version)
	return ordered_versions
