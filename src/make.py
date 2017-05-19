#! /usr/bin/python
import argparse, os, logging, time, sys

import defines as constants
import local
import dependencies
import utils
import makewriter
import makeexe
import img_tftp
import img_web
import incr_makewriter
import img_incr

def doit(args, work_path):
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	build_path = constants.build_paths[cc_key][deb_key]
	deploy_path = constants.deploy_paths[cc_key][deb_key]
	#Not version checking for local compilations. version set to None
	version = args.project_version if (args.project_version != "" and args.local == False) else None
	
	if args.final_release:
		if args.local or args.debug or args.no_cross_compile or args.create_only or args.no_rebuild or args.final_release_version == "local":
			raise Exception("Parameters no compatible with Final Release")
			
		if args.part_number == "":
			raise Exception("Part number required for creating images")
			
		args.project = "rootfs"
		args.compile_deps = True
		args.install = True
		args.clean_install_dir = True
		args.images = True
	else:
		if args.project == "":
			raise Exception("Project not set")
	
		if args.no_rebuild and (args.git or args.install or args.compile_deps):
			raise Exception("No rebuild no compatible with currernt parameters")
		
		if args.git and (not args.compile_deps or args.debug):
			raise Exception("Git projects must be compilled fully and in release mode")
		
		if args.images and (args.project != "rootfs"  or args.debug):
			raise Exception("Images can only be created for rootfs project and in release mode")
			
		if args.images and args.part_number == "":
			raise Exception("Part number required for creating images")
			
		if args.images:
			args.install = True

	dep_processor = dependencies.Dependencies(args, build_path, deploy_path)
	project_tree = dep_processor.get_depend_projects(version)

	make_writer = makewriter.Makewriter(args, project_tree, build_path, deploy_path, work_path)
	make_writer.write_makefile()
	
	if args.install and args.clean_install_dir:
		os.system('rm -Rf ' + constants.INSTALL_DIR)
	
	if not args.create_only:
		makeexe.compile(project_tree, args, work_path)
		
	if args.images:
		img_tftp.create_tftp_img(args, work_path)
		img_web.create_web_img(args, project_tree, work_path)
		incr_make_writer = incr_makewriter.IncrMakewriter(args, project_tree, build_path, deploy_path, work_path)
		incr_project_list = incr_make_writer.write_makefile()
		img_incr.create_web_img(args, project_tree, incr_project_list, work_path)

	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Build MRT developments and dependencies.')
	parser.add_argument('-P', '--project', help='project to build', default = "")
	parser.add_argument('-v', '--project-version', help='project version to build (if not set, last version will be built). Only valid when using git', default = "")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-g', '--git', action='store_true', help='build from git sources')
	group.add_argument('-l', '--local', action='store_true', help='build from local sources (disables git)')
	parser.add_argument('-p', '--path', help='path to local sources (if local enabled)', default="")
	group2 = parser.add_mutually_exclusive_group(required=True)
	group2.add_argument('-d', '--debug', action='store_true', help='debug build')
	group2.add_argument('-r', '--release', action='store_true', help='release build')
	parser.add_argument('--no-cross-compile', action='store_true', help='x86 build')
	parser.add_argument('-D', '--compile-deps', action='store_true', help='rebuild all project dependencies')
	parser.add_argument('-m', '--make-params', help='arguments to be passed to final makefile of main project (if applies)', default = "")
	parser.add_argument('-c', '--create-only', action='store_true', help='only creates makefile and folder structure. Do not compile')
	parser.add_argument('-i', '--install', action='store_true', help='install project on install directory')
	parser.add_argument('-C', '--clean-install-dir', action='store_true', help='clean install directory (only if install selected)')
	parser.add_argument('--no-rebuild', action='store_true', help='do not rebuild whole project (only if -l, and not -i and -D)')
	parser.add_argument('-I', '--images', action='store_true', help='create full tftp and web images, and incremental image')
	parser.add_argument('--part-number', help='Part number') 
	parser.add_argument('-F', '--final-release', action='store_true', help='create final release storing version info in database. Includes -g -r -D -i -C -I, -P rootfs')
	parser.add_argument('-V', '--final-release-version', help='set fw version for current release. Needed if --final-release active', default = "local")
	parser.add_argument('-M', '--previous-min-version', help='Minimum fw version needed in RTU for compatibility with new fw. Needed if --final-release active', default = "local")
	args = parser.parse_args()

	
	prefix = "local" if args.local else "git"
	date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
	work_path = constants.MAIN_DIR + 'builds/'+ prefix+ '/' + date 
	os.system('mkdir -p ' + work_path)
	filename = work_path + '/log.txt'
	logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
	logging.info("Starting app")
	logging.info("Invoked with arguments: " + str(args))
	
	
	doit(args, work_path)
	
	'''try:
		doit(args, work_path)
	except Exception as inst:
		logging.error("Program exitted with exception: " + str(inst))
		print "Program exitted with exception: " + str(inst)
		exit(1)
	else:
		logging.info("Execution completed without errors")
		exit(0)'''
	
	
	

	
	
