
FW_IBD_DEFINES =  {
                    '__VTN__':                      ['__VTN__', False],                 #Funcionalidad VTN visible
                    '__FUS_1_ALG__':                ['__FUS_1_ALG__', False],           #Algoritmo UFD de fusible fundido
                    '__UFD_WS_ID__':                ['__UFD_WS_ID__', False],           #Identificador de WS de UFD'
                    '__VOLT_AL_METERS__':           ['__VOLT_AL_METERS__', False],      #Alarmas de tension en tarjetas
                    '__EXT_PROFILES__':             ['__EXT_PROFILES__', False],        #Perfiles extendidos 
                    '__IP_IS_CFG__':                ['__IP_IS_CFG__', False],           #Relacion Ip/Is configurable
                    '__INOM_EXT_RANGE__':           ['__INOM_EXT_RANGE__', False],      #Rango extendido para Inom[0-5000]
                    '__STRONG_PWD__':               ['__STRONG_PWD__', False],          #Contrasenas reforzadas
                    '__IFT_CFG__':                  ['__IFT_CFG__', False],             #Ratio Ift configurable
                    '__FIREWALL__':                 ['__FIREWALL__', False],            #Firewall
                    '__SYNC_MET_ALWAYS__':          ['__SYNC_MET_ALWAYS__', False],     #Sincronizar hora de tarjetas aunque no haya NTP
                    '__C50__':                      ['__C50__', False],
                    '__C51__':                      ['__C51__', False],
                    '__C62__':                      ['__C62__', False],
                    '__G50__':                      ['__G50__', False],
                    '__G51__':                      ['__G51__', False],
                    '__G52__':                      ['__G52__', False],
                    '__G53__':                      ['__G53__', False],
                    '__G54__':                      ['__G54__', False],
                    '__G55__':                      ['__G55__', False],
                    '__G56__':                      ['__G56__', False],
                    '__G57__':                      ['__G57__', False],
                    '__G58__':                      ['__G58__', False],
                    '__G59__':                      ['__G59__', False],
                    '__G61__':                      ['__G61__', False],
                    '__G62__':                      ['__G62__', False],
                    '__G63__':                      ['__G63__', False],
                    '__G64__':                      ['__G64__', False],
                    '__G65__':                      ['__G65__', False],
                    '__SM7__':                      ['__SM7__', False],
                    '__M01__':                      ['__M01__', False],
                    '__M02__':                      ['__M02__', False],
                    '__S69_SYNC__':                 ['__S69_SYNC__', False],            #S69 se puede pedir de forma sincrona
                    '__S72_SYNC__':                 ['__S72_SYNC__', False],            #S72 se puede pedir de forma sincrona
                    '__FW_FAM_EN__':                ['__FW_FAM_EN__', False],           #Habilitado pedir y mostrar la familia de fw de las tarjetas y RTU
                    '__WEB_LANG_SEL__':             ['__WEB_LANG_SEL__', False],        #Selector de idioma en web
                    '__LDAP_DN_CFG__':              ['__LDAP_DN_CFG__', False],         #LDAP Domain Name configurable en web
                    '__NETWORK_SEC__':              ['__NETWORK_SEC__', False],         #Habilitar protocolos seguros y control de conexiones
                    '__PROFILES_DIS__':             ['__PROFILES_DIS__', False],        #Los perfiles se pueden deshabilitar con per=0 en Web
                    '__WEB_HEADER_LOGIN__':         ['__WEB_HEADER_LOGIN__', False],    #Mostrar la cabecera de la web en las pantallas de login
                    '__FW_HASH_CHECK__':            ['__FW_HASH_CHECK__', False],         #Habilitar el chequeo del hash de los fw en la web
                    '__USER_TIME_SET__':            ['__USER_TIME_SET__', False],         #El usuario puede poner en hora el equipo
                    '__WEB_MET_EVENTS__':           ['__WEB_MET_EVENTS__', False],         #Mostar en la web las pestanas de eventos de tarjetas
                    '__SHOW_PQ_VERSION__':          ['__SHOW_PQ_VERSION__', False],         #Mostar en la web versiobn de fw de PQ
                    '__SKIP_ALARM_REG_EVENTS__':    ['__SKIP_ALARM_REG_EVENTS__', False],   #NO utiliza el registro de alarmas de las tarjetas para decidir que subgupos de eventos pedir
                    '__FT_ALARM_SYNOP__':          	['__FT_ALARM_SYNOP__', False],			#Mostrar la alarma de fugas a tierra en e sinoptico de la web
                    '__MODBUS_MODULE__':			['__MODBUS_MODULE__', False],		#Modulo modbus habilitado
                    '__INSTANTS_WITH_ALARMS__':		['__INSTANTS_WITH_ALARMS__', False],	#Pedir a tarjetas valores instantaneos con alarmas
                    '__DISPLAY__':					['__DISPLAY__', False],				#Display hw y modulo sw asociado
                    '__MY01__':						['__MY01__', False],				#MY01 report (CSV Malasia)
                    '__DNS__':                      ['__DNS__', False],                #Habilita configuracion de DNS y posibilidad de URLs para los servidores externos
                    '__NETWORK_SEC_XML__':          ['__NETWORK_SEC_XML__', False],         #Habilitar protocolos seguros y control de conexiones mediante XML y WS
                    '__PWD_CHANGE_WEB__':           ['__PWD_CHANGE_WEB__', False],  #LAs password de acceso RTU y tarjetas se pueden cambiar desde la web
                    '__LDAP_DN_CFG_XML__':          ['__LDAP_DN_CFG_XML__', False],         #LDAP Domain Name configurable en XML/WS
                    '__MRT_WS_ID__':                ['__MRT_WS_ID__', False],           #Identificador de WS de UFD'
                    }

