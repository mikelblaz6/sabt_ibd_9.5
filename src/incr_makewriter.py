#! /usr/bin/python
import argparse, os, logging
from distutils.version import LooseVersion, StrictVersion

import defines as constants
import local
import dependencies
import utils
import mrt_git
import database


class IncrProjectWriter:
	def __init__(self, args, project, version, project_tree, build_path, deploy_path, compilation_id = None):
		self.main_project = args.project
		self.local = args.local
		self.compile_deps = args.compile_deps
		self.build_path = build_path
		self.deploy_path = deploy_path
		self.cross_compile = not args.no_cross_compile
		self.make_params = args.make_params
		self.debug = args.debug
		
		self.project = project
		self.version = version
		self.project_tree = project_tree
		self.project_folder = utils.get_full_path(self.project, self.version)
		self.project_build_path = self.build_path + self.project_folder
		self.project_deploy_path = self.deploy_path + self.project_folder

		self.compilation_id = compilation_id
		self.include = False
					
		cur_commit = mrt_git.get_current_commit(self.project_build_path)[1]
		cur_version = mrt_git.get_last_tag(self.project_build_path)[1]
		last_commit = None
		if self.compilation_id != None:
			sql = database.Database()
			last_commit = sql.GetPreviousCommit(self.project, self.compilation_id)
		
		if last_commit == None:
			if self.compilation_id != None:
				print "Proyecto", self.project, ":",self.version, "no encontrado en releases anteriores"
			if self.project != "u-boot":
				print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
				b = raw_input()
				if b=='y':
					self.include = True
		elif last_commit != cur_commit:
			if self.project != "u-boot":
				print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
				b = raw_input()
				if b=='y':
					self.include = True
		

	def get_common_repl_tags(self):
		repl_tags = [('${BUILD_DIR}/' + self.project + ' ', '${BUILD_DIR}/' + self.project_folder + ' '),
						('${DEPLOY_DIR}/' + self.project + ' ', '${DEPLOY_DIR}/' + self.project_folder + ' '),
						('${BUILD_DIR}/' + self.project + ';', '${BUILD_DIR}/' + self.project_folder + ';'),
						('${DEPLOY_DIR}/' + self.project + ';', '${DEPLOY_DIR}/' + self.project_folder + ';'),
						('${BUILD_DIR}/' + self.project + '/', '${BUILD_DIR}/' + self.project_folder + '/'),
						('${DEPLOY_DIR}/' + self.project + '/', '${DEPLOY_DIR}/' + self.project_folder + '/'),
						('${BUILD_DIR}/' + self.project + '\n', '${BUILD_DIR}/' + self.project_folder + '\n'),
						('${DEPLOY_DIR}/' + self.project + '\n', '${DEPLOY_DIR}/' + self.project_folder + '\n'),
						('${MAKE_FLAGS}', self.make_params)]
		return repl_tags

	def get_main_provide(self):
		return '${DEPLOY_DIR}/' + self.project_folder + self.project_tree[self.project][self.version]['provides'][0]
			

	def project_install_target_process(self):
		ret = ''
		
		if self.include == True:
			#Tags to replace in PROJECT INSTALL template

			repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide(),),
							('$PROJECT$', self.project_folder + '_install'),
							('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install'),]
			mk_temp = open(constants.MAIN_DIR + 'templates/install_target.tmpl')
			temp_text = mk_temp.read()
			mk_temp.close()

			ret = utils.replace_strings(temp_text, repl_tags)
			
		return ret
		
		
	def project_install_target_process_incr_type(self):
		ret = ''
		
		if self.main_project != "rootfs" or self.project != "rootfs":
			return ret
		
		#Tags to replace in PROJECT INSTALL template

		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide(),),
						('$PROJECT$', self.project_folder + '_install-incr'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install-incr'),]
		mk_temp = open(constants.MAIN_DIR + 'templates/install_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()

		ret = utils.replace_strings(temp_text, repl_tags)
			
		return ret
	

class IncrMakewriter:
	
	def __init__(self, args, project_tree, build_path, deploy_path, work_path):
		self.main_project = args.project
		self.local = args.local
		self.compile_deps = args.compile_deps
		self.build_path = build_path
		self.deploy_path = deploy_path
		self.cross_compile = not args.no_cross_compile
		self.make_params = args.make_params
		self.debug = args.debug
		self.project_tree = project_tree
		self.work_path = work_path
		self.install = args.install
		self.args = args
		self.to_database = args.final_release
		self.fw_version = args.final_release_version
		
		
	def makefile_hdr_process(self):
		repl_tags  = [('$GCC_DIR$', constants.GCC_DIR if self.cross_compile else constants.GCC_DIR_x86),
						('$BUILD_DIR$', self.build_path),
						('$DEPLOY_DIR$', self.deploy_path),
						('$INSTALL_DIR$', constants.INSTALL_DIR_INCR),
						('$ROOTFS_DIR$', constants.ROOTFS_DIR),]
							
		mk_temp = open(constants.MAIN_DIR + 'templates/makefile_hdr.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
		temp_text = utils.replace_strings(temp_text, repl_tags)
		return temp_text
		

	def write_makefile(self):
		release_db_id = None
		if self.to_database:
			sql = database.Database()
			release_db_id = sql.GetLastRelease()
		
		project_list = []
		make_text = self.makefile_hdr_process()
					
		for project, project_data in self.project_tree.iteritems():
			for version, version_data in project_data.iteritems():
				pr_writer = IncrProjectWriter(self.args, project, version, self.project_tree, self.build_path, self.deploy_path, release_db_id)
				project_text = pr_writer.project_install_target_process()
				if len(project_text) > 0:
					project_list.append(utils.get_full_path(project, version))
				if self.main_project == "rootfs" and project == "rootfs":
					project_text += pr_writer.project_install_target_process_incr_type()
				make_text += project_text
				
		install_project_list = []
		for project in project_list:
			install_project_list.append(project + "_install")
		install_project_list.append("rootfs_install-incr")
		repl_tags = [('$INCR_PROJECTS$', " ".join(install_project_list)),]
		mk_temp = open(constants.MAIN_DIR + 'templates/incr_install.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
		
		make_text += utils.replace_strings(temp_text, repl_tags)
											
		
		fid = open(self.work_path + '/Makefile_incr', 'w')
		fid.write(make_text)
		fid.close()
		
		fid = open(constants.MAIN_DIR + 'Makefile_incr', 'w')
		fid.write(make_text)
		fid.close()
		
		return project_list
		


