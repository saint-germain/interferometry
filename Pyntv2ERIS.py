#--------------------------PYNTERFEROMETER v2------------------------------#
#
# The Pynterferometer was originally created and developed by 
# ADAM AVISON (1) and SAM GEORGE (2).
#
# Version 2 updated by ADAM AVISON.
# Webcam fix by amsr see lines 325 and following 
# For educational/non commercial use. If commerical use is desired please
# see www.jb.man.ac.uk/pynterferometer/download.html
#
# Version (MAC) 2.0 24/08/2015 
#---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -#
# (1) UK ALMA Regional Centre, Jodrell Bank Centre for Astrophysics,
#     University of Manchester.
#
# (2) Astrophysics Group, Cavendish Laboratory, University of Cambridge.
#-----------------------------------------------------------------------#

#----------------------------IMPORTED PACKAGES--------------------------#
from Tkinter import *
from ttk import *
import tkMessageBox
from PIL import Image, ImageTk
import math, os, time, sys
import numpy as np
import random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2



#--- Get stuff from functions directory
sys.path.insert(0,'funcs/')
from guiFuncs import *
from arrayFuncs import *
import antPositions

#---- GUI SPECIFIC FUNCTIONS ----------#
#--- THAT REALLY CAN'T GO ELSEWHERE ---#
#--------------------------------------#

#--- Setup simulation variables.---#
def initialise():
    global configmsg
    size=int(WIDTH_IMGS), int(HEIGHT_IMGS)
    im = Image.open(filenamein)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(filenamein, "PNG")

    orig_x, orig_y, zoom_factor,sythesis_type=changeArrayShape("Spiral")
    balls=build_balls()
    draw(balls, zoom_factor)
    updateStatus(4)
    
def ask_quit(): #--- QUIT SAFELY
    if tkMessageBox.askokcancel("Quit", "You really want to quit now?\nThink of all the fun you're quitting!"):
        plt.close('all')
        root.destroy()

def build_balls():
    global balls, add_min
    global orig_x, orig_y
    global x_pos, y_pos, BALLS
    ''' Create balls variable.'''
    if add_min == 1:
        add_min=0
        nu_orig_x=x_pos
        nu_orig_y=y_pos
        nu_orig_x=append(nu_orig_x,orig_x[BALLS])
        nu_orig_y=append(nu_orig_y,orig_y[BALLS])
        balls = tuple(Ball(nu_orig_x[ball], nu_orig_y[ball]) for ball in xrange(BALLS))
        balls = tuple(Ball(orig_x[ball], orig_y[ball]) for ball in xrange(BALLS))
    else:
        balls = tuple(Ball(orig_x[ball], orig_y[ball]) for ball in xrange(BALLS))

    return balls


def draw(balls, zoom_factor):
    ''' Draw array_canvas'''
    array_canvas.delete(ALL)
    array_canvas.create_line((X_LEFTOUT, Y_UPOUT, X_LEFTOUT, Y_DOWNOUT), fill='#00CC99', width=3)
    array_canvas.create_line((X_RIGHTOUT, Y_UPOUT, X_RIGHTOUT, Y_DOWNOUT), fill='#00CC99', width=3)
    array_canvas.create_line((X_RIGHTOUT, Y_DOWNOUT, X_LEFTOUT, Y_DOWNOUT), fill='#00CC99', width=3)
    array_canvas.create_line((X_RIGHTOUT, Y_UPOUT, X_LEFTOUT, Y_UPOUT), fill='#00CC99', width=3)
    #make grid
    for line in range(int(10*zoom_factor)+(int(np.ceil(zoom_factor)))):#great scott thats an ugly expressioN! 
        increment=((WIDTH_ANT-(2*WALL))/(10*zoom_factor))*line         # and requires 1.21 JW of power to solve. :p
        array_canvas.create_line(((X_LEFTOUT+increment), Y_UPOUT, (X_LEFTOUT+increment), Y_DOWNOUT), fill='black', width=1)
        array_canvas.create_line((X_RIGHTOUT, (Y_UPOUT+increment), X_LEFTOUT, (Y_UPOUT+increment)), fill='black', width=1)
    # Draw all balls.
    for ball in balls:
        x1 = ball.position.x - BALL_RADIUS
        y1 = ball.position.y - BALL_RADIUS
        x2 = ball.position.x + BALL_RADIUS
        y2 = ball.position.y + BALL_RADIUS
        array_canvas.create_oval((x1, y1, x2, y2), fill='#FF9900', outline='#FFC266')

    global x_pos, y_pos
    x_pos = tuple(ball.position.x for ball in balls)
    y_pos = tuple(ball.position.y for ball in balls)
        
