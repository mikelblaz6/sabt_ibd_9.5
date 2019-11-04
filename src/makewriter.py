#! /usr/bin/python
import os, sys
import mrt_argparse
from distutils.version import LooseVersion, StrictVersion

import defines as constants
import local
import dependencies
import utils
import mrt_git
import database
import logger

from utils import print_error


def get_template(project_path, cc, debug):
	cc_key = constants.ARM_TEMPLATE_SUFFIX if cc else constants.X86_TEMPLATE_SUFFIX
	debug_key = constants.DEBUG_TEMPLATE_SUFFIX if debug else constants.RELEASE_TEMPLATE_SUFFIX
	
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
	ret = ""
	temp_file = open(temp_filename)
	for line in temp_file:
		if not "#" in line:
			ret += line 
	temp_file.close()
	return ret	


'''Esta clase rellena los apartados de cada proyecto dentro del makefile general, 
asi como las plantillas de los makefiles de cada proyecto con los datos especificos a la compilacion:
'''
class ProjectWriter:
	def __init__(self, args, project, version, project_tree, paths, compilation_id = None, sql = None):
		self.args = args
		self.paths = paths	
		self.project = project
		self.version = version
		self.project_tree = project_tree
		self.project_folder = utils.get_full_path(self.project, self.version, args.compiler)
		self.project_build_path = self.paths.build_path + self.project_folder
		self.project_deploy_path = self.paths.deploy_path + self.project_folder
		
		(ok, self.template_filename) = get_template(self.project_build_path, not self.args.no_cross_compile, self.args.debug)
		if not ok and self.args.debug:
			(ok, self.template_filename) = get_template(self.project_build_path, not self.args.no_cross_compile, False)
			if ok:
				logger.warning("Project " + str(project) + " compiled for release when building debug. Debug template missing.")
				print("WARNING: Project " + str(project) + " compiled for release when building debug. Debug template missing.")
		if not ok:
			logger.error('Template not found for project ' + str(project) + " for modes x86=" + str(self.args.no_cross_compile) + ", debug=" + str(self.args.debug))
			print_error('Template not found for project ' + str(project) + " for modes x86=" + str(self.args.no_cross_compile) + ", debug=" + str(self.args.debug))
			raise Exception()
			
		cur_commit = mrt_git.get_current_commit(self.project_build_path)[1]
		if self.args.git:
			logger.info(str(self.project) + ". Commit id: " + str(cur_commit))
			print(str(self.project) + ". Commit id: " + str(cur_commit))
			if self.args.final_release and sql != None:
				sql.NewModule(compilation_id, self.project, cur_commit, tftp_img_included = 1)
		else:
			logger.info(str(self.project) + ". Local commit id: " + str(cur_commit))
			print(str(self.project) + ". Local Commit id: " + str(cur_commit))


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
			
			
	''' Crea el makefile del proyecto rellenando su plantilla.'''
	def project_create_makefile_exe(self):
		temp_text = read_template_file(self.template_filename)
		
		repl_tags = self.get_common_repl_tags()
		
		#if self.args.compile_deps:
		if len(self.project_tree[self.project][self.version]['depends']) > 0:
			for dep in self.project_tree[self.project][self.version]['depends']:
				for version in self.project_tree[dep]:
					break #solo una version por proyecto
				repl_tags.append(('${DEPLOY_DIR}/' + dep + ' ', '${DEPLOY_DIR}/' + utils.get_full_path(dep, version, self.args.compiler) + ' '))
				repl_tags.append(('${DEPLOY_DIR}/' + dep + ';', '${DEPLOY_DIR}/' + utils.get_full_path(dep, version, self.args.compiler) + ';'))
				repl_tags.append(('${DEPLOY_DIR}/' + dep + '/', '${DEPLOY_DIR}/' + utils.get_full_path(dep, version, self.args.compiler) + '/'))
			
		make_exe = open(self.project_build_path + '/mrt/makefile.final', 'w')
		make_exe.write(utils.replace_strings(temp_text, repl_tags)	)
		make_exe.close()
		
			
	''' Rellena el apartado build del proyecto dentro del makefile general '''
	def project_build_target_process(self):
		depend_provides = ""
		if self.args.compile_deps:
			depend_provides_list = []
			if len(self.project_tree[self.project][self.version]['depends']) > 0:
				for dep in self.project_tree[self.project][self.version]['depends']:
					for version in self.project_tree[dep]:
						break #solo una version por proyecto
					depend_provides_list.append("${DEPLOY_DIR}/" + utils.get_full_path(dep, version, self.args.compiler) + self.project_tree[dep][version]['provides'][0]) 
			depend_provides = " ".join(depend_provides_list)
		
		#Tags to replace in target template
		repl_tags = [('$MAIN_PROVIDE$', self.get_main_provide()),
						('$PROJECT$', self.project_folder),
						('$DEPEND_PROVIDES$', depend_provides),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final build'),
						('$GCC_BIN_VERSION$', constants.GCC_BIN_x86_VERSION if self.args.no_cross_compile else constants.GCC_BIN_VERSION)]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_BUILD_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		
		return utils.replace_strings(temp_text, repl_tags)
	
	''' Rellena el apartado phony del proyecto dentro del makefile general '''
	def project_phony_target_process(self):
		#Tags to replace in phony template for 'project' tarjet
		repl_tags = [('$DEPENDS$', self.get_main_provide()),
						('$PROJECT$', self.project_folder),
						('$TEMPLATE_CONTENT$', ''),]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_PHONY_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		
		return utils.replace_strings(temp_text, repl_tags)
		
	''' Rellena el apartado install del proyecto dentro del makefile general '''
	def project_install_target_process(self):
		install_depends = ""		
		if len(self.project_tree[self.project][self.version]['install_depends']) > 0:
			install_depend_list = []
			for dep in self.project_tree[self.project][self.version]['install_depends']:
				for version in self.project_tree[dep]:
					break #solo una version por proyecto
				install_depend_list.append(utils.get_full_path(dep, version, self.args.compiler) + '_install') 
			install_depends = " ".join(install_depend_list)
		
		#Tags to replace in PROJECT INSTALL template
		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide() + " " + install_depends,),
						('$PROJECT$', self.project_folder + '_install'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install'),]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_INSTALL_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()

		return utils.replace_strings(temp_text, repl_tags)
		
	def project_install_target_process_build_type(self, build_type):
		if self.args.project != constants.ROOTFS_PROJECT or self.project != constants.ROOTFS_PROJECT:
			return ''
		
		if build_type == None:
			install_target_suffix = ''
		elif build_type == constants.BUILD_TYPE_FULL:
			install_target_suffix = '-full'
		elif build_type == constants.BUILD_TYPE_TFTP:
			install_target_suffix = '-tftp'

		
		#Tags to replace in PROJECT INSTALL template
		repl_tags = [('$DEPEND_PROVIDES$', self.get_main_provide(),),
						('$PROJECT$', self.project_folder + '_install' + install_target_suffix),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final install' + install_target_suffix),]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_INSTALL_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()

		return utils.replace_strings(temp_text, repl_tags)
		
	
		
	def project_image_target_process(self):
		if self.args.project != constants.ROOTFS_PROJECT or self.project != constants.ROOTFS_PROJECT:
			return ''
			
		#Tags to replace in phony template for 'project' tarjet
		repl_tags = [('$PROJECT$', self.project_folder + '_image'),
						('$TEMPLATE_CONTENT$', '\t$(MAKE) -C ' + '${BUILD_DIR}/' + self.project_folder + ' -f mrt/makefile.final create_img'),]
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_IMAGE_TARGET_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		
		return utils.replace_strings(temp_text, repl_tags)
	
	
	
'''Esta clase genera los makefiles necesarios para la compilacion del proyecto.
* Un makefile global para el proyecto que realiza llamadas a los makefiles de los proyectos individuales, teniendo
en cuenta las dependencias extraidas en el arbol del proyecto.
* Rellena las plantillas de los makefiles de cada proyecto con los datos especificos a la compilacion
'''
class Makewriter:
	
	def __init__(self, args, project_tree, paths, build_type = None):
		self.paths = paths
		self.project_tree = project_tree
		self.build_type = build_type
		self.args = args
		
		
	def write_main_makefile_header(self):	
		if self.build_type == constants.BUILD_TYPE_TFTP:
			install_dir = constants.INSTALL_DIR_TFTP
		elif self.build_type == constants.BUILD_TYPE_FULL:
			install_dir = constants.INSTALL_DIR_FULL
		else:
			install_dir = constants.INSTALL_DIR_GENERIC		

		
		repl_tags  = [('$GCC_DIR$', constants.GCC_DIR_x86 if self.args.no_cross_compile else constants.GCC_DIR),
						('$BUILD_DIR$', self.paths.build_path),
						('$DEPLOY_DIR$', self.paths.deploy_path),
						('$INSTALL_DIR$', install_dir),
						('$ROOTFS_DIR$', constants.ROOTFS_DIR),
						('$PART_NUMBER_LIST$', self.args.part_number_list),
						('$FW_FAMILY$', self.args.fw_family),]
							
		mk_temp = open(constants.MAIN_DIR + constants.MAKEFILE_HEADER_TEMPLATE_FILE)
		temp_text = mk_temp.read()
		mk_temp.close()
		temp_text = utils.replace_strings(temp_text, repl_tags)
		return temp_text
		
	
	def write_makefile(self, compilation_id = None, sql = None):
		main_makefile_text = self.write_main_makefile_header()

		logger.info("")
		logger.info("--- Module, Current_commit ---")
		for project, project_data in self.project_tree.iteritems():
			for version in project_data:
				pr_writer = ProjectWriter(self.args, project, version, self.project_tree, self.paths, compilation_id, sql)
				
				main_makefile_text += pr_writer.project_build_target_process()
				
				main_makefile_text += pr_writer.project_phony_target_process()
				
				if self.args.install:
					main_makefile_text += pr_writer.project_install_target_process()
					
					if project == constants.ROOTFS_PROJECT and self.args.images:
						main_makefile_text += pr_writer.project_install_target_process_build_type(self.build_type)
						main_makefile_text += pr_writer.project_image_target_process()
					
				pr_writer.project_create_makefile_exe()
		
		
		if self.build_type == constants.BUILD_TYPE_TFTP:
			main_makefile_name = constants.TFTP_BUILD_MAKEFILE
		elif self.build_type == constants.BUILD_TYPE_FULL:
			main_makefile_name = constants.FULL_BUILD_MAKEFILE
		else:
			main_makefile_name = constants.GENERIC_MAKEFILE	

		# Se guarda el makefile en la ruta raiz del pryecto project_compiler y en la carpeta log
		fid = open(self.paths.work_path + '/' + main_makefile_name, 'w')
		fid.write(main_makefile_text)
		fid.close()
		
		fid = open(constants.MAIN_DIR + main_makefile_name, 'w')
		fid.write(main_makefile_text)
		fid.close()



