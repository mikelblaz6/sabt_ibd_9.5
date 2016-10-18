#! /usr/bin/python


def replace_template(path, tags):
	fid = open(path)
	ret = ""
	for line in fid:
		for tag in tags:
			if tag[0] in line:
				line = line.replace(tag[0], tag[1])
				break
		ret += line
	return ret
	
