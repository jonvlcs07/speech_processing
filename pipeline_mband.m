signals = load('dados/lists_of_files/signals_listing.mat');
signals = signals.signals;

in_paths = load('dados/lists_of_files/pp_signals_path_listing.mat');
in_paths = in_paths.pp_signals_path_listing;

n_signals = size(in_paths, 1);

for i = 1:n_signals
    in_file = in_paths(i,:);
    in_file = strtrim(in_file);
    out_file = strcat("dados/denoised_data_mband/", signals(i,:));
    out_file = convertStringsToChars(out_file);
    out_file = strtrim(out_file);
    
    disp(in_file)

    mband(in_file, out_file, 5, 'linear');
end