def updateArray():
    ''' to update array canvas'''
    array_canvas.after(1000 / FRAMES_PER_SEC, updateArray)
    draw(balls,zoom_factor)

def changeArrayShape(arrType):
    global balls, zoom_factor, orig_x, orig_y, synthesis_type,configmsg
    rescaleFact=(Y_DOWNOUT-Y_UPOUT)*0.95

    if arrType == 'Spiral':
        print 'sp'
        orig_x=antPositions.spiral_x
        orig_y=antPositions.spiral_y
        zoom_factor=1.0
        sythesis_type=0
        configmsg = "Spiral with "
    if arrType == 'Yshape':
        print 'ys'
        orig_x=antPositions.Yshape_x
        orig_y=antPositions.Yshape_y
        zoom_factor=1.0
        sythesis_type=0
        configmsg = "Y-Shape with "
    if arrType == 'Line':
        orig_x=antPositions.line_x
        orig_y=antPositions.line_y
        zoom_factor=1.0
        sythesis_type=0
        configmsg = "Line with "
    if arrType == 'AlmaC':
        orig_x=antPositions.almac_x
        orig_y=antPositions.almac_y
        zoom_factor=1.0
        sythesis_type=0
        configmsg = "Alma Compact with "
    if arrType == 'AlmaM':
        orig_x=antPositions.almam_x
        orig_y=antPositions.almam_y
        zoom_factor=1.0
        sythesis_type=0
        configmsg = "Alma Mid with "
    if arrType == 'AlmaL':
        orig_x=antPositions.almal_x
        orig_y=antPositions.almal_y
        zoom_factor=1.0        
        sythesis_type=0
        configmsg = "Alma Extended with "
    orig_x=(np.array(orig_x)*rescaleFact)+Y_UPOUT
    orig_y=(np.array(orig_y)*rescaleFact)+Y_UPOUT
    balls=build_balls()

    draw(balls,zoom_factor)
    balltext = str(BALLS) + " ant.    "
    updateStatus(4)
    
    return orig_x, orig_y,zoom_factor, sythesis_type

def synthType(sType,orig_x,orig_y,add_min):
    global synthesis_type, BALLS
    if sType == 'Earth' or sType == 'Snap':
        if BALLS==1:
            BALLS=2
            add_min=1
            build_balls()

    if sType == 'Snap':
        synthesis_type=0
    if sType == 'Earth':
        synthesis_type=1
    if sType == 'Single':
        synthesis_type=2
        BALLS=1
        add_min=1
        build_balls()

    balltext = str(BALLS) + " ant."
    
    updateStatus(4)


def numAnts(thisNum):
    global BALLS, balltext,synthesis_type
    if synthesis_type==2:
        synthesis_type=0
    else:
        synthesis_type=synthesis_type
        
    BALLS=thisNum
    balltext = str(BALLS) + " ant.       " #extra padding for 5
    updateStatus(4)
    build_balls()

def addMinAnt(way):
    global BALLS, balltext,synthesis_type,add_min
    OLD_BALLS=BALLS
    add_min=1
    BALLS=BALLS+way
    if BALLS==1:
        synthesis_type=2
    elif BALLS==0:
        statusmsg = "Minimum Antennas = 1"
        updateStatus(3)
        BALLS=1
        synthesis_type=2
    elif BALLS>50:
        statusmsg = "Minimum Antennas = 50"
        updateStatus(3)
        BALLS=50
        synthesis_type=synthesis_type
    else:
        if OLD_BALLS ==1:
            synthesis_type=0
        else:
            synthesis_type=synthesis_type
        
    balltext = str(BALLS) + " ant.       " #extra padding for 5
    updateStatus(4)
    build_balls()

