% Script to reduce a model and then perform gap-filling.

iniCobraToolbox(false)
changeCobraSolver('ibm_cplex')

% Load the model.
model = loadBiGGModel('e_coli_core', 'sbml')
filename = 'core';

% Perform FBA
fba_ori = optimizeCbModel(model)

% Select reaction list to remove
removed_reactions = {'EX_fru_e',  'TALA',    'TPI',    'ME2',    'PFL', 'NH4t', 'RPI', 'PGI', 'THD2', 'ICL'}

% Set reaction weights
weights.MetabolicRxns = 0.1; % Kegg metabolic reactions
weights.ExchangeRxns = 0.5; % Exchange reactions
weights.TransportRxns = 10; % Transport reactions

% Prepare stats table
cnt = 1;
Stats{cnt,1} = 'Model name';cnt = cnt+1;
Stats{cnt,1} = 'Size S (original model)';cnt = cnt+1;
Stats{cnt,1} = 'Number of compartments';cnt = cnt+1;
Stats{cnt,1} = 'List of compartments';cnt = cnt+1;
Stats{cnt,1} = 'Number of blocked reactions';cnt = cnt+1;
Stats{cnt,1} = 'Number of solvable blocked reactions';cnt = cnt+1;
Stats{cnt,1} = 'Size S (flux consistent)';cnt = cnt+1;
Stats{cnt,1} = 'Size SUX (including solvable blocked reactions)';cnt = cnt+1;
Stats{cnt,1} = 'Number of added reactions (all)';cnt = cnt+1;
Stats{cnt,1} = 'Number of added metabolic reactions ';cnt = cnt+1;
Stats{cnt,1} = 'Number of added transport reactions ';cnt = cnt+1;
Stats{cnt,1} = 'Number of added exchange reactions ';cnt = cnt+1;
Stats{cnt,1} = 'Time preprocessing';cnt = cnt+1;
Stats{cnt,1} = 'Time fastGapFill';cnt = cnt+1;

% Initiate parameters
col = 1;
predicted_reactions={};
cnt = 1;
i = 1;

% Delete reactions on rxnList.
reduced_model = removeRxns(model, removed_reactions, false);

% perform fba
fba_reduced = optimizeCbModel(reduced_model);

% Ensure the reduced model is still a valid model structure
verifyModel(reduced_model)

% Remove constraints from exchange reactions.
EX = strmatch('EX_',reduced_model.rxns);
reduced_model.lb(EX)=-100;
reduced_model.ub(EX)=100;
clear EX

% Get basic model statistics
Stats{cnt,i+1} = filename;cnt = cnt+1;
[a,b] = size(reduced_model.S);
Stats{cnt,i+1} = strcat(num2str(a),'x',num2str(b));cnt = cnt+1;
%% 
% List of compartments to be consisdered during gap-filling
[tok,rem] = strtok(reduced_model.mets,'\[');
rem = unique(rem);
Stats{cnt,i+1} = num2str(length(rem));cnt = cnt+1;
Rem = rem{1};
for j = 2:length(rem)
    Rem = strcat(Rem,',',rem{j});
end
Stats{cnt,i+1} = Rem;cnt = cnt+1;
clear Rem tok rem;

% Prepare gap fill
tic; [consistModel,consistMatricesSUX,BlockedRxns] = prepareFastGapFill(reduced_model);
tpre=toc;

% Add more stats
Stats{cnt,i+1} = num2str(length(BlockedRxns.allRxns));cnt = cnt+1;
Stats{cnt,i+1} = num2str(length(BlockedRxns.solvableRxns));cnt = cnt+1;
[a,b] = size(consistModel.S);
Stats{cnt,i+1} = strcat(num2str(a),'x',num2str(b));cnt = cnt+1;
[a,b] = size(consistMatricesSUX.S);
Stats{cnt,i+1} = strcat(num2str(a),'x',num2str(b));cnt = cnt+1;

% Perform fastgapfill

epsilon = 1e-4;
tic; [AddedRxns] = fastGapFill(consistMatricesSUX,epsilon, weights);
tgap=toc;
Stats{cnt,i+1} = num2str(length(AddedRxns.rxns));cnt = cnt+1;

% Post-processing of results
IdentifyPW = 0;
[AddedRxnsExtended] = postProcessGapFillSolutions(AddedRxns, reduced_model,BlockedRxns);

% Moar stats
Stats{cnt,i+1} = num2str(AddedRxnsExtended.Stats.metabolicSol);cnt = cnt+1;
Stats{cnt,i+1} = num2str(AddedRxnsExtended.Stats.transportSol);cnt = cnt+1;
Stats{cnt,i+1} = num2str(AddedRxnsExtended.Stats.exchangeSol);cnt = cnt+1;

Stats{cnt,i+1} = num2str(tpre);cnt = cnt+1;
Stats{cnt,i+1} = num2str(tgap);cnt = cnt+1;

% Generate a reaction list.
% You can use this to calculate pecision/recall, especially if the ids are
% the same. Essentially, you compare the reactions in rxnList (those you
% removed) to the reactions in RxnList (those that algorithm were predicted).
predicted_reactions{1,col}=filename;predicted_reactions(2:length(AddedRxnsExtended.rxns)+1,col) = AddedRxnsExtended.rxns; col = col + 1;
predicted_reactions{1,col}=filename;predicted_reactions(2:length(AddedRxnsExtended.rxns)+1,col) = AddedRxnsExtended.rxnFormula; col = col + 1;
predicted_reactions{1,col}=filename;predicted_reactions(2:length(AddedRxnsExtended.rxns)+1,col) = AddedRxnsExtended.subSystem; col = col + 1;

% Re-add the RxnList to the reduced_model.
% Needs the original BiGG ids. To-do.

% Save results
save('core_gapfill10', 'Stats', 'removed_reactions', 'predicted_reactions', 'AddedRxnsExtended', 'fba_ori', 'fba_reduced')

