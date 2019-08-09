#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
########################### // STL_ascii class // #############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class STL_ascii:

    def __init__(self, src_path):
        self.src_path = src_path
        
        
    def _ASCII_STL_as_list(self):
        '''
        Loads the ASCII-STL file into a list.
        '''
    
        # get encoding of ASCII-STL file
        encoding = File(self.src_path).get_encoding()
        if encoding == 'error':
            Error.error_report(err_code=4)
        # loop over all ascii lines of the STL-file
        try:
            LIST_OF_ASCII_LINES = []
            with open(self.src_path, 'r', encoding=encoding) as input:
                for line in input.readlines():
                    # convert the line with it's items to a list 
                    # example: line = 'bla bli blub\n' --> 
                    # line as list = ['bla', 'bli', 'blub']
                    LIST_OF_ASCII_LINES.append(Line(line).get_line_items())
                    
        except UnicodeDecodeError:
            Error.error_report(err_code=4)
                   

        return LIST_OF_ASCII_LINES
                
   
   
    def get_corner_points(self):
        '''
        Returns the corner vertices of the AER-domain.
        The indexing sheme is like followed.
        
 

        AER-Domain box
             ________
            /       /|       z
           /       / |       |  y
          /       /  |       | /
         /_______/   /       |/___x
         |       |  /
         |       | /
         |_______|/
        
        
            |             C_i______D_i  with i in [0,1] and i = 0 if x_y plaine
            |               |      |    is bottom plaine.
            |               |  y   |    and i = 1 if x_y plain is top plain
            |_______ \      |  |_x |
                     /      |      |
                            |      |
                            |______|       
                          A_i      B_i
        
        
        '''
    
       
        
        CORNER_VERTs = []
        
        i = 0
        for ascii_line in self._ASCII_STL_as_list():
            
            if ascii_line[0] == 'vertex':
                vert = [float(item) for item in ascii_line[1:]]
                if i == 0:
                    CORNER_VERTs.append(vert)
                else:
                    if vert not in CORNER_VERTs:
                        CORNER_VERTs.append(vert)
                    
                    if len(CORNER_VERTs) == 8:
                        break
                
            i += 1    
               

                
                
        X = []
        Y = []
        Z = []
        for vert in CORNER_VERTs:
           X.append(vert[0])
           Y.append(vert[1])
           Z.append(vert[2])
            
        x_min = min(X)
        x_max = max(X)
        
        y_min = min(Y)
        y_max = max(Y)
        
        z_min = min(Z)
        z_max = max(Z)
        
            
        for vert in CORNER_VERTs:
            if vert[0] == x_min and vert[1] == y_min and vert[2] == z_min:
                A_0 = vert
                
            if vert[0] == x_max and vert[1] == y_min and vert[2] == z_min:
                B_0 = vert
                
            if vert[0] == x_min and vert[1] == y_max and vert[2] == z_min:
                C_0 = vert
                
            if vert[0] == x_max and vert[1] == y_max and vert[2] == z_min:
                D_0 = vert

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
            if vert[0] == x_min and vert[1] == y_min and vert[2] == z_max:
                A_1 = vert
                
            if vert[0] == x_max and vert[1] == y_min and vert[2] == z_max:
                B_1 = vert
                
            if vert[0] == x_min and vert[1] == y_max and vert[2] == z_max:
                C_1 = vert
                
            if vert[0] == x_max and vert[1] == y_max and vert[2] == z_max:
                D_1 = vert 
            
            
        return (A_0, B_0, C_0 , D_0, A_1, B_1 , C_1 , D_1)
            
            
            
            
    def get_corner_point_key_to_index_map(self):
        corner_vert_map = {'A_0':0, 
                           'B_0':1,
                           'C_0':2,
                           'D_0':3,
                           'A_1':4,
                           'B_1':5,
                           'C_1':6,
                           'D_1':7
        }
            
        
        return corner_vert_map
        
        
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // config class // ##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       