def zoomArray(factor):
    global zoom_factor
    zoom_factor=factor

                        
#--- Mouse related fucntions ---#
def on_motion(event):
    i=0
    for ball in balls:
        if(ball.userPick(event.x,event.y)):
            ball.antwasPick(event.x,event.y)
            isOut(event.x,event.y,i)
            checkCollision(i)
            draw(balls,zoom_factor)
        i=i+1

def on_release(event):
       release_x, release_y= event.x, event.y
       draw(balls,zoom_factor)

#--- Moving then antenna about ---#
def isOut (x,y,i):
    """See if antenna exceeds Canvas boundary"""
    # Ant pos outside x left
    if (x < X_LEFTOUT):
        print "less than XL"
        balls[i].position.x=orig_x[i]
        balls[i].position.y=orig_y[i]
        return True
    elif (x > X_RIGHTOUT):
        # Set xy - Position to start
        print "greater than XR"
        balls[i].position.x=orig_x[i]
        balls[i].position.y=orig_y[i]
        return True
    elif (y < Y_UPOUT):
        #Set xy - Position to start
        print "less than YU"
        balls[i].position.x=orig_x[i]
        balls[i].position.y=orig_y[i]
        return True
    elif (y > Y_DOWNOUT):
        # Set xy - Position to start
        print "greater than YD"
        balls[i].position.x=orig_x[i]
        balls[i].position.y=orig_y[i]
        return True
    else:
        return False

def checkCollision(i):
    """ Do the antenna collide """
    for ball in balls: 
        if(ball.colliding(balls[i])):
            shiftAway(i)
            break

def shiftAway(b):
        """ If they collide shift one away """
        rand=random.uniform(-1,1)
        balls[b].position.x = balls[b].position.x+((rand)*30.0)
        balls[b].position.y = balls[b].position.y+((rand)*30.0)
        isOut(balls[b].position.x,balls[b].position.y,b)
        

#--- Change Sky image ----#

def changeInpImage(img):
    global filenamein
    if img=='Gal':
        filenamein = "imgs/Galaxy.png"
    if img=='Nov':
        filenamein = "imgs/Nova.png"
    if img=='Pro':
        filenamein = "imgs/ProtoC.png"
    if img=='Love':
        filenamein = "imgs/Lovell.png"
    if img=='Eso':
        filenamein = "imgs/ESO.png"
    if img=='Dog':
        filenamein = "imgs/Dog.png"
          
    size=int(WIDTH_IMGS), int(HEIGHT_IMGS)
    im = Image.open(filenamein)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(filenamein, "PNG")

def useWebcam():
    ''' Connect to the webcam and process the image '''
    global filenamein, col_map
    filenamein = "imgs/input.png"
    ramp_frame=30 #ignore 30 frames to get the light levels right in image
    vidcap=cv2.VideoCapture()
    vidcap.open(0)
    for i in range(ramp_frame):
        retval,image=vidcap.read()

    vidcap.release()
    cv2.imwrite(filenamein,image)
    #on Mac OSX cv makes 640x480 images
    im = Image.open(filenamein)
    # AMSR - replace these two lines with the one below on Linux
  #  box = (400, 50, 800, 450)
  #  region = im.crop(box)
    region = im
    region.save(filenamein) #convert the file to the same size as AIPS
    #Colourscale input image
    in_img=Image.open(filenamein).convert("L")
    img_arr=np.asarray(in_img)
    fig_in = plt.figure(1, figsize=[(2.68*(WIDTH_ANT/600)),(2.68*(WIDTH_ANT/600))]) #Horrific aspect ratio hack... sorry!
    plt.gca().invert_yaxis()
    fig_in.clear()
    fig_in.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax_in=fig_in.add_subplot(111)
    #col_map=cm.gist_gray
    ax_in.imshow(img_arr, cmap=col_map)                
    ax_in.get_xaxis().set_visible(False)
    ax_in.get_yaxis().set_visible(False)
    plt.axis('off')
    fig_in.savefig('imgs/inputted.png', dpi=150, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches=None, pad_inches=None)
    filenamein='imgs/inputted.png'