FW_UFD_DEFINES =  {
                    '__VTN__':                      ['__VTN__', True],                 #Funcionalidad VTN visible
                    '__FUS_1_ALG__':                ['__FUS_1_ALG__', True],  # Algoritmo UFD de fusible fundido
                    '__UFD_WS_ID__':                ['__UFD_WS_ID__', True],           #Identificador de WS de UFD'
                    '__VOLT_AL_METERS__':           ['__VOLT_AL_METERS__', True],      #Alarmas de tension en tarjetas
                    '__EXT_PROFILES__':             ['__EXT_PROFILES__', True],        #Perfiles extendidos 
                    '__IP_IS_CFG__':                ['__IP_IS_CFG__', True],           #Relacion Ip/Is configurable
                    '__INOM_EXT_RANGE__':           ['__INOM_EXT_RANGE__', True],      #Rango extendido para Inom[0-5000]
                    '__STRONG_PWD__':               ['__STRONG_PWD__', True],          #Contrasenas reforzadas
                    '__IFT_CFG__':                  ['__IFT_CFG__', True],             #Ratio Ift configurable
                    '__FIREWALL__':                 ['__FIREWALL__', True],            #Firewall
                    '__SYNC_MET_ALWAYS__':          ['__SYNC_MET_ALWAYS__', True],       #Sincronizar hora de tarjetas aunque no haya NTP
                    '__C50__':                      ['__C50__', True],
                    '__C51__':                      ['__C51__', True],
                    '__C62__':                      ['__C62__', True],
                    '__G50__':                      ['__G50__', True],
                    '__G51__':                      ['__G51__', True],
                    '__G52__':                      ['__G52__', True],
                    '__G53__':                      ['__G53__', True],
                    '__G54__':                      ['__G54__', True],
                    '__G55__':                      ['__G55__', True],
                    '__G56__':                      ['__G56__', True],
                    '__G57__':                      ['__G57__', True],
                    '__G58__':                      ['__G58__', True],
                    '__G59__':                      ['__G59__', True],
                    '__G61__':                      ['__G61__', True],
                    '__G62__':                      ['__G62__', True],
                    '__G63__':                      ['__G63__', True],
                    '__G64__':                      ['__G64__', True],
                    '__G65__':                      ['__G65__', True],
                    '__SM7__':                      ['__SM7__', True],
                    '__M01__':                      ['__M01__', True],
                    '__M02__':                      ['__M02__', True],
                    '__S69_SYNC__':                 ['__S69_SYNC__', True],            #S69 se puede pedir de forma sincrona
                    '__S72_SYNC__':                 ['__S72_SYNC__', True],            #S72 se puede pedir de forma sincrona
                    '__FW_FAM_EN__':                ['__FW_FAM_EN__', True],           #Habilitado pedir y mostrar la familia de fw de las tarjetas y RTU
                    '__WEB_LANG_SEL__':             ['__WEB_LANG_SEL__', True],        #Selector de idioma en web
                    '__LDAP_DN_CFG__':              ['__LDAP_DN_CFG__', True],         #LDAP Domain Name configurable
                    '__NETWORK_SEC__':              ['__NETWORK_SEC__', True],         #Habilitar protocolos seguros y control de conexiones
                    '__PROFILES_DIS__':             ['__PROFILES_DIS__', True],        #Los perfiles se pueden deshabilitar con per=0 en Web
                    '__WEB_HEADER_LOGIN__':         ['__WEB_HEADER_LOGIN__', True],    #Mostrar la cabecera de la web en las pantallas de login
                    '__FW_HASH_CHECK__':            ['__FW_HASH_CHECK__', True],         #Habilitar el chequeo del hash de los fw en la web
                    '__USER_TIME_SET__':            ['__USER_TIME_SET__', True],         #El usuario puede poner en hora el equipo
                    '__WEB_MET_EVENTS__':           ['__WEB_MET_EVENTS__', True],         #Mostar en la web las pestanas de eventos de tarjetas
                    '__SHOW_PQ_VERSION__':          ['__SHOW_PQ_VERSION__', True],         #Mostar en la web versiobn de fw de PQ
                    '__SKIP_ALARM_REG_EVENTS__':    ['__SKIP_ALARM_REG_EVENTS__', True], 
                    '__FT_ALARM_SYNOP__':          	['__FT_ALARM_SYNOP__', True],			#Mostrar la alarma de fugas a tierra en e sinoptico de la web
                    '__MODBUS_MODULE__':			['__MODBUS_MODULE__', False],		#Modulo modbus habilitado
                    '__INSTANTS_WITH_ALARMS__':		['__INSTANTS_WITH_ALARMS__', False],	#Pedir a tarjetas valores instantaneos con alarmas
                    '__DISPLAY__':					['__DISPLAY__', False],				#Display hw y modulo sw asociado
                    '__MY01__':						['__MY01__', False],				#MY01 report (CSV Malasia)
                    '__DNS__':                      ['__DNS__', False],                #Habilita configuracion de DNS y posibilidad de URLs para los servidores externos
                    '__NETWORK_SEC_XML__':          ['__NETWORK_SEC_XML__', False],         #Habilitar protocolos seguros y control de conexiones mediante XML y WS
                    '__PWD_CHANGE_WEB__':           ['__PWD_CHANGE_WEB__', False],  #LAs password de acceso RTU y tarjetas se pueden cambiar desde la web
                    '__LDAP_DN_CFG_XML__':          ['__LDAP_DN_CFG_XML__', False],         #LDAP Domain Name configurable en XML/WS
                    '__MRT_WS_ID__':                ['__MRT_WS_ID__', False],           #Identificador de WS de UFD'
                   }
                   
