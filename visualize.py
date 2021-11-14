import numpy as np
import fields

#############################################################
# Create x and y lists to draw earth at a point             #
# Inputs:                                                   #
#  - r - radius of the earth                                #
#  - num_angles - the number of angles to sample x and y at #
#  - pos - the position of the earth                        #
# Outputs:                                                  #
#  - x - x coordinates for the earth at all sample angles   #
#  - y - y coordinates for the earth at all sample angles   #
#############################################################
def genEarthLists(r=6378.1e3, num_angles=361, pos=np.array([0,0])):
    angles = np.linspace(0, 2*np.pi, num_angles)
    return r*np.cos(angles) + pos[0], r*np.sin(angles) + pos[1]

##########################################################################
# Create x, y, gx, and gy lists for a vector field with vectors at (x,y) #
# and that point with direciton (gx, gy)                                 #
# Inputs:                                                                #
#  - r - radius of the arth                                              #
#  - num_x_points - number of points to sample in the x direction        #
#  - num_y_points - number of points to sample in the y direction        #
#  - width_radius_ratio - the ratio between the width of the sample      #
#    space and the radius (ex. 4 means it will sample from -2r to 2r)    #
#  - height_radius_ratio -  the ratio between the height of the sample   #
#    space and the radius (ex. 4 means it will sample from -2r to 2r)    #
# Outputs:                                                               #
#  - X - x meshgrid from combining x and y sample points                 #
#  - Y - y meshgrid from combining x and y sample points                 #
#  - gx - x component of each vector at each point in space              #
#  - gy - y component of each vector at each point in space              #
##########################################################################
def genGravityLists(r=6378.1e3, num_x_points=10, num_y_points=10, width_radius_ratio=4, height_radius_ratio=4):
    # Generate x and y lists
    x = np.linspace(-(width_radius_ratio/2)*r, (width_radius_ratio/2)*r, num_x_points)
    y = np.linspace(-(height_radius_ratio/2)*r, (height_radius_ratio/2)*r, num_y_points)
    
    # Generate meshgrids for x and y
    X, Y = np.meshgrid(x,y)
    
    # Initialize vector components
    gx = np.zeros(X.shape)
    gy = np.zeros(Y.shape)
    
    # Get the gx and gy components at each sample point
    for i in range(X.shape[0]):
        for j in range(X.shape[0]):
            gx[i,j], gy[i,j] = fields.gravityField(np.array([X[i,j], Y[i,j]]), r=r)
    
    return X, Y, gx, gy