#--------------SKY AND UV IMAGE FUCNTIONS ----------------------#
def updateInput():
    # to update array canvas
    input_image.after(IN_UPDATE, updateInput)
    drawInput()

def drawInput():
        inpimg=Image.open(filenamein)
        inpphoto=ImageTk.PhotoImage(inpimg)
        input_image.configure(image=inpphoto)
        input_image.image=inpphoto

def updateOutput():
    output_image.after(OUT_UPDATE, updateOutput)
    drawOutput()
    calcUVplt()

def drawOutput():
    outimg=Image.open('imgs/output.png')
    outphoto=ImageTk.PhotoImage(outimg)
    output_image.configure(image=outphoto)
    output_image.image=outphoto

def updateUV():
    uv_image.after(OUT_UPDATE, updateUV)
    drawUVplt()

def drawUVplt():
        uvimg=Image.open("imgs/uvplot.png")
        uvphoto=ImageTk.PhotoImage(uvimg)
        uv_image.configure(image=uvphoto)
        uv_image.image=uvphoto

def calcUVplt():
    global filenamein, col_map, x_pos, y_pos,  statusmsg
   
    '''Calculates the uv data and simulated images!'''
    in_img=mpimg.imread(filenamein) #gif_image
    in_img=in_img[:,:,1] #select a single colour plane from a RBG image
    img_siz=in_img.shape #input image dimensions

    statusmsg = "Calc. UV"
    updateStatus(3)

    pix_to_uv=150.0*(2.68*(WIDTH_ANT/600.0))

    umax=1.5*(((HEIGHT_ANT-(2.0*1.5*BALL_RADIUS))*pix_to_m*10.0)/wavel)#maximum for earth rot at HA 60
    vmax=1.5*((1.0*(WIDTH_ANT-(2.0*1.5*BALL_RADIUS))*pix_to_m*10.0*sin_dec)/wavel)
    
    if synthesis_type == 0 or synthesis_type ==1:    
        x=np.array(x_pos)
        y=np.array(y_pos)
        
        x=x*zoom_factor*pix_to_m
        y=y*zoom_factor*pix_to_m
        
        N=len(x)*(len(x)-1)                     #number of baselines

        lx=np.zeros((len(x),len(x)))
        ly=np.zeros((len(y),len(x)))

        for i in range(len(x)):
            for j in range(len(y)):
                lx[i,j]=(x[i]-x[j])
                ly[i,j]=(y[i]-y[j])
        
    if synthesis_type == 0:                          #snapshot mode
        u=(np.ceil(ly/wavel))                    # u values
        typeused = "Snapshot        "            #long white space to overlay correctly
        v=(np.ceil((-1.*lx*sin_dec)/wavel))      # v values
        
        re_u=np.reshape(u,(len(x)**2),order='F') #reshape u into linear form
        re_v=np.reshape(v,(len(y)**2),order='F') #reshape v into linear form
        
        full_re_u=re_u
        full_re_v=re_v

        #--- rescale to image scale
        full_re_uimg=(re_u/umax)*pix_to_uv
        full_re_vimg=(re_v/vmax)*pix_to_uv
                                                             
        obs_uv_matrix=np.zeros(img_siz)          #create an empty matrix same size as in image for multiplying with fft of true sky image

        for k in range(len(full_re_u)): 
            int_u=int(full_re_uimg[k])
            int_v=int(full_re_vimg[k])
            obs_uv_matrix[int_u,int_v]=1.0
                
    elif synthesis_type == 1:                         #Earth Rotation mode
        
        ha_range=[0.,20.,40.,60.,80.,100.,120.,140.,160.,180.]
        typeused = "Earth Rotation"
        u=0
        v=0
        full_re_u=0
        full_re_v=0
        
        for ha in ha_range:
            
            sin_ha=np.sin((ha * np.pi)/ 180.)
            cos_ha=np.cos((ha * np.pi)/ 180.)
            u=(np.ceil((((lx*sin_ha)+(ly*cos_ha))/wavel)))                    # u values including ha
            v=(np.ceil(((-1.*lx*sin_dec*cos_ha)+(ly*sin_dec*sin_ha))/wavel)) # v values
            
            re_u=np.reshape(u,(len(x)**2),order='F') #reshape u into linear form
            re_v=np.reshape(v,(len(y)**2),order='F') #reshape v into linear form
            full_re_u=np.append(full_re_u,re_u)
            full_re_v=np.append(full_re_v,re_v)
            #--- rescale to image scale
        full_re_uimg=(full_re_u/umax)*pix_to_uv
        full_re_vimg=(full_re_v/vmax)*pix_to_uv

                        
        obs_uv_matrix=np.zeros(img_siz) #create an empty matrix same size as in image for multiplying with fft of true sky image

        for k in range(len(full_re_uimg)):
            int_u=int(full_re_uimg[k])
            int_v=int(full_re_vimg[k])
            obs_uv_matrix[int_u,int_v]=1.0

    elif synthesis_type == 2:                     #Single Dish
        size_gauss=1.22*(wavel/12.)
        gaussian=gauss_kern(img_siz[0]/2,img_siz[1]/2)
        typeused = "Single Ant.    " #long white space to overlay corre
        obs_uv_matrix=np.zeros(img_siz)
        singledish=signal.fftconvolve(in_img,gaussian, mode='same')

        full_re_u=np.arange((-12.0/wavel),(12.0/wavel),0.1)
        full_re_v=np.arange((-12.0/wavel),(12.0/wavel),0.1)
        
    obs_uv_matrix[0,0]=0.0                   #fixes uv 0,0 to 0
    
    fig_uv = plt.figure(8,figsize=[(2.68*((HEIGHT_ANT*(2./3.))/570)),(2.68*((WIDTH_ANT*(2./3.))/570))]) #Horrific aspect ratio hack... sorry!
    fig_uv.clear()
    ax_uv = fig_uv.add_subplot(111)
    if synthesis_type == 0 or synthesis_type == 1:
        ax_uv.plot(full_re_u/1000.0,full_re_v/1000.0,'.',color='orange')#plot uv coverage
        #ax_uv.plot(0,0,'w.',mec='w')
    elif synthesis_type == 2:
        circ=pyl.Circle((0,0),radius=1.2,color='orange')
        ax_uv.add_patch(circ)
        ax_uv.set_xlim(-100.0,100.0)
        ax_uv.set_ylim(-100.0,100.0)
    ax_uv.tick_params(axis='both',labelsize='4')
    ax_uv.set_xlabel('u [k$\lambda$]',size='5')
    ax_uv.set_ylabel('v [k$\lambda$]',size='5')
    fig_uv.savefig('imgs/uvplot.png', dpi=150, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False,bbox_inches='tight',pad_inches=0.05)

    #---3 Do the maths ---#
    #--Section 7 chapter 2 Synthesis imaging--#
    fft_img=np.fft.fft2(in_img)              #This is the complex visibility from a complete and ideal array from u,v =0,0 outward.
    observed=fft_img*obs_uv_matrix           #Observed complex visibility. Combines ideal visibility with the observed uv points, removing those not seen by the selected array configuration.
    ifft_img=np.fft.ifft2(observed)          #inverse FFTs the observed visibility
    real_ifft_img=ifft_img.real              #Takes real part only for plotting

    fig_obs = plt.figure(4, figsize=[(2.68*(WIDTH_ANT/600.0)),(2.68*(WIDTH_ANT/600.0))]) #Horrific aspect ratio hack... sorry!
    fig_obs.clear()
    fig_obs.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax_obs=fig_obs.add_subplot(111)
    if synthesis_type == 0 or synthesis_type ==1:
        ax_obs.imshow(real_ifft_img, cmap=col_map)                #Show observed version of input image.
        ax_obs.get_xaxis().set_visible(False)
        ax_obs.get_yaxis().set_visible(False)
        #plt.gca().invert_yaxis()
        fig_obs.savefig('imgs/output.png', dpi=150, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=None)
        statusmsg = "Done: " + str(typeused)
        updateStatus(3)
    elif synthesis_type == 2:
        ax_obs.imshow(singledish, cmap=col_map)                #Show observed version of input image.
        ax_obs.get_xaxis().set_visible(False)
        ax_obs.get_yaxis().set_visible(False)
        #plt.gca().invert_yaxis()
        fig_obs.savefig('imgs/output.png', dpi=150, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=None)
        statusmsg = "Done: " + str(typeused)
        updateStatus(3)
    


