import sqlite3, MySQLdb, time

import defines as constants
import tabulate


DB_HOST = '192.168.77.4'
DB_USER = 'merytronic'
DB_PWD = 'merytronic2012'
OLD_DB_NAME = '402_12_fw_versions'
DB_NAME = '402_12_fw'

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
        self.con = MySQLdb.connect(DB_HOST, DB_USER, DB_PWD, DB_NAME)
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
                                    
        self.get_comp_pn_query = "SELECT * FROM part_number_compatibility pn1 \
                                    INNER JOIN compilations c1 ON pn1.comp_id=c1.id"
        
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
        query = "".join(["INSERT INTO `compilations` (`fw_family_id`, `fw_version`, `date`, `command_line`) VALUES (", str(fw_family_id) , ",'",str(fw_version),"','",str(date),"','",str(command_line),"')"])
        #print query
        self.cur.execute(query)
        return self.cur.lastrowid    
        
    def insert_into_part_number_compatibility(self, comp_id, part_number_id):
        query = "".join(["INSERT INTO `part_number_compatibility` (`comp_id`, `part_number_id`) VALUES (", str(comp_id) , ",",str(part_number_id),")"])
        #print query
        self.cur.execute(query)
        return self.cur.lastrowid
        
    def insert_into_version_compatibility(self, pn_comp_id, min_compatible_pn_comp_id):
        query = "".join(["INSERT INTO `version_compatibility` (`pn_comp_id`, `min_compatible_pn_comp_id`) VALUES (", str(pn_comp_id) , ",",str(min_compatible_pn_comp_id),")"])
        #print query
        self.cur.execute(query)
        return self.cur.lastrowid
        
    def insert_into_modules(self, comp_id, name, commit, tftp_img_included, full_upd_included, incr_upd_included):
        query = "".join(["INSERT INTO `modules` (`comp_id`, `name`, `commit`, `tftp_img_included`, `full_upd_included`, `incr_upd_included`) VALUES (",
                                    str(comp_id), ",'", str(name), "','", str(commit), "',", str(tftp_img_included), ",", str(full_upd_included), ",", str(incr_upd_included), ")"])
        #print query
        self.cur.execute(query)
        return self.cur.lastrowid
        
    def get_fw_family_id(self, fw_family):
        self.cur.execute("SELECT `id` FROM `fw_family` WHERE `name`='" + str(fw_family) + "'")
        return self.cur.fetchone()
        
    def get_part_number_id(self, part_number):
        self.cur.execute("SELECT `id` FROM `part_number` WHERE `name`='" + str(part_number) + "'")
        return self.cur.fetchone()
        
    def get_pn_comps_from_pn_fam_fw(self, part_number_id, fw_family_id, fw_version):
        query = "".join([self.get_comp_pn_query, " WHERE c1.fw_version='", str(fw_version), 
                            "' AND pn1.part_number_id=", str(part_number_id), 
                            " AND c1.fw_family_id=", str(fw_family_id)])
        #print query
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def get_pn_comps_from_fam_fw(self, fw_family_id, fw_version):
        query = "".join([self.get_comp_pn_query, " WHERE c1.fw_version='", str(fw_version), 
                            "' AND c1.fw_family_id=", str(fw_family_id)])
        #print query
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def get_modules_from_comp_id(self, comp_id):
        self.cur.execute("SELECT * FROM `modules` WHERE `comp_id`=" + str(comp_id))
        return self.cur.fetchall()
        
    def get_full_info_from_pn(self, part_number_id):
        query = "".join([self.get_full_info_query, " WHERE pn1.part_number_id=", str(part_number_id)])
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def get_full_info_from_pn_fam_fw(self, part_number_id, fw_family_id, fw_version):
        query = "".join([self.get_full_info_query, " WHERE pn1.part_number_id=", str(part_number_id), " AND c1.fw_version='", str(fw_version), "' AND c1.fw_family_id=", str(fw_family_id)])
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def get_full_info_from_fam_fw(self, fw_family_id, fw_version):
        query = "".join([self.get_full_info_query, " WHERE c1.fw_version='", str(fw_version), "' AND c1.fw_family_id=", str(fw_family_id)])
        self.cur.execute(query)
        return self.cur.fetchall()
        
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
        
    def NewRelease(self, fw_family, fw_version, part_number_list, min_versions_list, command_line = "", legacy_min_version_list = None):
        part_numbers = part_number_list.split(',')
        min_versions_tmp = min_versions_list.split(';')
        min_versions = []
        for min_vers_tmp in min_versions_tmp:
            min_versions.append((min_vers_tmp.split(',')[0], min_vers_tmp.split(',')[1]))
        legacy_min_versions = None
        if legacy_min_version_list != None:
            legacy_min_versions = legacy_min_version_list.split(',')
        
        if fw_family == 'None':
            print "Fw family not allowed for new releases"
            return 1
            
        fw_family_entry = self.get_fw_family_id(fw_family)
        if fw_family_entry == None:
            print "Fw family not allowed"
            return 1
        fw_family_id = fw_family_entry[0]
        
        entries = self.get_pn_comps_from_fam_fw(fw_family_id, fw_version)
        if len(entries) != 0:
            print "Fw version already deployed"
            return 1
            
        for min_vers in min_versions:
            prev_fw_family_entry = self.get_fw_family_id(min_vers[0])
            if prev_fw_family_entry == None:
                print "Prev fw family not allowed"
                return 1
                
            if min_vers[1] != fw_version:
                prev_fw_family_id = prev_fw_family_entry[0]
                comp_entry = self.get_pn_comps_from_fam_fw(prev_fw_family_id, min_vers[1])
                if len(comp_entry) == 0:
                    print "Prev version not deployed"
                    return 1
                    
        if legacy_min_version_list != None and \
            (len(legacy_min_versions) != len(part_numbers)):
            print "Error on legacy versions length"
            return 1
        
        index = 0
        for part_number in part_numbers:
            part_number_entry = self.get_part_number_id(part_number)
            if part_number_entry == None:
                print "Part-number not allowed"
                return 1
            part_number_id = part_number_entry[0]
            
            if legacy_min_version_list != None and legacy_min_versions[index] != 'None':
                entries = self.get_pn_comps_from_pn_fam_fw(part_number_id, self.get_fw_family_id('None')[0], legacy_min_versions[index])
                if len(entries) == 0:
                    print "Previous legacy release not found for pn", part_number
                    return 1
                                
            index += 1
                
                
        comp_id = self.insert_into_compilations(fw_family_id, fw_version, GetTime(), command_line)

        index = 0
        for part_number in part_numbers:
            part_number_id = self.get_part_number_id(part_number)[0]
            
            prev_comp_ids = []
            if legacy_min_version_list != None and legacy_min_versions[index] != 'None':
                prev_comps_info = self.get_pn_comps_from_pn_fam_fw(part_number_id, self.get_fw_family_id('None')[0], legacy_min_versions[index])
                for prev_comp in prev_comps_info:
                    print prev_comp
                    prev_comp_ids.append(prev_comp[0])
            
            for min_vers in min_versions:
                prev_fw_family = min_vers[0]
                min_fw_version = min_vers[1]
                min_fw_family_id = self.get_fw_family_id(prev_fw_family)[0]
                prev_comps_info = self.get_pn_comps_from_pn_fam_fw(part_number_id, min_fw_family_id, min_fw_version)
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
            
    def GetCommitByVersionFamily(self, name, fw_family, version):
        ret = None
        fw_family_id = self.get_fw_family_id(fw_family)[0]
        query = "".join(["SELECT `commit` FROM `modules` WHERE `name`='", str(name), "' AND `comp_id`=(SELECT `id` FROM `compilations` WHERE `fw_version`='", str(version) ,"' AND `fw_family_id`=",fw_family_id,")"])
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
        
    def GetCommitByVersionPartNumber(self, name, part_number, version):
        ret = None
        part_number_id = self.get_part_number_id(part_number)[0]
        fw_family_id = self.get_fw_family_id("None")[0]
        query = "".join(["SELECT `commit` FROM `modules` WHERE `name`='", str(name), 
                         "' AND `comp_id`=(SELECT pn1.id FROM part_number_compatibility pn1 INNER JOIN compilations c1 ON pn1.comp_id=c1.id WHERE pn1.part_number_id=", 
                         str(part_number_id), " AND c1.fw_version='", str(version),"' AND c1.fw_family_id=", str(fw_family_id) ,")"])
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
                    
        
    def GetModulesInfo(self, part_number, fw_version, fw_family):
        part_number_entry = self.get_part_number_id(part_number)
        if part_number_entry == None:
            print "Part-number not allowed"
            return 1
            
        fw_family_entry = self.get_fw_family_id(fw_family)
        if fw_family_entry == None:
            print "Fw family not allowed"
            return 1
            
        part_number_id = part_number_entry[0]
        fw_family_id = fw_family_entry[0]
        
        fw_compilations = self.get_full_info_from_pn_fam_fw(part_number_id, fw_family_id, fw_version)
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
            if fw_compilations[0][6] != fw_version:
                data += "     Version " + fw_compilations[0][6] + ", Fw family " + fw_compilations[0][7] + "\n"
        print data
        modules_to_print = []
        for module in modules:
            modules_to_print.append(module[2:])
        print(tabulate.tabulate(modules_to_print, headers = ["Module", "Commit id", "Tftp img included", "Full img included", "Incr upd included"]))
        print ""
        print ""
        
    def GetInfoForPartNumber(self, part_number):
        part_number_entry = self.get_part_number_id(part_number)
        if part_number_entry == None:
            print "Part-number not allowed"
            return 1
            
        part_number_id = part_number_entry[0]
        fw_compilations = self.get_full_info_from_pn(part_number_id)
        
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
            
    def NewModule(self, compilation_id, name, commit, tftp_img_included):
        query = "".join(["INSERT INTO `modules` (`comp_id`, `name`, `commit`, `tftp_img_included`,`full_upd_included`,`incr_upd_included`) VALUES (",
                         str(compilation_id),",'",str(name),"','",str(commit),"',",str(tftp_img_included),",0,0)"])
        print query
        try:
            self.cur.execute(query)
        except Exception as inst:
            print_error("Error database query: " + query + ". Exception:" + str(inst))
            raise Exception()
            
    def SetFullUpdIncluded(self, compilation_id, name, full_upd_included):
        query = "".join(["UPDATE `modules` SET `full_upd_included`=", str(full_upd_included), " WHERE `comp_id`=", str(compilation_id), " AND `name`='", str(name), "'" ])
        #print query
        try:
            self.cur.execute(query)
        except Exception as inst:
            print_error("Error database query: " + query + ". Exception:" + str(inst))
            raise Exception()
            
    def SetIncrUpdIncluded(self, compilation_id, name, incr_upd_included):
        query = "".join(["UPDATE `modules` SET `incr_upd_included`=", str(incr_upd_included), " WHERE `comp_id`=", str(compilation_id), " AND `name`='", str(name), "'" ])
        #print query
        try:
            self.cur.execute(query)
        except Exception as inst:
            print_error("Error database query: " + query + ". Exception:" + str(inst))
            raise Exception()
            
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
        print "  q. Exit"
        option = raw_input("  Enter option:")
        
        if option == '2':
            part_number = raw_input("  Insert part-number:")
            db.GetInfoForPartNumber(part_number)
        elif option == '1':
            part_number = raw_input("  Insert part-number:")
            fw_version = raw_input("  Insert fw-version:")
            fw_family = raw_input("  Insert fw-family:")
            db.GetModulesInfo(part_number, fw_version, fw_family)
        elif option == '4':
            fw_family = raw_input("  Insert fw_family:")
            fw_version = raw_input("  Insert fw_version:")
            part_number_list = raw_input("  Insert part_number_list:")
            min_versions_list = raw_input("  Insert min_versions_list:")
            legacy_min_version_list = raw_input("  Insert legacy_min_version_list:")
            if legacy_min_version_list == "":
                legacy_min_version_list = None
            #db.new_release(fw_family, fw_version, part_number_list, min_versions_list, "", legacy_min_version_list)
            db.NewRelease('UFD', '1.3.0', '402.12.00,402.12.04', 'UFD,1.3.0', "", '1.1.3,1.2.2')
            db.NewRelease('IBD', '1.2.9', '402.12.00,402.12.07', 'IBD,1.2.9', "", '1.1.3,1.1.3')
            db.NewRelease('UFD', '1.3.1', '402.12.00,402.12.03,402.12.04,402.12.07,402.12.08', 'UFD,1.3.0;IBD,1.2.9', "", '1.1.0,1.1.0,None,None,None')
            db.NewRelease('UFD', '1.3.2', '402.12.00,402.12.03,402.12.04,402.12.07,402.12.08', 'UFD,1.3.0;IBD,1.2.9', "", 'None,None,None,None,None')
        elif option == 'q':
            break
            
