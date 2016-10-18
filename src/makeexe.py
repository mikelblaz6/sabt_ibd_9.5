import subprocess, sys, os, shutil

import local
import utils
import defines as constants

def compile(project_tree, args, work_path):
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	deploy_path = constants.deploy_paths[cc_key][deb_key]
	
	for project, project_data in project_tree.iteritems():
		if args.project == project:
			for version, version_data in project_data.iteritems():
				project_name = utils.get_full_path(project, version)
	
	for project, project_data in project_tree.iteritems():
		if args.project == project or args.compile_deps:
			for version, version_data in project_data.iteritems():
				local.prepare_deploy(project, version, deploy_path)
			
	p = subprocess.Popen(['make', '-f', work_path + '/Makefile', project_name], close_fds = True)
	p.communicate()
	if p.returncode != 0:
		raise Exception("Error building")
		
	if args.install:
		for project, project_data in project_tree.iteritems():
			if args.project == project:
				for version, version_data in project_data.iteritems():
					project_name = utils.get_full_path(project, version)
		p = subprocess.Popen(['make', '-f', work_path + '/Makefile', project_name + '_install'], close_fds = True)
		p.communicate()
		if p.returncode != 0:
			raise Exception("Error installing")
			
	print "------------- COMPILATION ENDED SUCCESSFULLY ----------------"