#-----------------------------------------------------------------------#
def updateStatus(rowuse):
    global statusmsg
    global configmsg, balltext
    if rowuse == 3:
        statustext = Label(button_frame, text=statusmsg, relief=GROOVE)
        statustext.pack()
        statustext.place(bordermode=OUTSIDE, height=BUTTON_H, width=150, x=BUT_COL[6], y=BUT_ROW[1])

    if rowuse == 4:
        configtext = Label(button_frame, text=configmsg+balltext, relief=GROOVE)
        configtext.pack()
        configtext.place(bordermode=OUTSIDE, height=BUTTON_H, width=150, x=BUT_COL[6], y=BUT_ROW[2])

#==============================================================================================#        
#-----------------                         MAIN CODE                            ---------------#
#==============================================================================================#
         
#==========================================#
#-------------- GUI SETUP -----------------#

root = Tk()
root.title("Pynterferometer V2.0")
root.protocol("WM_DELETE_WINDOW", ask_quit)
#--- Define screen size ---#
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

#--- Set GUI size to window size ---#
root.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
root.configure(background = bgcolour)

#--- Setup array parameters
WIDTH_ANT, HEIGHT_ANT, X_LEFTOUT, X_RIGHTOUT, Y_UPOUT, Y_DOWNOUT, BUTTON_H, BUTTON_W, WIDTH_IMGS, HEIGHT_IMGS = setupArray(WIDTH, HEIGHT, BALL_RADIUS)


