% Generate universal metabolite dictionary, that maps BiGG to KEGG
% identifiers.
% Author: Lily Sakellaridi

% Clear current workspace.
clear all;

% Load data from cobratoolbox/BiKEGG-master.

load('/home/sakel001/cobratoolbox/BiKEGG-master/AllKEGG2BiGGmet.mat');

% Assign identifiers to variables.
bigg_ids = AllKEGG2BiGGmet.Metbigg;
kegg_ids = AllKEGG2BiGGmet.Metkegg;

% Ensure there is an equal number of bigg and kegg identifiers.
assert(length(bigg_ids) == length(kegg_ids))

% Store the total number of metabolite identifiers.
total_mets = length(bigg_ids);

% Make the dicitonary.
b2k_met_dict = {};
for i = 1: total_mets
    b2k_met_dict{i, 1} = bigg_ids{1, i};
    b2k_met_dict{i, 2} = kegg_ids{1, i};
end

% The dictionary contains cells that are not 1X1.
% Trim them out.

trimmed_b2k_dict = {};
for i = 1: total_mets
    size_cell = size(bigg_ids{1, i});
    size_cell = size_cell(2);
    
    if size_cell > 1
        continue
    
    else
        trimmed_b2k_met_dict{i, 1} = bigg_ids{1, i};
        trimmed_b2k_met_dict{i, 2} = kegg_ids{1, i};
    end
end
