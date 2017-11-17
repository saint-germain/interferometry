import matplotlib.pyplot as plt
import numpy as np

def intsim(in_img,ant,freq,myres):
    if in_img.shape[0]!=in_img.shape[1]:
        print("Error: Input image must have equal number of rows and colums")
        print("Current size = ",in_img.shape)
#        break find out how to give exception
    
    width=in_img.shape[0] 
    
    plt.figure(figsize=(5,5))
    plt.imshow(in_img);
    
    if ant<=1:
        ant=2
        print("Number of antennae must be between 2 and 50")
        print("You have 2 antennae now") # avoid single-antenna observations
    if ant>50:
        ant=50
        print("Number of antennae must be between 2 and 50")
        print("You have 50 antennae now") # we only have 50 available antennae
    AA=np.loadtxt("almapos.txt")
    almal_x=AA[0,:ant]
    almal_y=AA[1,:ant]
    # get max baseline in original array (between 0 and 1)
    # this ensures that the max baseline is scaled to one
    dx=almal_x.max()-almal_x.min()
    dy=almal_y.max()-almal_y.min()
    bl_scaled=np.max([dx,dy])

    x=almal_x/bl_scaled
    y=almal_y/bl_scaled
    
    plt.figure(figsize=(5,5))
    plt.scatter(x,y)
    plt.xlabel("x (Normalized)")
    plt.ylabel("y (Normalized)")
    plt.axis("equal");
    
    lx=np.zeros((ant,ant))
    ly=np.zeros((ant,ant))

    # calculate relative positions between antennae (baselines for the visibilities)
    for i in range(ant):
        for j in range(ant):
            lx[i,j]=(x[i]-x[j])
            ly[i,j]=(y[i]-y[j])
    wavel=3e8/freq
    u=lx/wavel      # u values in wavenumber
    v=ly/wavel      # v values in wavenumber
    re_u=np.reshape(u,(len(x)**2),order='F') #reshape u into linear form
    re_v=np.reshape(v,(len(y)**2),order='F')
    scfac=np.max([re_u.max(),re_v.max()]) # max uv distance (will be used to scale uv coverage)
    if myres < 1:
        print("Resolution cannot be smaller than 1 px")
        print("Resolution automatically set to 1 px")
        myres=1.
    if myres >= width:
        myres=width-1
        print("Resolution cannot be greater or equal to width")
        print("Resolution automatically set to width-1: ",width-1)
        
    ore_u=re_u*(width-1)/(2*myres*scfac)
    ore_v=re_v*(width-1)/(2*myres*scfac) 
    # UV gridding
    # create an empty matrix same size as in image for multiplying with fft of true sky image
    # this acts as a mask in fourier space (resolution of exactly 1 px)
    obs_uv_matrix=np.zeros(in_img.shape)          
    for k in range(len(ore_u)): 
        int_u=int((ore_u)[k])
        int_v=int((ore_v)[k])
        obs_uv_matrix[int_u,int_v]=1.0

    obs_uv_matrix[0,0]=0.0  
    print('Available uv grid points:',(obs_uv_matrix>0).sum(),'Total visibilities:',ant*(ant-1))

    plt.figure(figsize=[5,5]) 
    plt.plot(ore_u,ore_v,'.',color='orange')
    plt.xlabel('u [k$\lambda$]',size='10')
    plt.ylabel('v [k$\lambda$]',size='10')
    plt.show();

    plt.figure(figsize=[10,10]) 
    plt.imshow(obs_uv_matrix); # mask
    # Transform image to Fourier space, then multiply with uv mask and then apply the inverse FFT to reconstruct image
    # Max resolution uv coverage

    fft_img=np.fft.fft2(in_img)              #This is the complex visibility from a complete and ideal array from u,v =0,0 outward.
    observed=fft_img*obs_uv_matrix           #Observed complex visibility. Combines ideal visibility with the observed uv points, removing those not seen by the selected array configuration.
    ifft_img=np.fft.ifft2(observed)          #inverse FFTs the observed visibility
    real_ifft_img=ifft_img.real              #Takes real part only for plotting
    
    plt.figure(figsize=[5,5]) 
    plt.imshow(real_ifft_img);