FW_MRT_DEFINES =  {
                    '__VTN__':                      ['__VTN__', True],                 #Funcionalidad VTN visible
                    '__FUS_1_ALG__':                ['__FUS_1_ALG__', False],  # Algoritmo UFD de fusible fundido
                    '__UFD_WS_ID__':                ['__UFD_WS_ID__', False],           #Identificador de WS de UFD'
                    '__VOLT_AL_METERS__':           ['__VOLT_AL_METERS__', True],      #Alarmas de tension en tarjetas
                    '__EXT_PROFILES__':             ['__EXT_PROFILES__', True],        #Perfiles extendidos 
                    '__IP_IS_CFG__':                ['__IP_IS_CFG__', True],           #Relacion Ip/Is configurable
                    '__INOM_EXT_RANGE__':           ['__INOM_EXT_RANGE__', True],      #Rango extendido para Inom[0-5000]
                    '__STRONG_PWD__':               ['__STRONG_PWD__', True],          #Contrasenas reforzadas
                    '__IFT_CFG__':                  ['__IFT_CFG__', True],             #Ratio Ift configurable
                    '__FIREWALL__':                 ['__FIREWALL__', True],            #Firewall
                    '__SYNC_MET_ALWAYS__':          ['__SYNC_MET_ALWAYS__', True],       #Sincronizar hora de tarjetas aunque no haya NTP
                    '__C50__':                      ['__C50__', True],
                    '__C51__':                      ['__C51__', True],
                    '__C62__':                      ['__C62__', True],
                    '__G50__':                      ['__G50__', True],
                    '__G51__':                      ['__G51__', True],
                    '__G52__':                      ['__G52__', True],
                    '__G53__':                      ['__G53__', True],
                    '__G54__':                      ['__G54__', True],
                    '__G55__':                      ['__G55__', True],
                    '__G56__':                      ['__G56__', True],
                    '__G57__':                      ['__G57__', True],
                    '__G58__':                      ['__G58__', True],
                    '__G59__':                      ['__G59__', True],
                    '__G61__':                      ['__G61__', True],
                    '__G62__':                      ['__G62__', True],
                    '__G63__':                      ['__G63__', True],
                    '__G64__':                      ['__G64__', True],
                    '__G65__':                      ['__G65__', True],
                    '__SM7__':                      ['__SM7__', True],
                    '__M01__':                      ['__M01__', True],
                    '__M02__':                      ['__M02__', True],
                    '__S69_SYNC__':                 ['__S69_SYNC__', True],            #S69 se puede pedir de forma sincrona
                    '__S72_SYNC__':                 ['__S72_SYNC__', True],            #S72 se puede pedir de forma sincrona
                    '__FW_FAM_EN__':                ['__FW_FAM_EN__', True],           #Habilitado pedir y mostrar la familia de fw de las tarjetas y RTU
                    '__WEB_LANG_SEL__':             ['__WEB_LANG_SEL__', True],        #Selector de idioma en web
                    '__LDAP_DN_CFG__':              ['__LDAP_DN_CFG__', True],         #LDAP Domain Name configurable
                    '__NETWORK_SEC__':              ['__NETWORK_SEC__', True],         #Habilitar protocolos seguros y control de conexiones
                    '__PROFILES_DIS__':             ['__PROFILES_DIS__', True],        #Los perfiles se pueden deshabilitar con per=0 en Web
                    '__WEB_HEADER_LOGIN__':         ['__WEB_HEADER_LOGIN__', True],    #Mostrar la cabecera de la web en las pantallas de login
                    '__FW_HASH_CHECK__':            ['__FW_HASH_CHECK__', True],         #Habilitar el chequeo del hash de los fw en la web
                    '__USER_TIME_SET__':            ['__USER_TIME_SET__', True],         #El usuario puede poner en hora el equipo
                    '__WEB_MET_EVENTS__':           ['__WEB_MET_EVENTS__', True],         #Mostar en la web las pestanas de eventos de tarjetas
                    '__SHOW_PQ_VERSION__':          ['__SHOW_PQ_VERSION__', True],         #Mostar en la web versiobn de fw de PQ
                    '__SKIP_ALARM_REG_EVENTS__':    ['__SKIP_ALARM_REG_EVENTS__', True], 
                    '__FT_ALARM_SYNOP__':          	['__FT_ALARM_SYNOP__', True],			#Mostrar la alarma de fugas a tierra en e sinoptico de la web
                    '__MODBUS_MODULE__':			['__MODBUS_MODULE__', True],		#Modulo modbus habilitado
                    '__INSTANTS_WITH_ALARMS__':		['__INSTANTS_WITH_ALARMS__', True],	#Pedir a tarjetas valores instantaneos con alarmas
                    '__DISPLAY__':					['__DISPLAY__', False],				#Display hw y modulo sw asociado
                    '__MY01__':						['__MY01__', False],				#MY01 report (CSV Malasia)
                    '__DNS__':                      ['__DNS__', True],                #Habilita configuracion de DNS y posibilidad de URLs para los servidores externos
                    '__NETWORK_SEC_XML__':          ['__NETWORK_SEC_XML__', True],         #Habilitar protocolos seguros y control de conexiones mediante XML y WS
                    '__PWD_CHANGE_WEB__':           ['__PWD_CHANGE_WEB__', True],  #LAs password de acceso RTU y tarjetas se pueden cambiar desde la web
                    '__LDAP_DN_CFG_XML__':          ['__LDAP_DN_CFG_XML__', True],         #LDAP Domain Name configurable en XML/WS
                    '__MRT_WS_ID__':                ['__MRT_WS_ID__', True],           #Identificador de WS de UFD
                   }
                   