class Config:

    def __init__(self, src_path=None):
        self.src_path = src_path
        
        
        
    def get_config_data(self):      
        def conf_string_tuple(strng_tpl):
            for waste_char in [' ', '(', ')']:
                strng_tpl = strng_tpl.strip(waste_char)

            _tpl = [float(item.strip(' ')) for item in strng_tpl.split(',')]
                    
            return _tpl
            

    
 
        # maps the parameter names of the cofig file to an index for indexing
        # a list which have include all parametervalues
        main_map = {'NUMBER_I':0,
                    'NUMBER_J':1,
                    'NUMBER_K':2,
                    'STL_PATH':3,
                    'CORNER_POINT_COORD':4        
        }
 
 
 
        # maps the corner point names to an index of the corresponded 
        # sublist included in the parameter value list
        corner_point_map  = {'A_0':0,
                             'B_0':1,
                             'C_0':2,
                             'D_0':3,
                             'A_1':4,
                             'B_1':5,
                             'C_1':6,
                             'D_1':7        
        }
        
        
        # paramter value list
        PARAMs = ['' for i in range(4)] 
        PARAMs.append([key for key in corner_point_map])
        

        encoding  = File(self.src_path).get_encoding()
        if encoding == 'error':
            Error.error_report(err_code=5)

        with open(self.src_path, 'r', encoding=encoding) as input:
            get_corner_point_flag = 'standby'
            for line in input.readlines():
                if line.startswith('//') or line == '\n':
                    continue
                else:
                    for key in main_map:
                        if key in line and key!= 'CORNER_POINT_COORD':
                            line = line.strip('\n').split('=')
                            line = [item.strip(' ') for item in line]
                            
                            # to prevent a runtime error if the item is not
                            # a number 
                            try:
                                PARAMs[main_map[key]] = int(line[-1])
                            except:
                                if key not in [[key for key in main_map][:2]]:
                                    PARAMs[main_map[key]] = line[-1]
                                    
                            

                            
                        if key in line and key == 'CORNER_POINT_COORD':
                            get_corner_point_flag = 'go'
                            
                        
                if get_corner_point_flag == 'go':
                    line = line.strip('\n').split('=')
                    line = [item.strip(' ') for item in line]

                    for key in corner_point_map:
                        if key in line:
                            # PARAMS[-1][corner_point__map[key]] = 
                            
                            strng_tpl = line[-1]

                            tpl_as_float_list = conf_string_tuple(strng_tpl)

                            PARAMs[-1][corner_point_map[key]] =               \
                            tpl_as_float_list
 

 
        ### Error report                                        

        # No valid entrys corresponding to the domain dimensioning                     
        if (PARAMs[3] == '' or PARAMs[3] == 'NULL') and PARAMs[-1][0] == 'A_0':
            Error.error_report(err_code=0)
            
        elif (PARAMs[3] != '' and PARAMs[3] != 'NULL') and PARAMs[-1][0] != 'A_0':
            Error.error_report(err_code=1)
        elif '' in PARAMs[:3]:
            Error.error_report(err_code=2)

        else:
            print('\n')
            print(''.join(['~' for i in range(80)]))
            print('')
            print('... the entrys of the configuration file seems to be valid.')
            print('')
            print(''.join(['~' for i in range(80)]))
            print('')
            
        return PARAMs    
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################## // File class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class File:

    def __init__(self, src_path=None):
        self.src_path = src_path


    def get_encoding(self):

        '''
        returns the ASCII encoding of File instance.
        '''


        ENCODINGs = ['utf8', 'ISO-8859-1', 'latin-1']
        _encoding = 42
        
        i = 0
        while True:
            if i == len(ENCODINGs):
                return 'error'
                break
            try:
                with open(self.src_path, 'r', encoding=ENCODINGs[i]) as input:
                    _encoding = ENCODINGs[i]
                    pass
       
            except UnicodeDecodeError:
                continue       

            else:
                _encoding = ENCODINGs[i]
                break
            i += 1

        return _encoding  
        
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################## // Line class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  

class Line:

    def __init__(self, line=None):
        self.line  = line

       
    def get_line_items(self,sep=None):

        '''
        returns the line as a list object with well formated items
        It means that a by formatstrings induced item name like
        for instance "  itemname " gets renamed to "item name".
        Note the blanks in "  item name ".
        '''

        if sep == None:
            line = self.line.strip('\n').split(' ')
        else:
            line = self.line.strip('\n').split(sep)

        
        ### remove blanks at beginning or end of item
        line_new = []

        for item in line:
            if item != '':
                line_new.append(item.strip(' '))

        del line

       
        return line_new       
        
        
class Error:
    '''
    
    '''

    def error_report(err_code):
        
        if err_code == 0:
            print('\n')
            print(''.join(['!' for i in range(80)]))
            print('')
            print('The entrys corresponding to the domain dimensioning are not' 
                   + ' valid!\n'
            )
            print('It seems you forgot the definition of the domain'
                   + ' dimensioning.'
            )       
            print('\nPlease check the configuration file.')
            print('')
            print(''.join(['!' for i in range(80)]))
            print('\n')   
            quit()            
        
        if err_code == 1:
            print('\n')
            print(''.join(['!' for i in range(80)]))
            print('')
            print('The entrys corresponding to the domain dimensioning are not' 
                   + ' valid!\n'
            )
            print('It seems you have did entrys in the STL_PATH parameter\n'
                   + 'as well as in the CORNER_POINT_COORD parameter.'
            )    
            print("Maybe you've forgot to comment out one of both options")
            print('\nPlease check the configuration file.')
            print('')
            print(''.join(['!' for i in range(80)]))
            print('\n')
            quit()
        
        if err_code == 2:
            print('\n')
            print(''.join(['!' for i in range(80)]))
            print('')
            print('The entrys corresponding number of box definition are not' 
                   + ' valid!\n'
            )
            print('It seems you have forgot to enter these parameters\n')
            print('\nPlease check the configuration file.')
            print('')
            print(''.join(['!' for i in range(80)]))
            print('\n') 
            quit()
        
        if err_code == 3:
            print('\n')
            print(''.join(['!' for i in range(80)]))
            print('')
            print('The path you entered in the configfile seems not to be'
                  + ' valid!\n'           
            )
            print('Please check for the correct location of the STL file\n'
                  + 'if you do using a relative path.'
            )
            print('')
            print(''.join(['!' for i in range(80)]))
            print('\n')   
            quit()
            
        if err_code == 4:
            print(''.join(['!' for i in range(80)]))
            print('')
            print("Can't decode the STL file!")
            print('')
            print('Currently only ASCII files are allowed.')
            print('Please convert the STL file in ASCII' +
                  ' by using meshlab or the ASCII option\n' +
                  'in ANSYS.'
            )
            print('')
            print(''.join(['!' for i in range(80)]))       
            quit()
        if err_code == 5:
            print(''.join(['!' for i in range(80)]))
            print("Can't decode the config file !!!")
            print('Please check the file encoding')
            print(''.join(['!' for i in range(80)]))       
            quit()

                