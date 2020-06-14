function [X] = STFT_DFT(input, N, L, w)
% Output is the spectogram using the FT method for STFTs

if nargin < 5
    a = 0.54;
    b = -0.46;
    phi = pi/N;
    w = 2/sqrt(4*a^2+2*b^2)*(a+b*cos(2*pi*(0:N-1)'/N+phi));
end

% Zero-pad the input
if mod(length(input), L) > 0
    input = [input; zeros(L-mod(length(input),L),1)];
end

fftN = N;
X = zeros(fftN,floor((length(input)-N)/L)+1);
for m = 1:(length(input)-N)/L+1
    section = w.*input((m-1)*L+1:(m-1)*L+N);
    section_freq = fft(section,fftN);
    X(:,m) = section_freq(1:end);
end
end