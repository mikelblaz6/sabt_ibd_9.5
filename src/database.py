import MySQLdb, time

import defines as constants
import tabulate

OLD_DB_NAME = '402_12_fw_versions'

part_number_list = (('402.12.00', '402_12_00', '1.0.2', {'1.0.2':'1.0.2', '1.0.3':'1.0.2', '1.0.4':'1.0.2', 
																'1.1.0':'1.0.2', '1.1.2':'1.1.0', '1.1.3':'1.1.0'}),
							('402.12.01', '402_12_01', '1.0.2', {'1.0.2':'1.0.2', '1.0.3':'1.0.2', '1.0.4':'1.0.2', 
																'1.0.5':'1.0.2', '1.0.6':'1.0.2', '1.0.7':'1.0.2',
																'1.2.0':'1.0.2'}),
							('402.12.02', '402_12_02', '1.0.2', {'1.0.2':'1.0.2', '1.0.3':'1.0.2', '1.0.4':'1.0.2', '1.1.0':'1.0.2'}),
							('402.12.03', '402_12_03', '1.0.2', {'1.0.2':'1.0.2', '1.0.3':'1.0.2', '1.0.4':'1.0.2', '1.1.0':'1.0.2'}),
							('402.12.04', '402_12_04', '1.0.2', {'1.0.2':'1.0.2', '1.0.4':'1.0.2', '1.2.0':'1.0.2', '1.2.1':'1.0.2', '1.2.2':'1.2.1'}),
							('402.12.05.01', '402_12_05_01', '1.0.3', {'1.0.3':'1.0.3',}),
							('402.12.06', '402_12_06', '1.1.0', {'1.1.0':'1.1.0',}),
							('402.12.07', '402_12_07', '1.1.1', {'1.1.1':'1.1.1', '1.1.2':'1.1.1', '1.1.3':'1.1.1'}),)

def print_error(data):
	print data

def GetTime():
	a = time.localtime(time.time())
	return time.strftime("%Y/%m/%d %H:%M:%S",a)
	

#===============================================================================
# class OldDatabase:
#     def __del__(self):
#         self.quit()
# 
#     def __init__(self, tmout = 15):
#         self.con = MySQLdb.connect(DB_HOST, DB_USER, DB_PWD, OLD_DB_NAME)
#         self.cur = self.con.cursor()
#         
#     def quit(self):
#         try:
#             self.cur.close()
#         except:
#             pass
# 
#         try:
#             self.con.close()
#         except:
#             pass
# 
#     def get_compilations(self, db_table_prefix):
#         query = "".join(["SELECT * FROM `", db_table_prefix, "_compilations` ORDER BY `id`"])
#         self.cur.execute(query)
#         return self.cur.fetchall()
#         
#     def get_modules(self, db_table_prefix, comp_id=None):
#         query = "".join(["SELECT * FROM `", str(db_table_prefix), "_modules`"])
#         if comp_id != None:    
#             query = "".join([query, " WHERE `comp_id`=", str(comp_id)])
#         query = "".join([query, " ORDER BY `id`"])
#         self.cur.execute(query)
#         return self.cur.fetchall()
#===============================================================================


