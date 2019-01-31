#!/usr/bin/env/ python3
"""
Script to evaluate the Cobrapy gap-filling implementation
on several models.

Author: Lily Sakellaridi
"""

import cobra.test
from cobra.flux_analysis import gapfill
import os
from sys import argv, exit

def precision_recall_calculator(reactions_removed, reactions_restored):
    """
    Calculates precision and recall from gap-filling results.
    
    reactions_removed: list; the reactions originally removed
    reactions_restored: list; the reactions predicted by the algorithm
    """
    
    reactions_removed = set(reactions_removed)
    reactions_restored = set(reactions_restored)
    
    true_positives = reactions_removed.intersection(reactions_restored)
    
    precision = len(true_positives)/len(reactions_restored)
    recall = len(true_positives)/len(reactions_removed)
    
    return precision, recall



if __name__=="__main__":
    # Step 1: Get the inputs from the command line.
    if len(argv) != 5:
        print("Script usage: python3 evaluation.py <model> <reference> <reaction_set> <number_of_iterations\n"
        "model: the genome-scale model under analysis; .json file\n"
        "reference: the reference database (eg BiGG); .json file\n"
        "reaction_set: the reactions you want to remove to introduce gaps\n"
        "number_of_iteractions: the number of times you want the algorithm to run\n"
        "It is important to use python3 instead of python! Otherwise, the script\n"
        "Will not be able to detect gurobi and cplex!")
        exit(0)
    
        
    model = cobra.io.read_sbml_model(argv[1])
    reference = cobra.io.load_json_model(argv[2])
    reaction_set = argv[3]
    number_of_iterations = int(argv[4])
    
    # I assume the reaction set is a file with a single line
    # that has the format "RXN1 RXN2"
    with open(reaction_set) as rs:
        lines = rs.readlines()
        reaction_set = lines[0].rstrip().split(" ")
        print(reaction_set)
        print(type(reaction_set))

    # Change the solver to gurobi or cplex.
    # gplk can't handle this.

    model.solver = "gurobi"

    # Store the original reaction number
    len_rxns_ori = len(model.reactions)

    # Run fba
    fba_ori = model.slim_optimize()
    print("Original fba")
    print(fba_ori)

    # Introduce artificial gaps
    model.remove_reactions(reaction_set)
    print("You successfully removed the reactions")

    # Run fba again
    fba_degraded = model.slim_optimize()
    print("Degraded fba")
    print(fba_degraded)

    # Sanity checks

    try:
        assert len(model.reactions) < len_rxns_ori
    except AssertionError:
        print("You did not remove any reactions.")
        exit(0)
    try:
        assert fba_degraded < fba_ori
    except AssertionError:
        print("Warning: The reactions you removed are not significant for growth.")
    
    # Perform gap-filling
    # If it growls at you with 'solver status infeasible' or some shit, set demand_reactions = True.
    result = gapfill(model, reference, demand_reactions = False, iterations = number_of_iterations)
    solutions = []
    for i, entries in enumerate(result):
        print("---- Run %d ----" % (i + 1))
        solution = []
        for e in entries:
            print(e.id)
            solution.append(e.id)
        solutions.append(solution)
    
    print(solutions)

    # Run fba on the restored model
    #fba_restored = model.optimize().objective_value
    #print(fba_restored)

    # Calculate precision and recall 
    # The original reaction set is reaction_set, a list containing
    # the removed reactions.
    # The variable solutions contains lists, whose number is equal
    # to the number of iterations. Each list is a different solution
    # to be compared to the original set.

    precisions = []
    recalls = []
    for i, solution in enumerate(solutions):
        #print(solution)
        #print(type(solution))
        precision, recall = precision_recall_calculator(reaction_set, solution)
    
        precisions.append(precision)
        recalls.append(recall)
    
        print("Precision for run %d" % i)
        print(precision)
        print("Recall for run %d" % i)
        print(recall)
    
    precision_avg = sum(precisions)/number_of_iterations
    recall_avg = sum(recalls)/number_of_iterations
    
    print("Average precision")
    print(precision_avg)
    print("Average recall")
    print(recall_avg)
    





    
    
    