#--- The MAIN FRAME TO HOLD STUFF---#
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#--- The ARRAY canvas for moving your antennas ---#
array_canvas = Canvas(mainframe, width=WIDTH_ANT, height=HEIGHT_ANT, background='white', relief=GROOVE)
array_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
array_canvas.bind("<B1-Motion>", on_motion)
array_canvas.bind("<ButtonRelease-1>", on_release)
array_canvas.after(1000 / FRAMES_PER_SEC, updateArray)

#-------------------------------------------#
#===========================================#

#=========================================#
#-------------- BUTTONS! -----------------#
button_frame= Canvas(mainframe,background=bgcolour,height=(HEIGHT_ANT*(2./3.)),width=(WIDTH_ANT*(5./3.)),highlightcolor=bgcolour,highlightbackground=bgcolour)
button_frame.grid(columnspan=2,column=0, row=1, sticky=(N, W,E, S))

BUT_COL,BUT_ROW=buttonColRows(BUTTON_W, BUTTON_H, 9, 6)

#--- Array configs--------#
spiral=Button(button_frame, text="Spiral", command=lambda: changeArrayShape('Spiral'))
spiral.pack()
spiral.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[0],y=BUT_ROW[0])

y_shape=Button(button_frame, text="Y-shape", command=lambda: changeArrayShape('Yshape'))
y_shape.pack()
y_shape.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[0],y=BUT_ROW[1])

line=Button(button_frame, text="Line", command=lambda: changeArrayShape('Line'))
line.pack()
line.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[0],y=BUT_ROW[2])

almaC=Button(button_frame, text="ALMA\nCom", command=lambda: changeArrayShape('AlmaC'))
almaC.pack()
almaC.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[1],y=BUT_ROW[0])

