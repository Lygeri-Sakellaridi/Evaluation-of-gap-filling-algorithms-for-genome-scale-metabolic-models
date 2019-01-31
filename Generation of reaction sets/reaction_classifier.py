#!/usr/bin/env python3
"""
Script to generate reaction sets that will be used for evaluation of gap-fillers.

First, the script classifies a model's reactions according to their effect on growth.
The reaction files used as input are the result of single reaction deletion analysis. 

Afterwards, reaction sets are generated using the classified reaction lists as input.

Finally, the generated lists are written to their corresponding output files.

Author: Lily Sakellaridi
"""

from sys import argv, exit
from random import sample
import os

def reaction_classifier(lines, max_growth):
    """
    Classifies model reactions in essential, no-effect, influential and infeasible.
    
    INPUT:
    lines: open line format csv file. The file contains the output dataframe
    from single deletion analysis.
    
    OUTPUT:
    reaction_names_dict: dictionary where
    keys: the names of each reaction type (eg 'essential'); str
    values: the reactions belonging to each type (eg essential_reactions); list
    """
    
    # If the growth rate is above this value, the model considered as growing.
    tol_growth = 1e-06
    
    # If the difference between maximum growth and observed growth is below this value,
    # the reaction is considered to have no effect.
    # Use 95% of max growth as a good threshold.
    upper_limit = (95/100) * max_growth
    #print("upper_limit is: " + str(upper_limit))
    
    
    assert upper_limit >= 0
    
    essential_reactions = []
    influential_reactions = []
    no_effect_reactions = []
    infeasible_reactions = []
    
    for line in lines[1:]:        # remove header
        line = line.rstrip()
        line = line.split(",")
        reaction_id = line[0]
        reaction_id = reaction_id[12:-3]
        #print(reaction_id)
        growth_rate = line[1]
        #print(growth_rate, type(growth_rate))
        solver_status = line[2]
        #print(line)
        
        if solver_status == "infeasible":
            infeasible_reactions.append(reaction_id)
        
            
        else:   
        
            growth_rate = float(growth_rate)
            #print(growth_rate, type(growth_rate))
            if growth_rate < tol_growth:
                essential_reactions.append(reaction_id)
                
            elif growth_rate >= upper_limit:
                
                
                no_effect_reactions.append(reaction_id)
            else:
                influential_reactions.append(reaction_id)
                
    #reaction_types = ['essential', 'no_effect', 'influential']
    reaction_lists = [essential_reactions, no_effect_reactions, influential_reactions]
    #reaction_types_dict = dict(zip(reaction_types, reaction_lists))
    return reaction_lists
    
def write_list_to_file(reaction_list):
    """
    Writes a list of reactions to a space-separated file.
    
    reaction_list: list of reactions of a specific type, eg essential; list
    reaction_type: str
    """
    with open('reactions', 'w') as out:
        for reaction in reaction_list:
            out.write(reaction + " ")
    
            
    
if __name__=="__main__":
    
    # Step 1: Get the input arguments
    if len(argv) != 3:
        print("The first argument is the file that is the output from single reaction deletion analysis.")
        print("For example, iJO166.xml_srd_result.")
        print("The second argument is the maximum growth of the model you're examining.")
        print("The max growth is 0.9824 for iJO1366, and 0.2879 for iMM904.")
        exit(0)
    infile = argv[1]
    #print(infile)
    
    max_growth = float(argv[2])
    #print(max_growth, type(max_growth))
    
    # Step 2: Classify the reactions
    with open(infile) as inf:
        lines = inf.readlines()
        reaction_lists = reaction_classifier(lines, max_growth)
        #print(reaction_lists)
        
    # Step 3: Write each output to a corresponding file.
    essential = reaction_lists[0]
    no_effect = reaction_lists[1]
    influential = reaction_lists[2]
    
    #write_list_to_file(essential)
    #write_list_to_file(no_effect)
    write_list_to_file(influential)
    
    
