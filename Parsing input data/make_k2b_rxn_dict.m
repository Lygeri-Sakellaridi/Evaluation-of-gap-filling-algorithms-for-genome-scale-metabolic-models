% Generate model-specific reaction dictionary, mapping KEGG to BiGG identifiers.
% Author: Lily Sakellaridi

% clear the workspace.
clear all;

% Load model data from cobratoolbox/BiKEGG-master/BiGG2KEGG.
% load('/home/sakel001/cobratoolbox/BiKEGG-master/BiGG2KEGG/e_coli_coreKEGG.mat');

% Assign the identifiers to variables.
bigg_ids = B2Kegg.B;
kegg_ids = B2Kegg.K;

% Ensure that there is an equal number of kegg and bigg identifiers.
% Then, store that number.
assert(length(bigg_ids) == length(kegg_ids))
total_ids = length(bigg_ids);

% Create the dictionary.


k2b_rxn_dict = {};

for i = 1: total_ids
    k2b_rxn_dict(i, 1) = kegg_ids(i);
    k2b_rxn_dict(i, 2) = bigg_ids(i);
end

% Give the dicitonary a model-specific name.
iMM904_k2b_rxn_dict = k2b_rxn_dict;

% Clear all workspace variables except the dicitonary, and save the result.
clear B2Kegg bigg_ids kegg_ids k2b_rxn_dict total_ids i;