almaM=Button(button_frame, text="ALMA\nMid", command=lambda: changeArrayShape('AlmaM'))
almaM.pack()
almaM.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[1],y=BUT_ROW[1])

almaL=Button(button_frame, text="ALMA\nExt", command=lambda: changeArrayShape('AlmaL'))
almaL.pack()
almaL.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[1],y=BUT_ROW[2])

#--- SYNTHESIS TYPE ----#
ear_rot=Button(button_frame, text="Earth\nRotation", command=lambda: synthType('Earth',orig_x,orig_y,add_min))
ear_rot.pack()
ear_rot.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[3], y=BUT_ROW[0])

snapshot=Button(button_frame, text="Snapshot\nmode", command=lambda: synthType('Snap',orig_x,orig_y,add_min))
snapshot.pack()
snapshot.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[3], y=BUT_ROW[1])

sing_dish=Button(button_frame, text="Single\nAntenna", command=lambda: synthType('Single',orig_x,orig_y,add_min))
sing_dish.pack()
sing_dish.place(bordermode=OUTSIDE,  height=BUTTON_H, width=BUTTON_W, x=BUT_COL[3], y=BUT_ROW[2])


#--- SKY IMAGE -------------#
sciOne=Button(button_frame, text="Use\nGalaxy", command=lambda: changeInpImage('Gal'))
sciOne.pack()
sciOne.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[4], y=BUT_ROW[0])

sciTwo=Button(button_frame, text="Use\nNova", command=lambda: changeInpImage('Nov'))
sciTwo.pack()
sciTwo.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[4], y=BUT_ROW[1])

sciThe=Button(button_frame, text="Use\nCluster", command=lambda: changeInpImage('Pro'))
sciThe.pack()
sciThe.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[4], y=BUT_ROW[2])


funOne=Button(button_frame, text="Use\nESO", command=lambda: changeInpImage('Eso'))
funOne.pack()
funOne.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[5], y=BUT_ROW[0])

funTwo=Button(button_frame, text="Use\nLovell", command=lambda: changeInpImage('Love'))
funTwo.pack()
funTwo.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[5], y=BUT_ROW[1])

funThe=Button(button_frame, text="Use\nDog", command=lambda: changeInpImage('Dog'))
funThe.pack()
funThe.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[5], y=BUT_ROW[2])


#--- WEBCAM
takecam=Button(button_frame, text="Use Webcam", command=useWebcam)
takecam.pack()
takecam.place(bordermode=OUTSIDE,height=BUTTON_H, width=2.1*BUTTON_W, x=BUT_COL[4], y=BUT_ROW[3])


#--- Add/min antennas --------#
five_ants=Button(button_frame, text="05\nAntennae", command=lambda: numAnts(5))
five_ants.pack()
five_ants.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[2], y=BUT_ROW[0])

ten_ants=Button(button_frame, text="10\nAntennae", command=lambda: numAnts(10))
ten_ants.pack()
ten_ants.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[2], y=BUT_ROW[1])

twe_ants=Button(button_frame, text="30\nAntennae", command=lambda: numAnts(30))
twe_ants.pack()
twe_ants.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[2], y=BUT_ROW[2])

add_ants=Button(button_frame, text="Add\nAntennae", command=lambda: addMinAnt(1))
add_ants.pack()
add_ants.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[0], y=BUT_ROW[3])

min_ants=Button(button_frame, text="Remove\nAntennae", command=lambda: addMinAnt(-1))
min_ants.pack()
min_ants.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[1], y=BUT_ROW[3])

#--- Zoom in zoom out ----#
#--Zoom---#
zoom_out=Button(button_frame, text="Increase\nArray Size", command=lambda: zoomArray(10.0))
zoom_out.pack()
zoom_out.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W,x=BUT_COL[0], y=BUT_ROW[4])

unzoom_bu=Button(button_frame, text="Normal\nArray Size", command=lambda: zoomArray(1.0))
unzoom_bu.pack()
unzoom_bu.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[1], y=BUT_ROW[4])

