function [output_signal, fs] = Griffin_Lim_Example(show_plot)
    %% README
    
    % This example illustrates how the Griffin-Lim algorithm should be
    % used. The output of this function is the signal reconstructed with
    % this method and the corresponding sample rate. Play back and compare
    % to the 'welcome16k.wav' file to hear if it worked.
    % You may also toggle the show_plot variable to see the
    % divergence measure over iterations.
    
    %% Script
    % Initialize
    win_length = 512;
    iterations = 100;
    hop_length = 128;
    
    if nargin == 0
       show_plot = false;
    end
    
    [input_signal, fs] = audioread('welcome16k.wav');
    
    % Modified Hamming window works best
    a = 0.54;
    b = -0.46;
    phi = pi/win_length;
    wind = 2/sqrt(4*a^2+2*b^2)*(a+b*cos(2*pi*(0:win_length-1)'/win_length+phi));
    % Alternatively, use a rectangular window for arbitrary window spacing
    %wind = rectwin(win_length);
    
    % Acquire the magnitude spectrogram of the signal
    spectrogram = STFT_DFT(input_signal, win_length, hop_length, wind);
    signal_mag = abs(spectrogram);
    
    % Run function
    output_signal = Griffin_Lim(signal_mag, win_length, hop_length, wind, iterations, show_plot);
end

