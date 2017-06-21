import matplotlib.cm as cm
import numpy as np
#--- Attributes of the GUI ---#
BALL_RADIUS = 20.0        # FOR ballS IN PIXELS
bgcolour="#cccccc"      #BG colour for most bits of the widget
FRAMES_PER_SEC = 40     # SCREEN UPDATE RATE
IN_UPDATE=2000          # ms for output update!
OUT_UPDATE=2100          # ms for output update!

#--- INITIALISATION PARAMETERS ---#
WALL = 50               # FROM SIDE IN PIXELS
filenamein = "imgs/ESO.png" #initial image;
outimage = "imgs/output.png" #initial output image;
statusmsg = "Intial"    #start point


add_min=0 #initially we aren't adding any more antennas
BALLS = 50 #always start with 50 antenna
configmsg = "Spiral with " #initial config of antennas
balltext = str(BALLS)+" ant."         #initial number of antennas
x_pos = [0]             #initialise - otherwise get a x_pos not defined in first 
y_pos = [0]             # calc_uvplt call.
synthesis_type=0    # Always start with snapshot interferometry
pix_to_m=45.0     #for positions in array
col_map=cm.gist_gray    #default
freq=3e10               # Frequency
wavel=3e8/freq          # Wavelength
dec_ang=90.0            # Declination angle of 'source'
sin_dec=np.sin((dec_ang * np.pi)/ 180.) #sin of dec




#--- GUI Funcs ---#
def buttonColRows(button_w, button_h, nCols, nRows):    

    but_cols=[]
    but_rows=[]
    for nC in range(nCols):
        but_cols.append((nC*button_w)+((nC+1.0)*(button_w/10.0)))

    for nR in range(nRows):
        but_rows.append((nR*button_h)+((nR+1.0)*(button_h/10.0)))
    
    return but_cols,but_rows
    