class Database:    
	def __del__(self):
		self.quit()

	def __init__(self, tmout = 15):
		#self.con = sqlite3.connect('/home/jonathan/Desktop/PART_NUMBERS', timeout = 5)
		self.con = MySQLdb.connect(constants.DB_HOST, constants.DB_USER, constants.DB_PWD, constants.DB_NAME)
		self.cur = self.con.cursor()
		self.cur.execute("begin")
		
		self.get_full_info_query = "SELECT c1.id, p1.name AS part_number, f1.name AS fw_family, \
c1.fw_version, c1.date, c1.command_line, \
c2.fw_version AS min_fw_version, f2.name AS prev_family, pn1.id \
FROM compilations c1 \
INNER JOIN part_number_compatibility pn1 ON c1.id=pn1.comp_id \
INNER JOIN version_compatibility vc ON pn1.id=vc.pn_comp_id \
INNER JOIN part_number_compatibility pn2 ON vc.min_compatible_pn_comp_id=pn2.id \
INNER JOIN compilations c2 ON pn2.comp_id=c2.id \
INNER JOIN fw_family f1 ON c1.fw_family_id=f1.id \
INNER JOIN fw_family f2 ON c2.fw_family_id=f2.id \
INNER JOIN part_number p1 ON pn1.part_number_id=p1.id"
									
		self.get_comp_pn_query = "SELECT * FROM part_number_compatibility pn1 INNER JOIN compilations c1 ON pn1.comp_id=c1.id"
		
		
	def quit(self):
		try:
			self.cur.close()
		except:
			pass

		try:
			self.con.close()
		except:
			pass
		
	def commit(self):
		self.con.commit()
		
	
	def insert_into_compilations(self, fw_family_id, fw_version, date, command_line = ""):
		query = "INSERT INTO `compilations` (`fw_family_id`, `fw_version`, `date`, `command_line`) VALUES (%s,%s,%s,%s)"
		data = (fw_family_id, str(fw_version), str(date), str(command_line))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid    
	
	def insert_into_packages(self, name, version, date):
		query = "INSERT INTO `packages` (`name`, `version`, `date`) VALUES (%s,%s,%s)"
		data = (str(name), str(version), str(date))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid   
	
	def insert_into_packages_compilations(self, comp_id, pck_id):
		query = "INSERT INTO `packages_compilations` (`pck_id`, `comp_id`) VALUES (%s,%s)"
		data = (pck_id, comp_id)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid 
		
	def insert_into_part_number_compatibility(self, comp_id, part_number_id):
		query = "INSERT INTO `part_number_compatibility` (`comp_id`, `part_number_id`) VALUES (%s,%s)"
		data = (comp_id, part_number_id)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid
		
	def insert_into_version_compatibility(self, pn_comp_id, min_compatible_pn_comp_id):
		query = "INSERT INTO `version_compatibility` (`pn_comp_id`, `min_compatible_pn_comp_id`) VALUES (%s,%s)"
		data = (pn_comp_id, min_compatible_pn_comp_id)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid
		
	def insert_into_modules(self, comp_id, name, commit, tftp_img_included, full_upd_included, incr_upd_included):
		query = "INSERT INTO `modules` (`comp_id`, `name`, `commit`, `tftp_img_included`, `full_upd_included`, `incr_upd_included`) VALUES (%s,%s,%s,%s,%s,%s)"
		data = (comp_id, str(name), str(commit), tftp_img_included, full_upd_included, incr_upd_included)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.lastrowid
	
	def update_full_incl_into_modules(self, comp_id, name, full_upd_included):
		query = "UPDATE `modules` SET `full_upd_included`=%s WHERE `comp_id`=%s AND `name`=%s"
		data = (full_upd_included, comp_id, str(name))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		
	def update_incr_incl_into_modules(self, comp_id, name, incr_upd_included):
		query = "UPDATE `modules` SET `incr_upd_included`=%s WHERE `comp_id`=%s AND `name`=%s"
		data = (incr_upd_included, comp_id, str(name))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		
	def get_fw_family_id(self, fw_family):
		query = "SELECT `id` FROM `fw_family` WHERE `name`=%s"
		data = (str(fw_family),)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchone()
		
	def get_part_number_id(self, part_number):
		query = "SELECT `id` FROM `part_number` WHERE `name`=%s"
		data = (str(part_number),)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchone()
		
	def get_pn_comps_from_pn_fam_fw(self, part_number, fw_family, fw_version):
		query = "".join([self.get_comp_pn_query, " WHERE c1.fw_version=%s \
AND pn1.part_number_id=(SELECT `id` FROM `part_number` WHERE `name`=%s) \
AND c1.fw_family_id=(SELECT `id` FROM `fw_family` WHERE `name`=%s)"])
		data = (str(fw_version), str(part_number), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
		
	def get_pn_comps_from_fam_fw(self, fw_family, fw_version):
		query = "".join([self.get_comp_pn_query, " WHERE c1.fw_version=%s AND c1.fw_family_id=(SELECT `id` FROM `fw_family` WHERE `name`=%s)"])
		data = (str(fw_version), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
		
	def get_modules_from_comp_id(self, comp_id):
		query = "SELECT * FROM `modules` WHERE `comp_id`=%s ORDER BY `name`"
		data = (comp_id,)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
		
	def get_full_info_from_pn(self, part_number):
		query = "".join([self.get_full_info_query, " WHERE pn1.part_number_id=(SELECT `id` FROM `part_number` WHERE `name`=%s)"])
		data = (str(part_number),)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
		
	def get_full_info_from_pn_fam_fw(self, part_number, fw_family, fw_version):
		query = "".join([self.get_full_info_query, 
" WHERE pn1.part_number_id=(SELECT `id` FROM `part_number` WHERE `name`=%s) \
AND c1.fw_version=%s \
AND c1.fw_family_id=(SELECT `id` FROM `fw_family` WHERE `name`=%s)"])
		data = (str(part_number), str(fw_version), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
		
	def get_full_info_from_fam_fw(self, fw_family, fw_version):
		query = "".join([self.get_full_info_query, " WHERE c1.fw_version=%s AND c1.fw_family_id=(SELECT `id` FROM `fw_family` WHERE `name`=%s)"])
		data = (str(fw_version), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
	
	def get_full_info_from_pck(self, pck_id):
		query = "".join([self.get_full_info_query, " WHERE c1.id=%s"])
		data = (pck_id,)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
	
	def get_module_from_version_family(self, name, fw_family, version):
		query = "SELECT * FROM `modules` WHERE `name`=%s AND `comp_id`=(SELECT `id` FROM `compilations` WHERE `fw_version`=%s AND `fw_family_id`=(SELECT `id` FROM `fw_family` WHERE `name`=%s))"
		data = (str(name), str(version), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
	
	def get_module_from_version_part_number(self, name, fw_family, version, part_number):
		query = "SELECT * FROM `modules` WHERE `name`=%s AND \
`comp_id`=(SELECT pn1.id FROM part_number_compatibility pn1 \
INNER JOIN compilations c1 ON pn1.comp_id=c1.id WHERE pn1.part_number_id=(SELECT `id` FROM `part_number` WHERE `name`=%s) \
AND c1.fw_version=%s AND c1.fw_family_id=(SELECT `id` FROM `fw_family` WHERE `name`=%s))"
		data = (str(name), str(part_number), str(version), str(fw_family))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()

	def get_part_number_name(self, part_number_id):
		query = "SELECT name FROM part_number WHERE `id`=%s"
		data = (str(part_number_id),)
		self.cur.execute(query, data)
		return self.cur.fetchone()
	
	def get_comp_id(self, fw_family, version):
		ret = None
		query = "SELECT `id` FROM `compilations` WHERE `fw_version`=%s AND `fw_family_id`=(SELECT `id` FROM `fw_family` WHERE `name`=%s)"
		data = (str(version), str(fw_family))
		self.cur.execute(query, data)
		rows = self.cur.fetchone()
		if len(rows) > 0:
			ret = rows[0]
		return ret
	
	def get_comp_info(self, comp_id):
		query = "SELECT c1.id, c1.fw_version, c1.date, c1.command_line, f1.name FROM compilations c1 \
INNER JOIN fw_family f1 ON c1.fw_family_id=f1.id \
WHERE c1.id=%s"
		data = (comp_id,)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
	
	def get_pck_info(self, name, version):
		query = "SELECT p1.name, p1.version, p1.date, c1.comp_id, p1.id FROM packages p1 \
INNER JOIN packages_compilations c1 ON p1.id=c1.pck_id \
WHERE p1.name=%s AND p1.version=%s"
		data = (str(name), str(version))
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchall()
	
	def get_fw_family_code(self, fw_family):
		query = "SELECT `code` FROM fw_family WHERE `name`=%s"
		data=(str(fw_family),)
		self.cur.execute(query, data)
		#print self.cur._last_executed
		return self.cur.fetchone()[0]
	
	def delete_from_version_compatibility(self, pn_comp_id):
		query = "DELETE FROM version_compatibility WHERE pn_comp_id=%s"
		data = (pn_comp_id,)
		self.cur.execute(query, data)
		
	def delete_from_part_number_compatibility(self, comp_id):
		query = "DELETE FROM part_number_compatibility WHERE comp_id=%s"
		data = (comp_id,)
		self.cur.execute(query, data)
		
	def delete_from_modules(self, comp_id):
		query = "DELETE FROM modules WHERE comp_id=%s"
		data = (comp_id,)
		self.cur.execute(query, data)
		
	def delete_from_compilations(self, comp_id):
		query = "DELETE FROM compilations WHERE `id`=%s"
		data = (comp_id,)
		self.cur.execute(query, data)
		
	def delete_from_packages(self, pck_id):
		query = "DELETE FROM packages WHERE `id`=%s"
		data = (pck_id,)
		self.cur.execute(query, data)
			
#===============================================================================
#     def Migrate(self):    
#         old_db = OldDatabase()
#         legacy_fw_family_id = self.get_fw_family_id('None')[0]            
#         
#         for pn in part_number_list:
#             part_number_id = self.get_part_number_id(pn[0])[0]
#             min_fw_version = pn[2]
#             old_compilations = old_db.get_compilations(pn[1])
# 
#             for old_comp in old_compilations:
#                 old_comp_id = old_comp[0]
#                 old_comp_fw_version = old_comp[1]
#                 old_comp_date = old_comp[2]
#                 
#                 if old_comp_fw_version >= min_fw_version:
#                     comp_id = self.insert_into_compilations(legacy_fw_family_id, old_comp_fw_version, old_comp_date)
#                     pn_comp_id = self.insert_into_part_number_compatibility(comp_id, part_number_id)
#                     
#                     if old_comp_fw_version != min_fw_version:
#                         min_pn_comp_id = self.get_pn_comps_from_pn_fam_fw(part_number_id, legacy_fw_family_id, pn[3][old_comp_fw_version])[0][0]
#                         self.insert_into_version_compatibility(pn_comp_id, min_pn_comp_id)
#                     else:
#                         self.insert_into_version_compatibility(pn_comp_id, pn_comp_id)
#                                                 
#                     modules = old_db.get_modules(pn[1], old_comp_id)
#                     
#                     for module in modules:
#                         self.insert_into_modules(comp_id, module[2], module[3], module[5], module[6], module[7])
#         return 0
#===============================================================================


				
	def GetCommitByVersionFamily(self, name, fw_family, version):
		ret = None
		rows = self.get_module_from_version_family(name, fw_family, version)
		if len(rows) > 0:
			ret = rows[0][3]  
		return ret
		
	def GetCommitByVersionPartNumber(self, name, part_number, version):
		ret = None
		rows = self.get_module_from_version_part_number(name, "None", version, part_number)
		if len(rows) > 0:
			ret = rows[0][3]  
		return ret
		
	def GetModulesInfo(self, part_number, fw_version, fw_family):
		if self.get_part_number_id(part_number) == None:
			print "Part-number not allowed"
			return 1
			
		if self.get_fw_family_id(fw_family) == None:
			print "Fw family not allowed"
			return 1
					
		fw_compilations = self.get_full_info_from_pn_fam_fw(part_number, fw_family, fw_version)
		if len(fw_compilations) == 0:
			print "Fw not produced"
			return 1
			
		modules = self.get_modules_from_comp_id(fw_compilations[0][0])
				
		print ""
		print "-------- PART NUMBER", part_number, " -- FW VERSION", fw_version, " -- FW FAMILY", fw_family, " --- INFORMATION -------------------------------"
		print "Compilation id:", fw_compilations[0][0]
		print "Part number:", fw_compilations[0][1]
		print "Fw version:", fw_compilations[0][3]
		print "Fw family:", fw_compilations[0][2]
		print "Date:", fw_compilations[0][4]
		print "Command line:", fw_compilations[0][5]
		data = "Min versions: \n"
		for comp in fw_compilations:
			if comp[6] != fw_version:
				data += "     Version " + comp[6] + ", Fw family " + comp[7] + "\n"
		print data
		modules_to_print = []
		for module in modules:
			modules_to_print.append(module[2:])
		print(tabulate.tabulate(modules_to_print, headers = ["Module", "Commit id", "Tftp img included", "Full img included", "Incr upd included"]))
		print ""
		print ""
		
	def GetInfoForPartNumber(self, part_number):
		if self.get_part_number_id(part_number) == None:
			print "Part-number not allowed"
			return 1
			
		fw_compilations = self.get_full_info_from_pn(part_number)
		
		print ""
		print "-------- PART NUMBER", part_number, "INFORMATION --------------"
		info_to_print = []
		for comp in fw_compilations:
			min_version = comp[6]
			prev_family = comp[7]
			if min_version == comp[3] and prev_family == comp[2]:
				min_version = 'None'
				prev_family = 'None'
			info_to_print.append([comp[3], comp[2], comp[4], min_version, prev_family])
		print(tabulate.tabulate(info_to_print, headers = ["Version", "Fw family", "Date", "Min version", "Previous family"]))
		print ""
		print ""
		#print "   Version:",comp[3],"Family:",comp[2],"Date:",comp[4],"Min version:",min_version,"Previous family:",prev_family
		

	#===========================================================================
	# def LegacyNewRelease(self, fw_version):
	#     query = "".join(["INSERT INTO `", constants.DB_TABLES_PREFIX, "compilations` (`fw_version`, `date`) VALUES ('",str(fw_version),"','",str(GetTime()),"')"])
	#     print query
	#     
	#     try:
	#         self.cur.execute(query)
	#     except Exception as inst:
	#         print_error("Error database query: " + query + ". Exception:" + str(inst))
	#         raise Exception()
	#     else:
	#         return self.cur.lastrowid
	#===========================================================================
	
	def VerifyNewRelease(self, fw_family, fw_version, part_number_list, min_versions_list, legacy_min_version_list = None):
		part_numbers = part_number_list.split(',')
		min_versions_tmp = min_versions_list.split(';')
		min_versions = []
		for min_vers_tmp in min_versions_tmp:
			min_versions.append((min_vers_tmp.split(',')[0], min_vers_tmp.split(',')[1]))
		legacy_min_versions = None
		if legacy_min_version_list != None:
			legacy_min_versions = legacy_min_version_list.split(',')
		
		if fw_family == 'None':
			print "Error Fw family not allowed for new releases"
			return 1
			
		if self.get_fw_family_id(fw_family) == None:
			print "Error Fw family not registered"
			return 1
		
		entries = self.get_pn_comps_from_fam_fw(fw_family, fw_version)
		if len(entries) != 0:
			print "Error Fw version already deployed"
			return 1
			
		for min_vers in min_versions:
			if self.get_fw_family_id(min_vers[0]) == None:
				print "Error Prev fw family not allowed"
				return 1
				
			if min_vers[1] != fw_version:
				comp_entry = self.get_pn_comps_from_fam_fw(min_vers[0], min_vers[1])
				if len(comp_entry) == 0:
					print "Error Prev version not deployed"
					return 1
					
		if legacy_min_version_list != None and \
			(len(legacy_min_versions) != len(part_numbers)):
			print "Error on legacy versions length"
			return 1
		
		index = 0
		for part_number in part_numbers:
			if self.get_part_number_id(part_number) == None:
				print "Error Part-number not allowed"
				return 1
			
			if legacy_min_version_list != None and legacy_min_versions[index] != 'None':
				entries = self.get_pn_comps_from_pn_fam_fw(part_number, 'None', legacy_min_versions[index])
				if len(entries) == 0:
					print "Error Previous legacy release not found for pn", part_number
					return 1
								
			index += 1
			
		return 0
		
	def NewRelease(self, fw_family, fw_version, part_number_list, min_versions_list, command_line = "", legacy_min_version_list = None):
		part_numbers = part_number_list.split(',')
		min_versions_tmp = min_versions_list.split(';')
		min_versions = []
		for min_vers_tmp in min_versions_tmp:
			min_versions.append((min_vers_tmp.split(',')[0], min_vers_tmp.split(',')[1]))
		legacy_min_versions = None
		if legacy_min_version_list != None:
			legacy_min_versions = legacy_min_version_list.split(',')
		fw_family_id = self.get_fw_family_id(fw_family)[0]
		  
		comp_id = self.insert_into_compilations(fw_family_id, fw_version, GetTime(), command_line)

		index = 0
		for part_number in part_numbers:
			part_number_id = self.get_part_number_id(part_number)[0]
			
			prev_comp_ids = []
			if legacy_min_version_list != None and legacy_min_versions[index] != 'None':
				prev_comps_info = self.get_pn_comps_from_pn_fam_fw(part_number, 'None', legacy_min_versions[index])
				for prev_comp in prev_comps_info:
					print prev_comp
					prev_comp_ids.append(prev_comp[0])
			
			for min_vers in min_versions:
				prev_fw_family = min_vers[0]
				min_fw_version = min_vers[1]
				prev_comps_info = self.get_pn_comps_from_pn_fam_fw(part_number, prev_fw_family, min_fw_version)
				for prev_comp in prev_comps_info:
					print prev_comp
					prev_comp_ids.append(prev_comp[0])
			
			pn_comp_id = self.insert_into_part_number_compatibility(comp_id, part_number_id)
			if len(prev_comp_ids) == 0:
				prev_comp_ids.append(pn_comp_id)
			for prev_comp_id in prev_comp_ids:
				self.insert_into_version_compatibility(pn_comp_id, prev_comp_id)
					
			index += 1
			
		return comp_id
	
	def VerifyNewPackage(self, included_versions):
		included_versions_tmp = included_versions.split(';')
		included_versions = []
		for included_vers_tmp in included_versions_tmp:
			included_versions.append((included_vers_tmp.split(',')[0], included_vers_tmp.split(',')[1]))
			
		for version in included_versions:
			if version[0] == None:
				print "Package creation only for family compatible fws"
				return 1
			
			if self.get_comp_id(version[0], version[1]) == None:
				print "Error. Fw version not found:", version[0],version[1]
				return 1
			
		return 0
	
	def NewPackage(self, name, version, included_versions):
		included_versions_tmp = included_versions.split(';')
		included_versions = []
		for included_vers_tmp in included_versions_tmp:
			included_versions.append((included_vers_tmp.split(',')[0], included_vers_tmp.split(',')[1]))
			
		pck_id = self.insert_into_packages(name, version, GetTime())
		for version in included_versions:
			self.insert_into_packages_compilations(self.get_comp_id(version[0], version[1]), pck_id)
						
		return pck_id
			
	def NewModule(self, compilation_id, name, commit, tftp_img_included):
		self.insert_into_modules(compilation_id, name, commit, tftp_img_included, 0, 0)
			
	def SetFullUpdIncluded(self, compilation_id, name, full_upd_included):
		self.update_full_incl_into_modules(compilation_id, name, full_upd_included)
			
	def SetIncrUpdIncluded(self, compilation_id, name, incr_upd_included):
		self.update_incr_incl_into_modules(compilation_id, name, incr_upd_included)
		
	def RemoveRelease(self, fw_family, fw_version):
		if self.get_fw_family_id(fw_family) == None:
			print "Fw family not allowed"
			return 1
		
		entries = self.get_pn_comps_from_fam_fw(fw_family, fw_version)
		if len(entries) == 0:
			print "Fw version not deployed"
			return 1
		
		for entry in entries:
			self.delete_from_version_compatibility(entry[0])
		
		comp_id = entries[0][3]
		self.delete_from_part_number_compatibility(comp_id)
		self.delete_from_modules(comp_id)
		self.delete_from_compilations(comp_id)
		
	def RemovePackage(self, pck_id):
		self.delete_from_packages(pck_id)
		
	def GetInfoForPackage(self, name, version):
		pck_comps = self.get_pck_info(name, version)
		comps = []
		for pck_comp in pck_comps:
			comps.append(self.get_comp_info(pck_comp[3]))
			
		print ""
		print "-------- PACKAGE", name, " -- FW VERSION", version, " --- INFORMATION -------------------------------"
		print "Package id:", pck_comps[0][4]
		print "Package name:", pck_comps[0][0]
		print "Version:", pck_comps[0][1]
		print "Date:", pck_comps[0][2]
		
		comps_to_print = []
		for com in comps:
			for ind_com in com:
				comps_to_print.append([ind_com[0], ind_com[1], ind_com[4], ind_com[2]])
		print(tabulate.tabulate(comps_to_print, headers = ["Id", "Fw version", "Fw family", "Date"]))
		print ""
		print ""
			
	#===========================================================================
	# def GetLastRelease(self):
	#     ret = None
	#     query = "".join(["SELECT `id` FROM `", constants.DB_TABLES_PREFIX, "compilations` ORDER BY `id` DESC LIMIT 1"])
	#     try:
	#         self.cur.execute(query)
	#         rows = self.cur.fetchall()
	#     except Exception as inst:
	#         print_error("Error database query: " + query + ". xception:" + str(inst))
	#         raise Exception()
	#     else:
	#         if len(rows) > 0:
	#             ret = rows[0][0]  
	#     return ret
	#         
	# def GetPreviousCommit(self, name, compilation_id):
	#     ret = None
	#     query = "".join(["SELECT `commit` FROM `", constants.DB_TABLES_PREFIX, "modules` WHERE `name`='", str(name), "' AND `comp_id`<", str(compilation_id) ," ORDER BY `comp_id` DESC LIMIT 1"])
	#     #print query
	#     try:
	#         self.cur.execute(query)
	#         rows = self.cur.fetchall()
	#     except Exception as inst:
	#         print_error("Error database query: " + query + ". Exception:" + str(inst))
	#         raise Exception()
	#     else:
	#         if len(rows) > 0:
	#             ret = rows[0][0]  
	#     return ret
	#===========================================================================
		


if __name__ == '__main__':
	
	db = Database()
	
	while True:
		print "Menu:"
		print "  1. Get modules info from part-number, fw version and fw_family"
		print "  2. Get versions info from part-number"
		print "  3. Get package info from name, version"
		print "  4. Delete release"
		print "  5. Delete package"
		print "  q. Exit"
		option = raw_input("  Enter option:")
		
		if option == '1':
			part_number = raw_input("  Insert part-number:")
			fw_version = raw_input("  Insert fw-version:")
			fw_family = raw_input("  Insert fw-family:")
		elif option == '2':
			part_number = raw_input("  Insert part-number:")
			db.GetInfoForPartNumber(part_number)
		elif option == '3':
			name = raw_input("  Insert name:")
			version = raw_input("  Insert version:")
			db.GetInfoForPackage(name, version)
		elif option == '4':
			fw_version = raw_input("  Insert fw-version:")
			fw_family = raw_input("  Insert fw-family:")
			if fw_version == "None":
				print "Cannot remove legacy versions"
			else:
				db.RemoveRelease(fw_family, fw_version)
				db.commit()
		elif option == '5':
			pck_id = raw_input("  Insert package id:")
			db.RemovePackage(pck_id)
			db.commit()
		elif option == 'q':
			break
			
