import scipy.io
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy import interpolate

###Some Constants
h = 6.62607004e-34 # m^2 kg / s 
c = 299792458 # m/s
m_per_nm = 10**-9 

def get_weights(wave_keep):  
    ''' This function returns the weights of each channel
    for a fiven frequency
    INPUT:
        wave_keep -> wavefunctions of interest
    OUTPUT:
        weights -> and array of shape (len(wave_keep),3)
    '''
    weights = np.zeros((len(wave_keep),3)) ## Getting weights of all waveleghts
    for i,wl in enumerate(wave_keep):
        if wl>=380. and wl<440:
            weights[i,0] = -1.0*(wl-440.)/(440.-380.)
            weights[i,2] = 1.0
        if wl>=440 and wl<490:
            weights[i,1] = (wl-440.)/(490.-440.)
            weights[i,2] = 1.0
        if wl> 490 and wl < 510:
            weights[i,1] = 1.0
            weights[i,2] = -1.*(wl-510.)/(510.-490.)
        if wl >= 510 and wl < 580:
            weights[i,0] = (wl-510.)/(580.-510.)
            weights[i,1] = 1.0
        if wl >=580 and wl<645:
            weights[i,0] = 1.0
            weights[i,1] = -1.*(wl-645.)/(645.-580.)
        if wl>= 645 and wl<780:
            weights[i,0] = 1.0 
    return  weights 

def get_linear(wave_keep,reflect):
    return

def read_image(fname):
    '''This function reads the from:
    https://scien.stanford.edu/index.php/faces-1-meter-viewing-distance/
    and manage them in a suitable way.
    (It can take a while, to charge it).
    INPUT:
        fname -> File name
    OUTPUT:
        reflect -> Fraction of light reflected
    '''
    ### Reading image
    mat = scipy.io.loadmat(fname)
    illum = mat['illuminant'][0][0]
    
    ### Ilumminant information
    # wavelengths
    illum_wl = [data[0] for data in illum[2][0]]
    illum_wl = np.array([data[0] for data in illum_wl[0]])
    # 
    illum_il = [data[0] for data in illum[3][0]]
    illum_il = [data[0] for data in illum_il[0]]
    #
    bitDepth = 32
    mxCompress = (2**bitDepth) - 1
    mn = np.float64(illum[3][0][0][1][0][0])
    mx = np.float64(illum[3][0][0][2][0][0])
    #
    s = mx-mn
    s = np.float64(s)
    #
    ucData = (s/mxCompress)*np.float64(illum_il) + mn; ## Photons wl of illuminant
    
    ### Number of photos of reflactance
    photons = mat['photons']
    photons.shape
    wave = mat['wave']
    # These are in nano-meters
    wave = np.array([w[0] for w in wave]) # Lambda in nm
    E_per_photon = h*c/(wave*m_per_nm)
    ilum_Energy = ucData*E_per_photon ## Illuminant energy
    energy = np.zeros(photons.shape)
    ## Fraction of energy reflected
    reflect = np.zeros(photons.shape)
    for i in range(len(E_per_photon)):
        energy[:,:,i] = E_per_photon[i]*photons[:,:,i]
    for i in range(len(ilum_Energy)):
        reflect[:,:,i] = energy[:,:,i]/ilum_Energy[i] # photo_energy/ilum_Energy of a given lambda
    return reflect,wave

def eye_sensitivity(reflect, wave, tranformation='linear'):
    '''This function converts the reflected '''
    eff = pd.read_csv('./input_data/spectral_luminous_efficiency.csv', sep = ',')
    x = eff.wavelength.values
    y = eff.phototopic.values

    tck = interpolate.splrep(x, y, s=0)
    xnew = [w for w in wave if w < 800]
    effnew = interpolate.splev(xnew, tck, der=0) # Splines to get an array with the lambdas
    ind_keep = [ind for ind in range(len(wave)) if wave[ind] < 780 and wave[ind] > 380 ] 
    wave_keep = wave[ind_keep]

    #photons_keep = photons[:,:,ind_keep]
    #energy_keep = energy[:,:,ind_keep]
    reflect_keep = reflect[:,:,ind_keep]
    lineal_pixels_reflect = np.reshape(reflect_keep,(reflect_keep.shape[0]*reflect_keep.shape[1],reflect_keep.shape[2]))
    reflect_weig = reflected_to_rgb(lineal_pixels_reflect,wave_keep)
    x,y = reflect_keep.shape[0:2]
    reflect_weig = np.reshape(reflect_weig,(x,y,3))
    return reflect_weig

def reflected_to_rgb(lineal_pixels_reflect,wave_keep,tranformation='linear'):
    '''This module converts the re
    INPUT: 
        reflect -> An array with the fraction of energy reflected.
        tranformation -> Method to map to RGB
    OUTPUT:
        
    '''
    ### Now let's read sensitivities 
    # The sensitivities of the eye to these wavelengths.
    
    weight = get_weights(wave_keep)
    reflect_weig = np.dot(lineal_pixels_reflect,weight)
    return reflect_weig

def wavelengthToRGB(w):
#perhaps make factor the phototopic array
#multiply corresponding wavelength 
# Taken from Earl F. Glynn's web page:
# http://www.efg2.com/Lab/ScienceAndEngineering/Spectra.htm Spectra Lab Report   
# http://stackoverflow.com/questions/1472514/convert-light-frequency-to-rgb
 
    factor = 0
    red = 0
    green = 0 
    blue = 0
    rgb = np.zeros(3)
    IntensityMax = 1
    Gamma = .80
    
    if(w >= 380 and w <440):
        red = -(w-440)/np.float((440-380))
        green = 0
        blue = 1
    elif(w>= 440 and w <490):
        red = 0
        green = (w-440)/np.float((490-440))
        blue = 1 
    elif(w>= 490 and w <510):
        red = 0
        green = 1
        blue = -(w-510)/np.float((510-490))
    elif(w >= 510 and w < 580):
        red = (w-510)/np.float((580-510))
        green = 1
        blue = 0 
    elif(w >= 580 and w < 645):
        red = 1
        green = -(w-645)/np.float((645-580))
        blue = 0 
    elif(w >= 645 and w < 781):
        red = 1
        green = 0 
        blue = 0
    #later make this cporrespond to interpolated phototopic 
    if (w>= 380 and w <420):
        factor = 0.3 + 0.7*(w - 380) / np.float((420 - 380))
    elif (w >= 420 and w < 701):
        factor = 1
    elif (w>= 701 and w < 781):
        factor = 0.3 + 0.7*(780 - w) / np.float((780 - 700))
    else:
        factor = 0 
    if red == 0:
        rgb[0] = 0 
    else: 
        rgb[0] = IntensityMax *(red * factor)**Gamma
    if green == 0:
        rgb[1] = 0
    else:    
        rgb[1] = IntensityMax *(green * factor)**Gamma
    if blue == 0:
        rgb[2] = 0
    else:
        rgb[2] = IntensityMax *(blue * factor)**Gamma
    
    return rgb

