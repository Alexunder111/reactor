

import numpy as np
import os

from mod.lib import *



config_obj = Config('./config_file.conf')
PARAMETERS = config_obj.get_config_data()


# check if the source of the corner points is a STL file
# or defined as coordinates in the configuration file.
if PARAMETERS[3] not in ['NULL', '']:
    

    # check for path errors
    if os.path.isfile(PARAMETERS[3]) == False:
        Error.error_report(err_code=3)

    # if no error is occored
    else:

        # do instancing a STL_ascii object     
        stl_domain_obj = STL_ascii(PARAMETERS[3])
        # get the corner points of the file
        corner_verts = stl_domain_obj.get_corner_points()


    # get an index map for maping a key to
    # an corresponding index of the corner verts
    # corner_vert_map = stl_domain_obj.get_corner_point_key_to_index_map()
    
else:
    corner_verts = PARAMETERS[-1]


# number of AER boxes in x direction
N_I = PARAMETERS[0]

# number of AER boxes in y direction
N_J = PARAMETERS[1]

# number of AER boxes in z direction
N_K = PARAMETERS[2]
 

A_0 = corner_verts[0]
B_0 = corner_verts[1]
C_0 = corner_verts[2]
D_0 = corner_verts[3]
A_1 = corner_verts[4]
B_1 = corner_verts[5]
C_1 = corner_verts[6]
D_1 = corner_verts[7]



### compute AER-box dimensioning

# get the sizes of the AER box edges

# length a refers to the x-direction
# length b refers to the y-direction
# length c refers to the z-direction

a, b, c = AERBox.get_box_dimensioning(A_0, B_0, C_0, A_1, N_I, N_J, N_K)




BOXES = [[[[] for k in range(N_K)] for j in range(N_J)] for i in range(N_I)]




    
 
 
 
 
 
 
 
 
 
 
# ######################## debugging ##########################

# from mpl_toolkits.mplot3d import Axes3D  
# import matplotlib.pyplot as plt


# X = []
# Y = []
# Z = []

# for vert in corner_verts:
    # X.append(vert[0])
    # Y.append(vert[1])
    # Z.append(vert[2])

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# max_range = np.max(np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)])) / 2.0

# mid_x = (max(X)+min(X)) * 0.5
# mid_y = (max(Y)+min(Y)) * 0.5
# mid_z = (max(Z)+min(Z)) * 0.5
# ax.set_xlim(mid_x - max_range, mid_x + max_range)
# ax.set_ylim(mid_y - max_range, mid_y + max_range)
# ax.set_zlim(mid_z - max_range, mid_z + max_range)



# LABEL = ['A_0', 'B_0', 'C_0', 'D_0', 'A_1', 'B_1', 'C_1', 'D_1']    

# i = 0    
# for vert in corner_verts:
    # ax.scatter(vert[0], 
               # vert[1],
               # vert[2],
               # color='green',
               # alpha=1
    # )
    # ax.text(vert[0], vert[1], vert[2], LABEL[i])
  
    # i += 1



# KINDS = ['inlet', 'outlet', 'left', 'right', 'bottom', 'top']

# for i in range(N_I):
    # for j in range(N_J):
        # for k in range(N_K):
            # for plainkind in KINDS:
                # box_obj = AERBox((i, j, k), (a, b, c), plainkind)
    
                # vert = box_obj.getPlainMidpoint() 
     
                # ax.scatter(vert[0] + A_0[0], vert[1] + A_0[1], vert[2] + A_0[2], color='blue')
# plt.show()
















