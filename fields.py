import numpy as np

################################################
# Calculate the gravity at a point             #
# Inputs:                                      #
#  - point_pos - position of the point         #
#  - r - radius of the mass                    #
#  - m - mass of the mass                      #
#  - G - gravitational constant                #
#  - mass_pos - position of the mass           #
# Outputs:                                     #
#  - gravity if the point is above the surface #
#  - None otherwise                            #
################################################
def gravityField(point_pos, r=6378.1e3, m=5.97219e24, G=6.67e-11, mass_pos=np.array([0,0])):
    rel_pos = point_pos - mass_pos
    xp = rel_pos[0]
    yp = rel_pos[1]
    
    # Check if the point is inside the earth and return None if it is
    if xp**2 + yp**2 < r**2:
        #return None
        pass
    
    # Else return the actual value
    g_mag = G * m/(xp**2 + yp**2)
    return (g_mag*-xp/(xp**2+yp**2)**0.5, g_mag*-yp/(xp**2+yp**2)**0.5)

##################################################
# Calculate drag at a point                      #
# Inputs:                                        #
#  - point_pos - position of the point (m)       #
#  - point_vel - velocity of the point (m/s)     #
#  - A - cross-sectional area of the point (m*m) #
#  - r - radius of the mass (m)                  #
#  - cd - coefficient of drag                    #
#  - mass_pos - position of the mass             # 
# Outputs:                                       #
#  - drag if the point is above the surface      #
#  - None otherwise                              #
##################################################
def dragField(point_pos, point_vel, A=(3.7/2)**2*np.pi, r=6378.1e3, cd=0.3, mass_pos=np.array([0,0])):
    # Calculate the height (distance from center of the earth minus radius of the earth
    rel_pos = point_pos - mass_pos # m
    h = np.sqrt(np.sum(rel_pos**2)) - r # m
    
    # Implement piece-wise function for density based on https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html
    # h < 11 km
    if h < 11000:
        temp = 15.04 - 0.00649*h # C
        pres = 101.29 * ((temp + 273.1)/288.08)**5.256
    # 11 km < h < 25 km
    elif h < 25000:
        temp = -56.46
        pres = 22.65 * np.exp(1.73 - 0.000157*h)
    # Zero point for drag, zero pressure sets entire density equation to zero
    else:
        temp = 1
        pres = 0
    
    # Calculate density
    p = pres / (0.2869 * (temp + 273.1))
    
    # Calculate the force of drag (see falling sphere assignment)
    return cd * A * p * point_vel**2 / 2
