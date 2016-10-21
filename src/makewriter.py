#! /usr/bin/python
import argparse, os, logging
from distutils.version import LooseVersion, StrictVersion

import defines as constants
import local
import dependencies
import utils


def get_template(project_path, cc, debug):
	cc_key = 'arm' if cc else 'x86'
	debug_key = 'debug' if debug else 'release'
	
	found = False
	template = ""
	for temp in constants.templates[cc_key][debug_key]:
		if os.path.isfile(project_path + '/mrt/' + temp):
			found = True
			template = project_path + '/mrt/' + temp
			break
	if found:
		temp_file = open(template)
		for line in temp_file:
			if "#TARGETS" in line or "# TARGETS" in line or "#TARGET" in line or "# TARGET" in line:
				if not cc_key + "." + debug_key in line:
					found = False
				break
		temp_file.close()
	return (found, template)
	
def read_template_file(temp_filename):
	section_found = False
	ret = ""
	temp_file = open(temp_filename)
	for line in temp_file:
		if not "#" in line:
			ret += line 
	temp_file.close()
	return ret	


class ProjectWriter:
	def __init__(self, args, project, version, project_tree, build_path, deploy_path, ordered_versions = None):
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
		
		self.ordered_versions = ordered_versions
		
		(ok, self.temp_filename) = get_template(self.project_build_path, self.cross_compile, self.debug)
		if not ok and args.debug:
			(ok, self.temp_filename) = get_template(self.project_build_path, self.cross_compile, False)
			if ok:
				logging.warning("Project " + str(project) + " compiled for release when building debug. Debug template missing.")
		if not ok:
			raise Exception('Template not found for project ' + str(project) + " for modes x86=" + str(not self.cross_compile) + ", debug=" + str(self.debug))

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
			
			
	def project_create_makefile_exe(self):
		temp_text = read_template_file(self.temp_filename)
		
		repl_tags = self.get_common_repl_tags()
		
		
		if self.compile_deps:
			if len(self.project_tree[self.project][self.version]['depends']) > 0:
				for dep in self.project_tree[self.project][self.version]['depends']:
					repl_tags.append(('${DEPLOY_DIR}/' + dep[0] + ' ', '${DEPLOY_DIR}/' + utils.get_full_path(dep[0], dep[1]) + ' '))
					repl_tags.append(('${DEPLOY_DIR}/' + dep[0] + ';', '${DEPLOY_DIR}/' + utils.get_full_path(dep[0], dep[1]) + ';'))
					repl_tags.append(('${DEPLOY_DIR}/' + dep[0] + '/', '${DEPLOY_DIR}/' + utils.get_full_path(dep[0], dep[1]) + '/'))
			
		template_content = ""
		template_content = utils.replace_strings(temp_text, repl_tags)	
		
		
		make_exe = open(self.project_build_path + '/mrt/makefile.final', 'w')
		make_exe.write(template_content)
		make_exe.close()
		
			
	def project_build_target_process(self):
		ret = ''

		depend_provides = ""
		if self.compile_deps:
			depend_provides_list = []
			if len(self.project_tree[self.project][self.version]['depends']) > 0:
				for dep in self.project_tree[self.project][self.version]['depends']:
					depend_provides_list.append("${DEPLOY_DIR}/" + utils.get_full_path(dep[0], dep[1]) + self.project_tree[dep[0]][dep[1]]['provides'][0]) 
			depend_provides = " ".join(depend_provides_list)
		
		#Tags to replace in target template
		repl_tags = [('$MAIN_PROVIDE$', self.get_main_provide()),
						('$PROJECT$', self.project_folder),
						('$DEPEND_PROVIDES$', depend_provides),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final build'),
						('$GCC_BIN_VERSION$', constants.GCC_BIN_VERSION if self.cross_compile else constants.GCC_BIN_x86_VERSION)]
		mk_temp = open(constants.MAIN_DIR + 'templates/build_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
		
		ret = utils.replace_strings(temp_text, repl_tags)
			
		return ret
		
		
	def project_install_target_process(self):
		ret = ''

		install_depends = ""		
		if len(self.project_tree[self.project][self.version]['install_depends']) > 0:
			install_depend_list = []
			for dep in self.project_tree[self.project][self.version]['install_depends']:
				if self.ordered_versions != None and dep in self.ordered_versions:# and self.ordered_versions[dep] > 1:
					for vers in self.ordered_versions[dep]:
						install_depend_list.append(utils.get_full_path(dep, vers) + '_install') 
				else:
					install_depend_list.append(utils.get_full_path(dep, None) + '_install') 
			install_depends = " ".join(install_depend_list)
		
		
		#Tags to replace in PROJECT INSTALL template
		main_provide = self.get_main_provide() + " " + install_depends
		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide() + " " + install_depends,),
						('$PROJECT$', self.project_folder + '_install'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install'),]
		mk_temp = open(constants.MAIN_DIR + 'templates/install_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()

		
		ret = utils.replace_strings(temp_text, repl_tags)
			
		return ret
		
	def project_phony_target_process(self):
		ret = ''
		#Tags to replace in phony template for 'project' tarjet
		repl_tags = [('$DEPENDS$', self.get_main_provide()),
						('$PROJECT$', self.project_folder),
						('$TEMPLATE_CONTENT$', ''),]
		mk_temp = open(constants.MAIN_DIR + 'templates/phony_target.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
		
		return utils.replace_strings(temp_text, repl_tags)
		
	

class Makewriter:
	
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
		
		
	def get_ordered_versions(self):
		project_versions = {}
		for project, project_data in self.project_tree.iteritems():
			for version, version_data in project_data.iteritems():
				if project == self.main_project or self.compile_deps:
					if len(version_data['depends']) > 0:
						for dep in version_data['depends']:
							if not dep[0] in project_versions:
								project_versions[dep[0]] = []
							if not dep[1] in project_versions[dep[0]]:
								project_versions[dep[0]].append(dep[1])
		
		for project, versions in project_versions.iteritems():
			if len(versions) > 1:
				project_versions[project] = utils.order_versions(versions)	
		
		return project_versions
		
		
	def makefile_hdr_process(self):
		repl_tags  = [('$GCC_DIR$', constants.GCC_DIR if self.cross_compile else constants.GCC_DIR_x86),
						('$BUILD_DIR$', self.build_path),
						('$DEPLOY_DIR$', self.deploy_path),
						('$INSTALL_DIR$', constants.INSTALL_DIR),
						('$ROOTFS_DIR$', constants.ROOTFS_DIR),]
							
		mk_temp = open(constants.MAIN_DIR + 'templates/makefile_hdr.tmpl')
		temp_text = mk_temp.read()
		mk_temp.close()
		temp_text = utils.replace_strings(temp_text, repl_tags)
		return temp_text
		
	


	def write_makefile(self):
		
		make_text = self.makefile_hdr_process()
		
		ordered_versions = None
		if not self.local:
			ordered_versions = self.get_ordered_versions()
			
		for project, project_data in self.project_tree.iteritems():
			for version, version_data in project_data.iteritems():
				pr_writer = ProjectWriter(self.args, project, version, self.project_tree, self.build_path, self.deploy_path, ordered_versions)
				
				make_text += pr_writer.project_build_target_process()
				
				make_text += pr_writer.project_phony_target_process()
				
				if self.install and not self.debug and self.cross_compile:
					make_text += pr_writer.project_install_target_process()
				
				pr_writer.project_create_makefile_exe()
		
		
		fid = open(self.work_path + '/Makefile', 'w')
		fid.write(make_text)
		fid.close()
		
		fid = open(constants.MAIN_DIR + 'Makefile', 'w')
		fid.write(make_text)
		fid.close()
		


