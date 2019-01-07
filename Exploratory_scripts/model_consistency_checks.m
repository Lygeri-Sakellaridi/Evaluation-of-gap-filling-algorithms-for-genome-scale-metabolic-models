% Run consistency checks on a model.
% Author: Lily Sakellaridi
% 7/01/2019

% initialise cobra toolbox, change solver 
initCobraToolbox(false)
changeCobraSolver('ibm_cplex')

% Load the model
% Change these lines to test different models.
model = loadBiGGModel('e_coli_core', 'sbml');
model_name = 'core';


% Is it a valid model? 1 yes, 0 no.
valid_model = verifyModel(model, 'simpleCheck', true);

% Is it mass-balanced?
% Is it flux consistent?
% Do the database IDs match with their expected identifiers?
model_issues = verifyModel(model, 'massBalance', true, 'fluxConsistency', true, 'checkDatabaseIDs', true);

% Is it stoichiometrically consistent?
printLevel = 0;

method.solver = 'ibm_cplex';
method.interface = 'solveCobraLP';

[inform, m, model] = checkStoichiometricConsistency(model, printLevel, method);
MetIncons = "I am a flag. My value will change if your model is infeasible."

if inform == 0
    stoich_consistent = "Your model is infeasible. The MetIncons variable contains the problematic metabolites."
    MetIncons = model.mets(~model.SConsistentBool);
elseif inform == 1
    stoich_consistent = "Congratulations! Your model is stoiciometrically consistent."
elseif inform == -1
    stoich_consistent = "I could not find a solution within the alloted time. Try a different solver."
elseif inform == 2
    stoich_consistent = "Unbounded solution, should never happen."
else
    stoich_consistent = "Wow, that's a first. I should not be able to have this value. Check your oeverall script."
end



out_filename = model_name + "_consistency_checks_result"

% Save the results in a file named after the model.
save(out_filename, 'valid_model', 'model_issues', 'stoich_consistent', 'MetIncons')