zoom_in=Button(button_frame, text="Decrease\nArray Size", command=lambda: zoomArray(0.1))
zoom_in.pack()
zoom_in.place(bordermode=OUTSIDE, height=BUTTON_H, width=BUTTON_W, x=BUT_COL[2], y=BUT_ROW[4])

#-----------------------------------------#
#=========================================#

#==========================================#
#--------------SKY IMAGES------------------#
#--INPUT IMAGE--#
inpimg=Image.open(filenamein)
inpphoto=ImageTk.PhotoImage(inpimg)
input_image = Label(mainframe,image=inpphoto, width=(WIDTH_IMGS*5./3.),background=bgcolour, anchor=CENTER, relief=GROOVE)
input_image.grid(column=1, row=0, sticky=(N, W, E, S), ipadx=(WIDTH_ANT*1./25.),ipady=(WIDTH_ANT*1./25.))
input_image.after(1000 / FRAMES_PER_SEC, updateInput)

#--OUTPUT IMAGE--#
outimg=Image.open(outimage)
outphoto=ImageTk.PhotoImage(outimg)
output_image = Label(mainframe, image=outphoto, width=(WIDTH_IMGS*5./3.),background=bgcolour,anchor=CENTER, relief=GROOVE)
output_image.grid(column=2, row=0, sticky=(N, W, E, S), ipadx=(WIDTH_ANT*1./25.),ipady=(WIDTH_ANT*1./25.))
output_image.after(1000 / FRAMES_PER_SEC, updateOutput)

#-----------------------------------------#
#=========================================#

#============================================#
#--------------STATUS STUFF------------------#
namestatus = Label(button_frame, text='Status',font=("Helvetica", 16),relief=GROOVE)
namestatus.pack()
namestatus.place(bordermode=OUTSIDE, height=BUTTON_H, width=150, x=BUT_COL[6], y=BUT_ROW[0])

statustext = Label(button_frame, text=statusmsg,relief=GROOVE)
statustext.pack()
statustext.place(bordermode=OUTSIDE, height=BUTTON_H, width=150, x=BUT_COL[6], y=BUT_ROW[1])

configtext = Label(button_frame, text='saaa',relief=GROOVE)
configtext.pack()
configtext.place(bordermode=OUTSIDE, height=BUTTON_H, width=150, x=BUT_COL[6], y=BUT_ROW[2])
#--------------------------------------------#
#============================================#

#============================================#
#--------------MEDIA FRAME ------------------#
media_frame= Canvas(mainframe,background=bgcolour,height=(HEIGHT_ANT*(2./3.)),width=(WIDTH_ANT*(2./3.)),highlightcolor=bgcolour,highlightbackground=bgcolour)
media_frame.grid(column=2, row=1, sticky=(N, W,E, S))

#--UV IMAGE--#
uv_img=Image.open("imgs/uvplot.png")
uvphoto=ImageTk.PhotoImage(uv_img)
uv_image = Label(media_frame, image=uvphoto, width=(WIDTH_IMGS*4./3.),background=bgcolour,anchor=CENTER, relief=GROOVE)
uv_image.pack()
uv_image.after(1000 / FRAMES_PER_SEC, updateUV)

logo=Image.open("imgs/arclogo_adv.png")
logophoto=ImageTk.PhotoImage(logo)
logo_image = Label(button_frame,image=logophoto, background=bgcolour)
logo_image.pack()
logo_image.place(bordermode=OUTSIDE, height=51, width=150,x=BUT_COL[6],y=BUT_ROW[3]-5)

manlogo=Image.open("imgs/mancam.png")
manlogophoto=ImageTk.PhotoImage(manlogo)
manlogo_image = Label(button_frame,image=manlogophoto, background=bgcolour)
manlogo_image.pack()
manlogo_image.place(bordermode=OUTSIDE, height=51, width=150, x=BUT_COL[6],y=BUT_ROW[4]-1)

#--------------------------------------------#
#============================================#


#=========================================#
#--- Initialise the array, input image ---#

initialise()

#--- RUN THE GUI ---#

root.mainloop()