FW_MLY_DEFINES =  {
                    '__VTN__':                      ['__VTN__', False],                 #Funcionalidad VTN visible
                    '__FUS_1_ALG__':                ['__FUS_1_ALG__', False],  # Algoritmo UFD de fusible fundido
                    '__UFD_WS_ID__':                ['__UFD_WS_ID__', False],           #Identificador de WS de UFD'
                    '__VOLT_AL_METERS__':           ['__VOLT_AL_METERS__', True],      #Alarmas de tension en tarjetas
                    '__EXT_PROFILES__':             ['__EXT_PROFILES__', True],        #Perfiles extendidos 
                    '__IP_IS_CFG__':                ['__IP_IS_CFG__', True],           #Relacion Ip/Is configurable
                    '__INOM_EXT_RANGE__':           ['__INOM_EXT_RANGE__', True],      #Rango extendido para Inom[0-5000]
                    '__STRONG_PWD__':               ['__STRONG_PWD__', True],          #Contrasenas reforzadas
                    '__IFT_CFG__':                  ['__IFT_CFG__', True],             #Ratio Ift configurable
                    '__FIREWALL__':                 ['__FIREWALL__', True],            #Firewall
                    '__SYNC_MET_ALWAYS__':          ['__SYNC_MET_ALWAYS__', True],       #Sincronizar hora de tarjetas aunque no haya NTP
                    '__C50__':                      ['__C50__', True],
                    '__C51__':                      ['__C51__', False],
                    '__C62__':                      ['__C62__', True],
                    '__G50__':                      ['__G50__', True],
                    '__G51__':                      ['__G51__', False],
                    '__G52__':                      ['__G52__', False],
                    '__G53__':                      ['__G53__', False],
                    '__G54__':                      ['__G54__', False],
                    '__G55__':                      ['__G55__', True],
                    '__G56__':                      ['__G56__', True],
                    '__G57__':                      ['__G57__', True],
                    '__G58__':                      ['__G58__', True],
                    '__G59__':                      ['__G59__', True],
                    '__G61__':                      ['__G61__', True],
                    '__G62__':                      ['__G62__', True],
                    '__G63__':                      ['__G63__', True],
                    '__G64__':                      ['__G64__', True],
                    '__G65__':                      ['__G65__', True],
                    '__SM7__':                      ['__SM7__', True],
                    '__M01__':                      ['__M01__', True],
                    '__M02__':                      ['__M02__', True],
                    '__S69_SYNC__':                 ['__S69_SYNC__', True],            #S69 se puede pedir de forma sincrona
                    '__S72_SYNC__':                 ['__S72_SYNC__', True],            #S72 se puede pedir de forma sincrona
                    '__FW_FAM_EN__':                ['__FW_FAM_EN__', True],           #Habilitado pedir y mostrar la familia de fw de las tarjetas y RTU
                    '__WEB_LANG_SEL__':             ['__WEB_LANG_SEL__', True],        #Selector de idioma en web
                    '__LDAP_DN_CFG__':              ['__LDAP_DN_CFG__', True],         #LDAP Domain Name configurable
                    '__NETWORK_SEC__':              ['__NETWORK_SEC__', True],         #Habilitar protocolos seguros y control de conexiones
                    '__PROFILES_DIS__':             ['__PROFILES_DIS__', True],        #Los perfiles se pueden deshabilitar con per=0 en Web
                    '__WEB_HEADER_LOGIN__':         ['__WEB_HEADER_LOGIN__', True],    #Mostrar la cabecera de la web en las pantallas de login
                    '__FW_HASH_CHECK__':            ['__FW_HASH_CHECK__', True],         #Habilitar el chequeo del hash de los fw en la web
                    '__USER_TIME_SET__':            ['__USER_TIME_SET__', True],         #El usuario puede poner en hora el equipo
                    '__WEB_MET_EVENTS__':           ['__WEB_MET_EVENTS__', True],         #Mostar en la web las pestanas de eventos de tarjetas
                    '__SHOW_PQ_VERSION__':          ['__SHOW_PQ_VERSION__', True],         #Mostar en la web versiobn de fw de PQ
                    '__SKIP_ALARM_REG_EVENTS__':    ['__SKIP_ALARM_REG_EVENTS__', True], 
                    '__FT_ALARM_SYNOP__':          	['__FT_ALARM_SYNOP__', True],			#Mostrar la alarma de fugas a tierra en e sinoptico de la web
                    '__MODBUS_MODULE__':			['__MODBUS_MODULE__', True],		#Modulo modbus habilitado
                    '__INSTANTS_WITH_ALARMS__':		['__INSTANTS_WITH_ALARMS__', True],	#Pedir a tarjetas valores instantaneos con alarmas
                    '__DISPLAY__':					['__DISPLAY__', True],				#Display hw y modulo sw asociado
                    '__MY01__':						['__MY01__', True],				#MY01 report (CSV Malasia)
                    '__DNS__':                      ['__DNS__', True],                #Habilita configuracion de DNS y posibilidad de URLs para los servidores externos
                    '__NETWORK_SEC_XML__':          ['__NETWORK_SEC_XML__', True],         #Habilitar protocolos seguros y control de conexiones mediante XML y WS
                    '__PWD_CHANGE_WEB__':           ['__PWD_CHANGE_WEB__', True],  #LAs password de acceso RTU y tarjetas se pueden cambiar desde la web
                    '__LDAP_DN_CFG_XML__':          ['__LDAP_DN_CFG_XML__', True],         #LDAP Domain Name configurable en XML/WS
                    '__MRT_WS_ID__':                ['__MRT_WS_ID__', True],           #Identificador de WS de UFD
                   }

