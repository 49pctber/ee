function [x] = Griffin_Lim(Y_mag, win_length, hop_length, wind, n_iter, show_plot)
% This function implements the Griffin-Lim MSTFT reconstruction algorithm
% (LSEE-MSTFTM). Given only the magnitude spectrogram (no phase) of a given
% signal, this algorithm can iteratively estimate the phase of the STFT,
% and thus produce an approximation of the original signal.

% Initialize
if nargin < 6
    show_plot = false;
end
if nargin < 5
    n_iter = 50;
end

% Calculate this power once only
wind_energy = sum(wind.^2);

% Initialize signal x randomly, extract phase
x = rand(((size(Y_mag,2)-1)*hop_length)+win_length,1);
X = STFT_DFT(x, win_length, hop_length, wind);
phase = unwrap(angle(X));

% Run the iterative algorithm
for iter = 1:n_iter
    % Calculate X_hat from given magnitude and current phase estimate
    X_hat = Y_mag.*exp(1j*phase);
    D_M(iter) = sum(sum((abs(X)/max(max(abs(X))) - Y_mag/max(max(abs(Y_mag)))).^2)/(2*pi));
    % Initialize new x variable for this iteration
    x = zeros(((size(X_hat,2)-1)*hop_length)+win_length,1);
    % For each column of the STFT...
    for m = 1:size(X_hat,2)
        % Reconstruct the segment
        x_seg = ifft(X_hat(:,m), win_length);
        
        % Find the beginning and end indices of the segment in time
        start_ind = (m-1)*hop_length+1;
        end_ind = start_ind+length(x_seg)-1;
        % Sum terms at the corresponding indices
        x(start_ind:end_ind) = x(start_ind:end_ind) + x_seg.*wind/wind_energy;
    end
    % Get the new phase
    X = STFT_DFT(x, win_length, hop_length, wind);
    phase = unwrap(angle(X));
end

if show_plot
    figure(1)
    plot(D_M(2:end))
    title('D_M over iterations')
    xlabel('Iteration')
    ylabel('D_M')
end

% Reconstruction can come out complex
% Return only real part, normalized between -1 and 1
x = real(x)/max(max(abs(real(x))));
end

