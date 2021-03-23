infile_denoised = 'dados/denoised_data/signal_4.wav';
infile_clean = 'dados/falas_04/resampled_rate/F180902.WAV';
sr = 8000;

[denoised, sr] = audioread(infile_denoised);
denoised = denoised(16001:end);

[clean, sr] = audioread(infile_clean);

[d,g,rr,ss]  = v_sigalign(denoised, clean);

rr_clean = 'dados/aligned_noises/signal_4_rr.wav';
ss_clean = 'dados/aligned_noises/signal_4_ss.wav';

audiowrite(rr_clean, rr, sr);
audiowrite(ss_clean, ss, sr);

