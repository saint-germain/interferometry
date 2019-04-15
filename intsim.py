import matplotlib.pyplot as plt
import numpy as np

def intsim(ant,freq,myres,EW=False,PointSource=False,filein="palomas.png"):
    in_img=plt.imread(filein)[:,:,0]
    if PointSource:
        t = np.linspace(-500, 500, 1000)
        bump = np.exp(-0.0005*t**2)
        bump = bump / np.trapz(bump) # normalize the integral to 1
        kernel = bump[:, np.newaxis] * bump[np.newaxis, :]
        in_img=kernel
    if in_img.shape[0]!=in_img.shape[1]:
        print("Error: Input image must have equal number of rows and colums")
        print("Current size = ",in_img.shape)

    width=in_img.shape[0] 
    
    if ant<=1:
        ant=2
        print("Number of antennae must be between 2 and 50")
        print("You have 2 antennae now") # avoid single-antenna observations
    if ant>50:
        ant=50
        print("Number of antennae must be between 2 and 50")
        print("You have 50 antennae now") # we only have 50 available antennae

    if myres < 1:
        print("Resolution cannot be smaller than 1 px")
        print("Resolution automatically set to 1 px")
        myres=1.
    if myres >= width:
        myres=width-1
        print("Resolution cannot be greater or equal to width")
        print("Resolution automatically set to width-1: ",width-1)

    AA=np.loadtxt("almapos.txt")
    almal_x=AA[0,:ant]
    almal_y=AA[1,:ant]
    # get max baseline in original array (between 0 and 1)
    # this ensures that the max baseline is scaled to one

    wavel=3e8/freq
    bmax=wavel*width/2
    print("Max. baseline =",bmax,"m")

# Antenna position adjustment to fit max. baseline
    dx=almal_x-almal_x.min()
    dy=almal_y-almal_y.min()
    dmax=np.max([dx.max(),dy.max()])
    dnx=dx/dmax
    dny=dy/dmax
    x=bmax*dnx
    y=bmax*dny
    lx=np.zeros((ant,ant))
    ly=np.zeros((ant,ant))

    if EW :
        x=np.linspace(0,1,ant)*bmax
        y=np.zeros(ant)

    # calculate relative positions between antennae (baselines for the visibilities)
    for i in range(ant):
        for j in range(ant):
            lx[i,j]=(x[i]-x[j])
            ly[i,j]=(y[i]-y[j])

    # remember that x and y are swapped in imshow
    u=ly/wavel      # u values in wavenumber
    v=lx/wavel      # v values in wavenumber
    re_u=np.reshape(u,(len(x)**2),order='F') #reshape u into linear form
    re_v=np.reshape(v,(len(y)**2),order='F') 


    ore_u=re_u/myres
    ore_v=re_v/myres


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


    maxuv=np.max([ore_u.max(),ore_v.max()])

    angres=(1/maxuv)*(180/np.pi)
    print("Current angular resolution =",angres,"deg")
#    print("Angular size in the sky=",angres*width,"deg") # needs work
    print("Max. baseline for selected resolution =",wavel*maxuv,"m")

    # Transform image to Fourier space, then multiply with uv mask and then apply the inverse FFT to reconstruct image

    fft_img=np.fft.fft2(in_img)              #This is the complex visibility from a complete and ideal array from u,v =0,0 outward.
    observed=fft_img*obs_uv_matrix           #Observed complex visibility. Combines ideal visibility with the observed uv points, removing those not seen by the selected array configuration.
    ifft_img=np.fft.ifft2(observed)          #inverse FFTs the observed visibility
    real_ifft_img=ifft_img.real              #Takes real part only for plotting





    f, axarr = plt.subplots(2, 3, figsize=(16,10));
    axarr[0,0].imshow(in_img,cmap='hot');
    axarr[0,0].set_title('Original')

    axarr[0,1].scatter(x*wavel*maxuv/bmax,y*wavel*maxuv/bmax,s=100);
    axarr[0,1].set_xlabel("x (m)");
    axarr[0,1].set_ylabel("y (m)");
    axarr[0,1].axis("equal");
    axarr[0,1].set_title('Antenna array')

    axarr[0,2].plot(ore_u.astype(int),ore_v.astype(int),'.',color='red');
    axarr[0,2].set_xlabel('Gridded u [k$\lambda$]',size='10');
    axarr[0,2].set_ylabel('Gridded v [k$\lambda$]',size='10');
    axarr[0,2].set_title('Gridded visibilities')



    
    with np.errstate(divide='ignore',invalid='ignore'):
        axarr[1,0].imshow(np.log10(np.abs(fft_img.real)),cmap='Reds');
    axarr[1,0].set_xlim(0,500);
    axarr[1,0].set_ylim(0,500);
    axarr[1,0].set_title('FT of original')


    axarr[1,1].plot(ore_u.astype(int),ore_v.astype(int),'.',color='red'); # mask
    axarr[1,1].set_xlim(0,500);
    axarr[1,1].set_ylim(0,500);
    axarr[1,1].set_xlabel('Gridded u [k$\lambda$]',size='10');
    axarr[1,1].set_ylabel('Gridded v [k$\lambda$]',size='10');
    axarr[1,1].set_title('Gridded visibilities')

    axarr[1,2].imshow(real_ifft_img,cmap='hot');
    axarr[1,2].set_title('Reconstructed image')

