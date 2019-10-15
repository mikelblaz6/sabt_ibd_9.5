import ConfigParser, os, sys

import defines as constants
import local
import mrt_git
import utils
import logger

from utils import print_error

#project_tree:  
'''	'project': 'version',
				'provides',
				'depends'
'''

'''Esta clase genera el arbol de dependencias necesario para la construccion del makefile global.
El arbol tiene la siguiente informacion: 
* <proyecto>: <version>: 	'provides': <target principal>   	# extraido de la seccion PROVIDES del archivo 'project'
							'depends': <proyecto>				# extraido de la seccion DEPS del archivo 'project'
							'install_depends': <proyecto>		# extraido de la version INSTALL_DEPS del archivo 'project'
En compilacion local, no se consideraran versiones, con lo que <version> siempre valdra NONE. 
Para compilacion desde git, <version> tomara el valor correspondiente.
'''

class Dependencies:
	def __init__(self, args, paths):
		self.main_project = args.project
		self.local = args.local
		self.compile_deps = args.compile_deps
		self.project_tree = {}
		self.paths = paths
		self.git_last_versions = {}
		self.no_rebuild = args.no_rebuild
		self.compiler = args.compiler
	
	def get_depend_projects(self):
		self.get_depend_projects_iter(self.main_project)
		return self.project_tree

	# Funcion recursiva que recorre todo el arbol de dependencias
	def get_depend_projects_iter(self, project):
		try:
			version = None
			if not project in self.project_tree:
				self.project_tree[project] = {}
				if self.local:
					local.prepare_local(project, None, self.paths.build_path, self.compiler, not self.no_rebuild)
				else:
					version = mrt_git.get_project_source(project, self.paths.build_path, self.compiler)
			else:
				return

			project_build_path = self.paths.build_path + utils.get_full_path(project, version, self.compiler)
			cfg = ConfigParser.RawConfigParser(allow_no_value=True)
			cfg.optionxform=str
			cfg.read(project_build_path + '/mrt/project')
			
			self.project_tree[project][version] = {'provides':[], 'depends':[], 'install_depends':[]}
			for prov in cfg.items('PROVIDES'):
				self.project_tree[project][version]['provides'].append(prov[0])
			if cfg.has_section('INSTALL_DEPS'):
				for fdep in cfg.items('INSTALL_DEPS'):
					self.project_tree[project][version]['install_depends'].append(fdep[0])
					
			if cfg.has_section('DEPS') and self.compile_deps:
				for dependency in cfg.items('DEPS'):
					#Not version checking. Version set to None
					if not dependency[0] in self.project_tree[project][version]['depends']:
						self.project_tree[project][version]['depends'].append(dependency[0])
					self.get_depend_projects_iter(dependency[0])
		except Exception as inst:
			logger.error("Error getting dependencies for project " + str(project) + ", version " + str(version) + ". Exception: " + str(inst))
			print_error("Error getting dependencies for project " + str(project) + ", version " + str(version) + ". Exception: " + str(inst))
			raise Exception()
		

if __name__=='__main__':
	import sys, args_parser
	
	args = args_parser.get_shell_args(sys.argv[1:])
	args = args_parser.normalize_args(args)
	paths = args_parser.get_paths(args)
	dep_processor = Dependencies(args, paths)
	project_tree = dep_processor.get_depend_projects()

	print project_tree
