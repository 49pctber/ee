import os
import numpy as np

def estimateSNR(z):
    '''
    This algorithm blindly estimates the SNR of a given audio signal, z.
    Method based on Wave Amplitude Distribution Analysis (WADA) Signal to Noise Ratio (SNR) estimation
    by Kim and Stern.

    Notes:
    * The values of the lookup table were pre-computed and stored in 'Alpha0.400000.txt'
    * This algorithm works best when the signal in question is speech and the noise is non-speech
    * Minimum estimated SNR = -20dB. Maximum estimated SNR = 100dB. SNRs outside of this range will default to one of these extrema
    * Algorithm works best for SNRs below 20dB

    Inputs:
        z (numpy array): The audio signal in question
    Outputs:
        SNR (float): SNR of input z (in dB)
    '''
    # Import LUT
    file = 'Alpha0.400000.txt'
    with open(file) as f:
        SNR = []
        G_z = []
        for line in f:
            contents = line.split(' ')
            SNR.append(float(contents[0]))
            G_z.append(float(contents[-1]))

    LUT = np.vstack((np.array(G_z), np.array(SNR)))

    # Normalize
    z -= z.mean()
    z /= np.max(np.abs(z))

    # Calculate G_z
    G_z = np.log(np.mean(np.abs(z))) - np.mean(np.log(np.abs(z)))

    # Use LUT, interpolate
    if G_z >= LUT[0,-1]:
        SNR = LUT[1,-1]
    elif G_z <= LUT[0,0]:
        SNR = LUT[1,0]
    else:
        idx = np.where(LUT[0]>G_z)[0][0]
        x1 = LUT[0, idx-1]
        x2 = LUT[0, idx]
        y1 = LUT[1, idx-1]
        y2 = LUT[1, idx]
        lam = (G_z - x2)/(x1 - x2)

        SNR = lam*y1 + (1-lam)*y2

    return SNR
