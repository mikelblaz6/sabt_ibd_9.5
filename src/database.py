import sqlite3, time

import defines as constants

from utils import print_error

def GetTime():
	a = time.localtime(time.time())
	return time.strftime("%Y/%m/%d %H:%M:%S",a)


class Database:    
	def __del__(self):
		self.quit()

	def __init__(self, part_number, tmout = 15):
		self.con = sqlite3.connect(database = constants.DATABASE_PATH + part_number + '.db3', timeout = tmout)
		self.cur = self.con.cursor()
		self.cur.execute("begin")
		
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

	def NewRelease(self, fw_version):
		query = "".join(["INSERT INTO `compilations` (`fw_version`, `date`) VALUES ('",str(fw_version),"','",str(GetTime()),"')"])
		print query
		
		try:
			self.cur.execute(query)
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
		else:
			return self.cur.lastrowid
			
	def NewProject(self, compilation_id, name, commit, version, tftp_img_included):
		query = "".join(["INSERT INTO `modules` (`comp_id`, `name`, `commit`, `version`,`tftp_img_included`,`full_upd_included`,`incr_upd_included`) VALUES (",str(compilation_id),",'",str(name),"','",str(commit),"','",str(version),"',",str(tftp_img_included),",0,0)"])
		print query
		try:
			self.cur.execute(query)
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
			
	def SetFullUpdIncluded(self, compilation_id, name, version, full_upd_included):
		query = "".join(["UPDATE `modules` SET `full_upd_included`=", str(full_upd_included), " WHERE `comp_id`=", str(compilation_id), " AND `name`='", str(name), "' AND `version`='",str(version),"'" ])
		#print query
		try:
			self.cur.execute(query)
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
			
	def SetIncrUpdIncluded(self, compilation_id, name, version, incr_upd_included):
		query = "".join(["UPDATE `modules` SET `incr_upd_included`=", str(incr_upd_included), " WHERE `comp_id`=", str(compilation_id), " AND `name`='", str(name), "' AND `version`='",str(version),"'" ])
		#print query
		try:
			self.cur.execute(query)
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
			
	def GetLastRelease(self):
		ret = None
		query = "".join(["SELECT `id` FROM `compilations` ORDER BY `id` DESC LIMIT 1"])
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			print_error("Error database query: " + query + ". xception:" + str(inst))
			raise Exception()
		else:
			if len(rows) > 0:
				ret = rows[0][0]  
		return ret
			
	def GetPreviousCommit(self, name, compilation_id):
		ret = None
		query = "".join(["SELECT `commit` FROM `modules` WHERE `name`='", str(name), "' AND `comp_id`<", str(compilation_id) ," ORDER BY `comp_id` DESC LIMIT 1"])
		#print query
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
		else:
			if len(rows) > 0:
				ret = rows[0][0]  
		return ret
		
	def GetCommitByVersion(self, name, version):
		ret = None
		query = "".join(["SELECT `commit` FROM `modules` WHERE `name`='", str(name), "' AND `comp_id`=(SELECT `id` FROM `compilations` WHERE `fw_version`='", str(version) ,"')"])
		print query
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			print_error("Error database query: " + query + ". Exception:" + str(inst))
			raise Exception()
		else:
			if len(rows) > 0:
				ret = rows[0][0]  
		return ret


