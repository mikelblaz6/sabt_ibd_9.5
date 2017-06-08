import subprocess, sys, os, shutil

import local
import utils
import defines as constants

def compile(project_tree, args, work_path):
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	deploy_path = constants.deploy_paths[cc_key][deb_key]
	build_path = constants.build_paths[cc_key][deb_key]
	
	for project, project_data in project_tree.iteritems():
		if args.project == project:
			for version, version_data in project_data.iteritems():
				project_name = utils.get_full_path(project, version)
	
	for project, project_data in project_tree.iteritems():
		if args.project == project or args.compile_deps:
			for version, version_data in project_data.iteritems():
				local.prepare_deploy(project, version, deploy_path)
			
	p = subprocess.Popen(['make', '-f', work_path + '/Makefile_tftp', project_name], close_fds = True)
	p.communicate()
	if p.returncode != 0:
		raise Exception("Error building")
					
	print "------------- COMPILATION ENDED SUCCESSFULLY ----------------"
	

def install(project_tree, args, work_path, build_type):
	if args.install:
		for project, project_data in project_tree.iteritems():
			if args.project == project:
				for version, version_data in project_data.iteritems():
					project_name = utils.get_full_path(project, version)
					
		if build_type == "tftp":
			make_name = "Makefile_tftp"
			install_dir_name = constants.INSTALL_DIR_TFTP
		elif build_type == "full":
			make_name = "Makefile_full"
			install_dir_name = constants.INSTALL_DIR_FULL
			
		p = subprocess.Popen(['make', '-f', work_path + '/' + make_name, project_name + '_install'], close_fds = True)
		p.communicate()
		if p.returncode != 0:
			raise Exception("Error installing")
			
		if args.project == "rootfs":
			if build_type == "tftp":
				target = project_name + '_install-tftp'
			elif build_type == "full":
				target = project_name + '_install-full'
			elif build_type == "incr":
				target = project_name + '_install-incr'
			p = subprocess.Popen(['make', '-f', work_path + '/' + make_name, target], close_fds = True)
			p.communicate()
			if p.returncode != 0:
				raise Exception("Error installing build specific content")
			ret = os.system('sqlite3 ' + install_dir_name + '/home/sabt/data/db/system_db.db3 "update fw_info set fw_version=\'' + args.final_release_version + '\';"')
			if ret != 0:
				raise Exception("Error setting db fw info")

def create_image(args, work_path, build_type):
	if args.project == "rootfs":
		if build_type == "tftp":
			make_name = "Makefile_tftp"
		elif build_type == "full":
			make_name = "Makefile_full"
			
		p = subprocess.Popen(['make', '-f', work_path + '/' + make_name, 'rootfs_image'], close_fds = True)
		p.communicate()
		if p.returncode != 0:
			raise Exception("Error creating image")
