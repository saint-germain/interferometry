from scipy.io import wavfile
import numpy as np
from scipy.fftpack import fft,fftfreq,ifft,fftshift
import matplotlib.pyplot as plt


def EasyFourier(fcut,filename='Darth_Vader.wav'):
    
    fs, data = wavfile.read(filename)
    n=len(data)
    freqs=np.arange(n)-n//2
    c=fftshift(fft(data))
    f, axarr=plt.subplots(1,3,figsize=(20,5))
    axarr[0].plot(freqs[n//2+1:],c.real[n//2+1:]);
    axarr[0].set_xlabel(r"$\nu$ (arbitrary units)")
    axarr[0].set_ylabel(r"$\operatorname{Re}(F(\nu))$ (arbitrary units)")
    axarr[0].axvline(x=fcut,c='r')
    axarr[0].set_title('FT of original')

    l=np.copy(c)
    l[np.abs(freqs)>fcut]=0
    axarr[1].plot(freqs[n//2+1:],l.real[n//2+1:]);
    axarr[1].set_xlabel(r"$\nu$ (arbitrary units)")
    axarr[1].set_ylabel(r"$\operatorname{Re}(F(\nu))$ (arbitrary units)")
    axarr[1].axvline(x=fcut,c='r')
    axarr[1].set_title('Low-pass filter')

    h=np.copy(c)
    h[np.abs(freqs)<fcut]=0
    axarr[2].plot(freqs[n//2+1:],h.real[n//2+1:]);
    axarr[2].set_xlabel(r"$\nu$ (arbitrary units)")
    axarr[2].set_ylabel(r"$\operatorname{Re}(F(\nu))$ (arbitrary units)")
    axarr[2].axvline(x=fcut,c='r')
    axarr[2].set_title('High-pass filter')

    l1=ifft(fftshift(l)).real
    l1=l1*data.max()/l1.max()
    h1=ifft(fftshift(h)).real
    h1=h1*data.max()/h1.max()
    fnamel=filename[:-4]+'LPF.wav'
    fnameh=filename[:-4]+'HPF.wav'


    wavfile.write(fnamel,fs,l1.astype(np.int16))
    wavfile.write(fnameh,fs,h1.astype(np.int16))
    return filename,fnamel,fnameh