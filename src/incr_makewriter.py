#! /usr/bin/python
import argparse, os, logging
from distutils.version import LooseVersion, StrictVersion

import defines as constants
import local
import dependencies
import utils
import mrt_git
import database
from include_projects import *

class IncrProjectWriter:
	def __init__(self, args, project, version, project_tree, paths, compilation_id, sql):
		self.args = args
		self.paths = paths
		self.project = project
		self.version = version
		self.project_tree = project_tree
		self.project_folder = utils.get_full_path(self.project, self.version)
		self.project_build_path = self.paths.build_path + self.project_folder
		self.project_deploy_path = self.paths.deploy_path + self.project_folder
		self.min_version = args.previous_min_version

		self.include = False
		last_commit = None
		
		if self.args.final_release:	
			cur_version = mrt_git.get_last_tag(self.project_build_path)[1]
			cur_commit = mrt_git.get_current_commit(self.project_build_path)[1]
			min_version_commit = sql.GetCommitByVersion(self.project, self.min_version)

		if self.project != constants.UBOOT_PROJECT:
			'''if self.args.final_release:	
				if min_version_commit == None:
					print "Proyecto", self.project, ":",self.version, "no encontrado en releases anteriores"
				elif min_version_commit != cur_commit:
					print "Proyecto", self.project, ":",self.version, "ha cambiado respecto de la anterior release"
				else:
					print "Proyecto", self.project, ":",self.version, "NO ha cambiado respecto de la anterior release, pero verifica dependencias"
				print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
				b = raw_input()
				if b=='y':
					self.include = True
			else:
				print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
				b = raw_input()
				if b=='y':
					self.include = True'''
				
			for proj, inc in INCLUDE_PROJECTS_INCR.iteritems():
				if proj == self.project and inc == 'YES':
					self.include = True
					
			if self.include:
				print "Proyecto", self.project, ":",self.version, "incluido en la actualizacion incremental. Desea corregir? (y/n)"
			else:
				print "Proyecto", self.project, ":",self.version, "NO incluido en la actualizacion incremental. Desea corregir? (y/n)"
			b = raw_input()
			if b=='y':
				if self.args.final_release:	
					if min_version_commit == None:
						print "Proyecto", self.project, ":",self.version, "no encontrado en releases anteriores"
					elif min_version_commit != cur_commit:
						print "Proyecto", self.project, ":",self.version, "ha cambiado respecto de la anterior release"
					else:
						print "Proyecto", self.project, ":",self.version, "NO ha cambiado respecto de la anterior release, pero verifica dependencias"
					print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
					b = raw_input()
					if b=='y':
						self.include = True
				else:
					print "Desea incluir el proyecto", self.project, ":",self.version, "en la actualizacion incremental? (y/n)"
					b = raw_input()
					if b=='y':
						self.include = True
				for proj, inc in INCLUDE_PROJECTS_INCR.iteritems():
					self.include = False
					if proj == self.project and inc == 'YES':
						self.include = True
				
		if self.include and self.args.final_release:
			sql.SetIncrUpdIncluded(compilation_id, self.project, cur_version, incr_upd_included = 1)
			
		

	def get_common_repl_tags(self):
		repl_tags = [('${BUILD_DIR}/' + self.project + ' ', '${BUILD_DIR}/' + self.project_folder + ' '),
						('${DEPLOY_DIR}/' + self.project + ' ', '${DEPLOY_DIR}/' + self.project_folder + ' '),
						('${BUILD_DIR}/' + self.project + ';', '${BUILD_DIR}/' + self.project_folder + ';'),
						('${DEPLOY_DIR}/' + self.project + ';', '${DEPLOY_DIR}/' + self.project_folder + ';'),
						('${BUILD_DIR}/' + self.project + '/', '${BUILD_DIR}/' + self.project_folder + '/'),
						('${DEPLOY_DIR}/' + self.project + '/', '${DEPLOY_DIR}/' + self.project_folder + '/'),
						('${BUILD_DIR}/' + self.project + '\n', '${BUILD_DIR}/' + self.project_folder + '\n'),
						('${DEPLOY_DIR}/' + self.project + '\n', '${DEPLOY_DIR}/' + self.project_folder + '\n'),
						('${MAKE_FLAGS}', self.args.make_params)]
		return repl_tags

	def get_main_provide(self):
		return '${DEPLOY_DIR}/' + self.project_folder + self.project_tree[self.project][self.version]['provides'][0]
			

	def project_install_target_process(self):
		if not self.include:
			return ''
		
		#Tags to replace in PROJECT INSTALL template
		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide(),),
						('$PROJECT$', self.project_folder + '_install'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install'),]
		mk_temp = open(constants.MAIN_DIR + 'templates/install_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
			
		return utils.replace_strings(temp_text, repl_tags)
		
		
	def project_install_target_process_incr_type(self):
		if self.args.project != constants.ROOTFS_PROJECT or self.project != constants.ROOTFS_PROJECT:
			return ''
		
		#Tags to replace in PROJECT INSTALL template
		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide(),),
						('$PROJECT$', self.project_folder + '_install-incr'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install-incr'),]
		mk_temp = open(constants.MAIN_DIR + 'templates/install_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()

		return utils.replace_strings(temp_text, repl_tags)
	

class IncrMakewriter:
	def __init__(self, args, project_tree, paths):
		self.args = args
		self.paths = paths
		self.project_tree = project_tree
		self.args = args

		
	def write_main_makefile_header(self):
		repl_tags  = [('$GCC_DIR$', constants.GCC_DIR_x86 if self.args.no_cross_compile else constants.GCC_DIR),
						('$BUILD_DIR$', self.paths.build_path),
						('$DEPLOY_DIR$', self.paths.deploy_path),
						('$INSTALL_DIR$', constants.INSTALL_DIR_INCR),
						('$ROOTFS_DIR$', constants.ROOTFS_DIR),]
							
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_HEADER_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		temp_text = utils.replace_strings(temp_text, repl_tags)
		return temp_text
		

	def write_makefile(self, compilation_id, sql):
		project_list = []
		make_text = self.write_main_makefile_header()
		
		make_text += "export INCR=1\n"
					
		for project, project_data in self.project_tree.iteritems():
			for version in project_data:
				pr_writer = IncrProjectWriter(self.args, project, version, self.project_tree, self.paths, compilation_id, sql)
				project_text = pr_writer.project_install_target_process()
				if len(project_text) > 0:
					project_list.append(utils.get_full_path(project, version))
				if project == constants.ROOTFS_PROJECT and self.args.images:
					project_text += pr_writer.project_install_target_process_incr_type()
				make_text += project_text
				break
				
		install_project_list = []
		for project in project_list:
			install_project_list.append(project + "_install")
		for version in self.project_tree[constants.ROOTFS_PROJECT]:
			break
		install_project_list.append(utils.get_full_path(constants.ROOTFS_PROJECT, version) + "_install-incr")
		repl_tags = [('$INCR_PROJECTS$', " ".join(install_project_list)),]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_INCR_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		
		make_text += utils.replace_strings(temp_text, repl_tags)
											
		
		fid = open(self.paths.work_path + '/' + constants.INCR_BUILD_MAKEFILE, 'w')
		fid.write(make_text)
		fid.close()
		
		fid = open(constants.MAIN_DIR + '/' + constants.INCR_BUILD_MAKEFILE, 'w')
		fid.write(make_text)
		fid.close()
		
		return project_list
		

if __name__ == '__main__':
	for proj, inc in INCLUDE_PROJECTS_INCR.iteritems():
		if inc == 'YES':
			print "Proyecto", proj, "incluido en la actualizacion incremental. Desea corregir? (y/n)"
		else:
			print "Proyecto", proj, "NO incluido en la actualizacion incremental. Desea corregir? (y/n)"
