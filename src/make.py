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

def doit(args, paths):
	sql = None
	if args.final_release:
		sql = database.Database(args.part_number)
	
	try:
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
				compilation_id = sql.NewRelease(args.final_release_version)
			
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
	paths = args_parser.get_paths(args)
	logger.init(args, paths)
	
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
	
	
	

	
	