DEPENDENCIES =  {
                    '__VTN__':                      ['__C51__', '__G51__'],               
                    '__FUS_1_ALG__':                ['__G50__', '__C50__'],                 
                    '__VOLT_AL_METERS__':           ['__G50__', '__C50__'],     
                    '__EXT_PROFILES__':             ['__G50__', '__C50__'],            
                    '__IFT_CFG__':                  ['__G62__', '__C62__'],           
                    '__FIREWALL__':                 ['__G62__', '__C62__'],             
                    '__C50__':                      ['__VOLT_AL_METERS__', '__EXT_PROFILES__'],
                    '__G50__':                      ['__VOLT_AL_METERS__', '__EXT_PROFILES__'],
                    '__C62__':                      ['__IFT_CFG__', '__FIREWALL__'],
                    '__G62__':                      ['__IFT_CFG__', '__FIREWALL__'],
                    '__C51__':                      ['__VTN__',],
                    '__G51__':                      ['__VTN__',],
                    '__G52__':                      ['__VTN__',],
                    '__G53__':                      ['__VTN__',],
                    '__G54__':                      ['__VTN__',],
                    '__G56__':                      ['__EXT_PROFILES__',],
                    '__G57__':                      ['__EXT_PROFILES__',],
                    '__G58__':                      ['__EXT_PROFILES__',],
                    '__G59__':                      ['__EXT_PROFILES__',],
                    '__G63__':                      ['__EXT_PROFILES__',],
                    '__G64__':                      ['__EXT_PROFILES__',],
                    '__SM7__':                      ['__EXT_PROFILES__',],
                    '__MY01__':                     ['__EXT_PROFILES__',],
                   }


def get_cpp_defines(fw_family):
    if fw_family == 'IBD':
        defines = FW_IBD_DEFINES
    elif fw_family == 'UFD':
        defines = FW_UFD_DEFINES
    elif fw_family == 'MRT':
        defines = FW_MRT_DEFINES
    elif fw_family == 'MLY':
        defines = FW_MLY_DEFINES
    else:
        return {}
        
    for dep_key, dep_vals in DEPENDENCIES.iteritems():
        if defines[dep_key][1] == True:
            for dep_val in dep_vals:
                defines[dep_val][1] = True
    
    return defines


if __name__ == '__main__':
    print get_cpp_defines('UFD')

