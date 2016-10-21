import ConfigParser, os, logging

import defines as constants
import local
import mrt_git
import utils


#project_tree:  
'''	'project': 'version',
				'provides',
				'depends'
'''

'''Esta clase genera el arbol de dependencias necesario para la construccion del makefile global.
El arbol tiene la siguiente informacion: 
* <proyecto>: <version>: 	'provides': <target principal>   	# extraido de la seccion PROVIDES del archivo 'project'
							'depends': <proyecto, version>		# extraido de la seccion DEPS del archivo 'project'
							'install_depends': <proyecto>		# extraido de la version INSTALL_DEPS del archivo 'project'
En compilacion local, no se consideraran versiones, con lo que <version> siempre valdra NONE. 
Para compilacion desde git, <version> tomara el valor correspondiente. Es posible tener el mismo proyecto compilado en versiones diferentes,
ya que se hace en carpetas diferentes
'''

class Dependencies:
	def __init__(self, args, build_path, deploy_path):
		self.main_project = args.project
		self.local = args.local
		self.compile_deps = args.compile_deps
		self.project_tree = {}
		self.build_path = build_path
		self.deploy_path = deploy_path
		self.git_last_versions = {}
		self.no_rebuild = args.no_rebuild
	
	def get_depend_projects(self, version):
		if self.local:
			self.get_depend_projects_local(self.main_project, version)
		else:
			self.get_depend_projects_git(self.main_project, version)
		return self.project_tree

	# Funcion recursiva que recorre todo el arbol de dependencias
	def get_depend_projects_local(self, project, version):
		try:
			if not project in self.project_tree:
				if not self.no_rebuild:
					local.prepare_local(project, version, self.build_path)
				self.project_tree[project] = {}
				
			project_build_path = self.build_path + utils.get_full_path(project, version)
			cfg = ConfigParser.RawConfigParser(allow_no_value=True)
			cfg.optionxform = str
			cfg.read(project_build_path + '/mrt/project')
			if not version in self.project_tree[project]:
				self.project_tree[project][version] = {'provides':[], 'depends':[], 'install_depends':[]}
				for prov in cfg.items('PROVIDES'):
					self.project_tree[project][version]['provides'].append(prov[0])
				if cfg.has_section('INSTALL_DEPS'):
					for fdep in cfg.items('INSTALL_DEPS'):
						self.project_tree[project][version]['install_depends'].append(fdep[0])
			if cfg.has_section('DEPS') and self.compile_deps:
				for dependency in cfg.items('DEPS'):
					#Not version checking for local compilations. version set to None
					if not dependency[0] in self.project_tree[project][version]['depends']:
						self.project_tree[project][version]['depends'].append([dependency[0], None])
					self.get_depend_projects_local(dependency[0], None)
		except Exception as inst:
			logging.error("Error getting dependencies for project " + str(project) + ",version " + str(version) + ". Exception: " + str(inst))
			raise inst
		
		
	def get_depend_projects_git(self, project, version):
		self._get_depend_projects_git(project, version)
		self._normalize_git_versions()
		
	# Funcion recursiva que recorre todo el arbol de dependencias
	def _get_depend_projects_git(self, project, version):
		try:
			if not project in self.project_tree or (project in self.project_tree and not version in self.project_tree[project]):
				real_version = mrt_git.get_project_source(project, self.build_path, version)
				self.git_last_versions[project] = real_version
					
				if not project in self.project_tree:
					self.project_tree[project] = {}
			else:
				real_version = version
			cfg = ConfigParser.RawConfigParser(allow_no_value=True)
			project_build_path = self.build_path + utils.get_full_path(project, real_version)
			cfg.read(project_build_path + '/mrt/project')
			if not real_version in self.project_tree[project]:
				self.project_tree[project][real_version] = {'provides':[], 'depends':[], 'install_depends':[]}
				for prov in cfg.items('PROVIDES'):
					self.project_tree[project][real_version]['provides'].append(prov[0])
				if cfg.has_section('INSTALL_DEPS'):
					for fdep in cfg.items('INSTALL_DEPS'):
						self.project_tree[project][real_version]['install_depends'].append(fdep[0])
			if cfg.has_section('DEPS') and self.compile_deps:
				for dependency in cfg.items('DEPS'):
					if not dependency[0] in self.project_tree[project][real_version]['depends']:
						self.project_tree[project][real_version]['depends'].append([dependency[0], dependency[1]])
					self.get_depend_projects_git(dependency[0], dependency[1])
		except Exception as inst:
			logging.error("Error getting dependencies for project " + str(project) + ",version " + str(version) + ". Exception: " + str(inst))
			raise inst
		
				
	''' Esta funcion asigna el campo <version> adecuado a todos los proyectos para los que no se ha especificado version
	Se asigna la version encontrada en el punto mas alto de la rama correspondiente de git'''
	def _normalize_git_versions(self):
		for project, version in self.git_last_versions.iteritems():
			for pt_project, pt_project_data in self.project_tree.iteritems():
				for pt_version, pt_version_data in pt_project_data.iteritems():
					for index in xrange(len(self.project_tree[pt_project][pt_version]['depends'])):
						if self.project_tree[pt_project][pt_version]['depends'][index] == [project, None]:
							self.project_tree[pt_project][pt_version]['depends'][index] = [project, version]
				



if __name__=='__main__':
	project_tree = {}
	get_depend_projects(project_tree, 'nss-pam-ldapd', constants.BUILD_DIR, local = True)

	print project_tree
