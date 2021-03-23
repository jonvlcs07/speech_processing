import numpy as np
import scipy as sp


def get_signal_energy(signal: list) -> float:
    """Gets the energy of a signal"""
    
    x = abs(signal)
    energy = sum(x ** 2)
    return energy


def signal_rms(signal: list) -> float:
    """Calculate signal rms"""
    
    temp = (signal ** 2).mean()
    rms = np.sqrt(temp)
    return rms
    

def snr_db(signal: list, noise: list) -> float:
    """Calculate the SNR of a noise and a signal"""
    
    x_rms = signal_rms(signal)
    noise_rms = signal_rms(noise)
    
    snr = (x_rms / noise_rms) ** 2
    snr_db = 10 * np.log10(snr)
    return snr_db


def fix_snr(signal: list, in_snr: float, desired_snr: float) -> list:
    """Get desired SNR by multiplying the signal by a gain"""

    if desired_snr == np.inf:
        gain = 0
    else:
        gain = 10 ** (0.05 * (in_snr - desired_snr))
    
    out_snr = gain * signal
    
    return out_snr


def cut_noise(speech: list, noise: list, pure_noise_len = 16000) -> list:
    """ """
    
    speech_len = len(speech)
    noise_len = len(noise)

    # Noise cut will be speech length + 16000 points (2s)
    cut_len = speech_len + pure_noise_len

    # Pega o ultimo valor possivel para fazer o recorte da amostragem
    last_value = len(noise[:-cut_len])

    cut_start = np.random.randint(0, last_value)
    cut_end = cut_start + cut_len
    noise_cut = noise[cut_start:cut_end]
    
    return noise_cut, cut_start


def zero_pad_beggining(bigger_signal: list, smaller_signal: list) -> list:
    """ """
    
    bigger_len = len(bigger_signal)
    smaller_len = len(smaller_signal)
    len_delta = bigger_len - smaller_len
    
    zero_padding = [0] * len_delta
    padded = np.concatenate((zero_padding, smaller_signal), axis = None)
    
    return padded


# Error Metrics

def frame_signal(sample_rate: int, frame_seconds: float, overlap: float, signal: np.array) -> np.array:
    """Cut signal into frames of specified length"""
    
    frame_length_samples = int(sr * frame_seconds)
    overlap = int(frame_length_samples *  overlap)
    
    frames = librosa.util.frame(signal,
                                frame_length = frame_length_samples,
                                hop_length = overlap,
                                axis = 0)
    return frames


def energy_delta(signal_ref: np.array, signal_comp: np.array) -> float:
    """Relative delta"""
    
    energy_ref = get_signal_energy(signal_ref)
    energy_comp = get_signal_energy(signal_comp)
    
    energy_diff = abs(energy_comp - energy_ref) / energy_ref
    return energy_diff


def fft_mod(signal: np.array) -> np.array:
    """Magnitude of a fft"""
    
    magnitude_spectra = abs(fft(signal))
    return magnitude_spectra


# No caso caso indice desse sinal seria o erro, que é o erro do bin
def spectrum_error_signal(signal_ref: np.array, signal_est: np.array) -> np.array:
    """Calculates de signal of absolute error between two spectra"""
    
    mod_ref = abs(fft_mod(signal_ref) - fft_mod(signal_est))
    return mod_ref


# Seria o erro por trecho
def error_by_frame(frames_ref: list, frames_est: list, n_frame: int) -> float:
    """Mean spectrum error of a frame"""
    
    est_frame = frames_ref[n_frame]
    ref_frame = frames_ss[n_frame]
    
    frame_length = len(ref_frame)
    frame_error = (sum(spectrum_error_signal(ref_frame, est_frame))
                   / frame_length)
    
    return frame_error


# Seria o erro por bin
def error_by_bin(frames_ref: list, frames_est: list, k_bin: int) -> float:
    """ """
    bin_error = 0
    n_frames = len(frames_ref) 
    
    for frame in range(n_frames):
        est_frame = frames_ref[frame]
        ref_frame = frames_ss[frame]
        frame_error = spectrum_error_signal(ref_frame, est_frame)
        bin_error += frame_error[k_bin]
    
    mean_bin_error = bin_error / n_frames    
    
    return mean_bin_error


# Erro Global
def global_error(frames_ref: list, frames_est: list) -> float:
    """ """
    global_error = 0
    n_frames = len(frames_ref)
    n_bins = len(frames_ref[0])
    ratio = n_frames * n_bins
    
    for n_frame in range(len(frames_ref)):
        est_frame = frames_ref[n_frame]
        ref_frame = frames_ss[n_frame]
        frame_error = spectrum_error_signal(ref_frame, est_frame)
        global_error += sum(frame_error)
    
    mean_global_error = global_error / ratio
    
    return mean_global_error