import sqlite3, time

import defines as constants

def GetTime():
	a = time.localtime(time.time())
	return time.strftime("%Y/%m/%d %H:%M:%S",a)


class Database:    
	def __del__(self):
		self.quit()

	def connect(self, part_number, tmout = 15):
		self.con = sqlite3.connect(constants.SRC_DIR[0] + '/project_compiler/database/' + part_number + '.db3', timeout = tmout)
		self.cur = self.con.cursor()

	def quit(self):
		try:
			self.cur.close()
		except:
			pass

		try:
			self.con.close()
		except:
			pass

	def NewRelease(self, fw_version):
		query = "".join(["INSERT INTO `compilations` (`fw_version`, `date`) VALUES ('",str(fw_version),"','",str(GetTime()),"')"])
		
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			raise
		else:
			return self.cur.lastrowid
			
	def NewProject(self, compilation_id, name, commit, version):
		query = "".join(["INSERT INTO `modules` (`comp_id`, `name`, `commit`, `version`) VALUES (",str(compilation_id),",'",str(name),"','",str(commit),"','",str(version),"')"])
		
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			raise
			
	def GetLastRelease(self):
		ret = None
		query = "".join(["SELECT `id` FROM `compilations` ORDER BY `id` DESC LIMIT 1,0"])
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			raise
		else:
			if len(rows) > 0:
				ret = rows[0][0]  
		return ret
			
	def GetPreviousCommit(self, name, compilation_id):
		ret = None
		query = "".join(["SELECT `commit` FROM `modules` WHERE `name`=='", str(name), "' AND `comp_id`<", str(comp_id) ," ORDER BY `comp_id` DESC LIMIT 1,0"])
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
		except Exception as inst:
			raise
		else:
			if len(rows) > 0:
				ret = rows[0][0]  
		return ret
			
                
                                


if __name__ == '__main__':
	db = Database()
	db.connect()
	print db.GetNextFw('Iberdrola', 1, 8)
	print db.GetNextFw('Iberdrola', 1, 9)
	print db.GetNextFw('Iberdrola', 2, 0)
