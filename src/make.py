#! /usr/bin/python
import argparse, os, logging, time, sys

import defines as constants
import local
import dependencies
import utils
import makewriter
import makeexe


		

def doit(args, work_path):
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	build_path = constants.build_paths[cc_key][deb_key]
	deploy_path = constants.deploy_paths[cc_key][deb_key]
	#Not version checking for local compilations. version set to None
	version = args.project_version if (args.project_version != "" and args.local == False) else None
	
	if args.no_rebuild and (args.git or args.install or args.compile_deps):
		raise Exception("No rebuild no compatible with currernt config")
		
	if args.git and not args.compile_deps:
		raise Exception("Git projects must be compilled fully")

	dep_processor = dependencies.Dependencies(args, build_path, deploy_path)
	project_tree = dep_processor.get_depend_projects(version)

	make_writer = makewriter.Makewriter(args, project_tree, build_path, deploy_path, work_path)
	make_writer.write_makefile()
	
	if args.install and args.clean_install_dir:
		os.system('rm -Rf ' + constants.INSTALL_DIR)
	
	if not args.create_only:
		makeexe.compile(project_tree, args, work_path)

	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Build MRT developments and dependencies.')
	parser.add_argument('-P', '--project', help='project to build', required=True)
	parser.add_argument('-v', '--project-version', help='project version to build (if not set, last version will be built). Only valid when using git', required=False, default = "")
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
	args = parser.parse_args()

	
	prefix = "local" if args.local else "git"
	date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
	work_path = constants.MAIN_DIR + 'builds/'+ prefix+ '/' + date 
	os.system('mkdir -p ' + work_path)
	filename = work_path + '/log.txt'
	logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
	logging.info("Starting app")
	logging.info("Invoked with arguments: " + str(args))
	
	
	
	try:
		doit(args, work_path)
	except Exception as inst:
		logging.error("Program exitted with exception: " + str(inst))
		print "Program exitted with exception: " + str(inst)
		exit(1)
	else:
		logging.info("Execution completed without errors")
		exit(0)
	
	
	

	
	
