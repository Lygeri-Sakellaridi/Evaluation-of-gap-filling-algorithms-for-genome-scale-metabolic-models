% Make model-specific dictionary to be used by fast gap fill.
% The dictionary maps bigg to kegg metabolite identifiers.
% The dictionary then needs to be manually curated for missing identifiers
% and duplicate values.

% Store model name and BiGG identifier.
% Change these lines to use a different model.
model_bigg_id = 'iMM904';
model_name = 'yeast_iMM904';

% Load the model.
model = loadBiGGModel(model_bigg_id, 'sbml');

% Get the metabolite identifiers in BiGG and KEGG namespace.
% Each result is stored in a cell structure,
% where the rows are metabolite ids, and there is only one column.
model_bigg_metids = model.metisbigg__46__metaboliteID;
model_kegg_metids = model.metKEGGID;

% Combine the cells horizontally.
% The result is a cell with two columns.
% The first column contains the BiGG metabolite identifiers
%The second column contains the KEGG metabolite identifiers.
model_metids = [model_bigg_metids, model_kegg_metids];

% Get the total number of metabolites.
number_of_mets = length(model.mets);

% Convert the cell to a table, and write the output to a tsv file.
model_met_dict = cell2table(model_metids);
dict_filename = model_name;
writetable(model_met_dict, dict_filename, 'FileType', 'text', 'Delimiter', '\t');

