#! /usr/bin/python
import os, logging, time, sys, traceback

import args_parser, logger
import defines as constants
import local
import dependencies
import utils
import makewriter
import makeexe
import img_tftp
import img_full
import incr_makewriter
import img_incr
import database
import mrt_git
import include_projects
import project_commits

def doit(args, paths):
	os.system("rm " + constants.GCC_LINK)
	if args.compiler == "5":
		os.system("ln -s " + constants.GCC_5_DIR + " " + constants.GCC_LINK)
	else:
		os.system("ln -s " + constants.GCC_7_DIR + " " + constants.GCC_LINK)
	
	sql = None
	legacy_min_version_list = None
	
	try:
		if args.final_release or args.images:
			sql = database.Database()
			if args.legacy_mode:
				legacy_min_version_list = args.legacy_min_versions
			if sql.VerifyNewRelease(constants.GLOBAL_PROJECT, args.final_release_version, args.part_number_list, args.previous_min_versions_list, legacy_min_version_list) != 0:
				exit(1)
			
		dep_processor = dependencies.Dependencies(args, paths)
		project_tree = dep_processor.get_depend_projects()
		
		if not args.images:
			make_writer = makewriter.Makewriter(args, project_tree, paths)
			make_writer.write_makefile()
		
			if not args.create_only:
				makeexe.do_build(project_tree, args, paths)
				
				if args.install:		
					os.system('rm -Rf ' + constants.INSTALL_DIR_GENERIC)
					makeexe.do_install(project_tree, args, paths)
		else:
			compilation_id = None
			if args.final_release:
				compilation_id = sql.NewRelease(constants.GLOBAL_PROJECT, args.final_release_version, args.part_number_list, args.previous_min_versions_list, str(args), legacy_min_version_list)
				cur_commit = mrt_git.get_current_commit(constants.MAIN_DIR)[1]
				logger.info(str("Project compiler") + ". Commit id: " + str(cur_commit))
				print(str("Project compiler") + ". Commit id: " + str(cur_commit))
				sql.NewModule(compilation_id, "Project compiler", cur_commit, tftp_img_included = 0)
			
			''' Imagen TFTP '''
			make_writer_tftp = makewriter.Makewriter(args, project_tree, paths, constants.BUILD_TYPE_TFTP)
			make_writer_tftp.write_makefile(compilation_id, sql)
			
			makeexe.do_build(project_tree, args, paths)
			
			os.system('rm -Rf ' + constants.INSTALL_DIR_TFTP)
			makeexe.do_install(project_tree, args, paths, constants.BUILD_TYPE_TFTP)
			img_tftp.create_tftp_img(project_tree, args, paths)
			
			''' Imagen Full '''
			make_writer_full = makewriter.Makewriter(args, project_tree, paths, constants.BUILD_TYPE_FULL)
			make_writer_full.write_makefile()
			
			os.system('rm -Rf ' + constants.INSTALL_DIR_FULL)
			makeexe.do_install(project_tree, args, paths, constants.BUILD_TYPE_FULL)
			img_full.create_full_img(args, project_tree, paths, compilation_id, sql)
			
			''' Imagen incremental '''
			incr_make_writer = incr_makewriter.IncrMakewriter(args, project_tree, paths)
			incr_project_list = incr_make_writer.write_makefile(compilation_id, sql)
			
			os.system('rm -Rf ' + constants.INSTALL_DIR_INCR)
			makeexe.do_install(project_tree, args, paths, constants.BUILD_TYPE_INCR)		
			img_incr.create_incr_img(args, project_tree, incr_project_list, paths, compilation_id, sql)
			
			for alt_version in project_tree[constants.CMM_PROJECT]:
				project_name = utils.get_full_path(constants.CMM_PROJECT, alt_version, args.compiler)
				break
			os.system("mkdir -p " + paths.work_path + "/md5/")				
			priv_key = paths.build_path + "/" + project_name + constants.CMM_PRIV_KEY_FILE
			logger.info("")
			logger.info("--- Module, MD5 file ---")
			for project, project_data in project_tree.iteritems():
				for version in project_data:
					name = project_tree[project][version]['provides'][0].split('/')[-1]
					for root, dirs, files in os.walk(constants.INSTALL_DIR_TFTP):
						if name in files:
							filepath = os.path.join(root, name)
							sign_file = paths.work_path + "/md5/" + name + "_sign.bin"
							os.system("openssl dgst -MD5 -sign " + priv_key + " -out " + sign_file + " " + filepath)
							logger.info(project + "," + name + "," + name + "_sign.bin")
			
			print ""
			print "Archivo de log en:", logger.get_filename(args, paths)
			print "Archivos MD5 en:", paths.work_path + "/md5/"
			print ""
	except:
		if args.final_release:
			sql.quit()
		print traceback.format_exc()
		exit(1)
	else:
		if args.final_release:
			sql.commit()
			sql.quit()

	

if __name__ == '__main__':
	args = args_parser.get_shell_args(sys.argv[1:])
	args = args_parser.normalize_args(args)
	constants.set_GLOBAL_PROJECT(args.part_number_list, args.fw_family, args.previous_min_versions_list)
	if include_projects.set_include_projects(args.final_release_version):
		print "Include projects not found"
		exit(1)
	project_commits.set_project_commits()
	paths = args_parser.get_paths(args)
	if args.images:
		logger.init(args, paths)
	os.umask(0022)
	doit(args, paths)
	
	'''try:
		doit(args, work_path)
	except Exception as inst:
		logging.error("Program exitted with exception: " + str(inst))
		print "Program exitted with exception: " + str(inst)
		raise Exception()
	else:
		logging.info("Execution completed without errors")
		exit(0)'''
	
	
	

	
	
