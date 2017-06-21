from scipy import *
from scipy import signal, ndimage
import pylab as pyl
import antPositions
from PyntV2_balls import *
from PyntV2_TwoD import *


def setupArray(WIDTH, HEIGHT, BALL_RADIUS):
    #--- Define Telescope array parameters based on screen size ---#
    WIDTH_ANT= WIDTH/2.5
    HEIGHT_ANT= WIDTH/2.5
    X_LEFTOUT=BALL_RADIUS*1.5                  # LEFT BOUNDARY
    X_RIGHTOUT=WIDTH_ANT-(BALL_RADIUS*1.5)     # RIGHT BOUNDARY
    Y_UPOUT=BALL_RADIUS*1.5                    # TOP BOUNDARY
    Y_DOWNOUT=HEIGHT_ANT-(BALL_RADIUS*1.5)     # BOTTOM BOUNDARY
    BUTTON_H=WIDTH_ANT*(1./12.)
    BUTTON_W=WIDTH_ANT*(1./5.)
    WIDTH_IMGS=WIDTH_ANT*(2./3.)
    HEIGHT_IMGS=WIDTH_IMGS

    return WIDTH_ANT, HEIGHT_ANT, X_LEFTOUT, X_RIGHTOUT, Y_UPOUT, Y_DOWNOUT, BUTTON_H, BUTTON_W, WIDTH_IMGS, HEIGHT_IMGS

def gauss_kern(size, sizey=None):
    '''borrowed from StackOverflow and wikipedia'''
    size = int(size)    
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)               
    x, y = mgrid[-size:size, -sizey:sizey]
    A = 1
    x0 = 0
    y0 = 0
 
    sigma_x = size/2.35482
    sigma_y = sizey/2.35482
 
    theta = 180
    theta=float(theta)/pi
    a = cos(theta)**2/2/sigma_x**2 + sin(theta)**2/2/sigma_y**2;
    b = -sin(2*theta)/4/sigma_x**2 + sin(2*theta)/4/sigma_y**2 ;
    c = sin(theta)**2/2/sigma_x**2 + cos(theta)**2/2/sigma_y**2;

    Z_exp_x=((x-x0)**2)/(2*(sigma_x**2))
    Z_exp_y=((y-y0)**2)/(2*(sigma_y**2))

    Z=A*exp(-1*(Z_exp_x+Z_exp_y))
    return Z/Z.sum()
