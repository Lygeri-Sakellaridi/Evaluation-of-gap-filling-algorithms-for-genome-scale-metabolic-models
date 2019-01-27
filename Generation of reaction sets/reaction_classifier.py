#!/usr/bin/env python3
"""
Script to generate reaction sets that will be used for evaluation of gap-fillers.

First, the script classifies a model's reactions according to their effect on growth.
The reaction files used as input are the result of single reaction deletion analysis. 

Afterwards, reaction sets are generated using the classified reaction lists as input.

Finally, the generated sets are written to their corresponding output files.

Author: Lily Sakellaridi
"""

from sys import argv, exit
from random import sample
import os

def reaction_classifier(lines):
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
                
    reaction_types = ['essential', 'no_effect', 'influential']
    reaction_lists = [essential_reactions, no_effect_reactions, influential_reactions]
    reaction_types_dict = dict(zip(reaction_types, reaction_lists))
    return reaction_types_dict
    
def create_output_directory_tree(model_name):
    """
    Creates the directory tree that will store the results in appropriately named directories.
    
    model_name: the model's name; str
    
    The hierarchy is: all sets/model_name/set_size/set_type. In every step,
    the script performs a check for directory existence.
    """
    all_isdir = os.path.isdir("all_sets")
    if not all_isdir:
        os.mkdir("all_sets")
    else:
        model_isdir = os.path.isdir("all_sets/" + model_name)
        if not model_isdir:
            os.mkdir("all_sets/" + model_name)
            
        size5_isdir = os.path.isdir("all_sets/" + model_name + "/size5")
        size10_isdir = os.path.isdir("all_sets/" + model_name + "/size10")
            
        if not size5_isdir:
            os.mkdir("all_sets/" + model_name + "/size5")
        
        essential_isdir = os.path.isdir("all_sets/" + model_name + "/size5/" + "essential")
        if not essential_isdir:
            os.mkdir("all_sets/" + model_name + "/size5/" + "essential")
            
        influential_isdir = os.path.isdir("all_sets/" + model_name + "/size5/" + "influential")
        if not influential_isdir:
            os.mkdir("all_sets/" + model_name + "/size5/" + "influential")
            
        noeffect_isdir = os.path.isdir("all_sets/" + model_name + "/size5/" + "no_effect")
        if not noeffect_isdir:
            os.mkdir("all_sets/" + model_name + "/size5/" + "no_effect")
        
        if not size10_isdir:
            os.mkdir("all_sets/" + model_name + "/size10")
        
        essential_isdir = os.path.isdir("all_sets/" + model_name + "/size10/" + "essential")
        if not essential_isdir:
            os.mkdir("all_sets/" + model_name + "/size10/" + "essential")
            
        influential_isdir = os.path.isdir("all_sets/" + model_name + "/size10/" + "influential")
        if not influential_isdir:
            os.mkdir("all_sets/" + model_name + "/size10/" + "influential")
            
        noeffect_isdir = os.path.isdir("all_sets/" + model_name + "/size10/" + "no_effect")
        if not noeffect_isdir:
            os.mkdir("all_sets/" + model_name + "/size10/" + "no_effect")
            
    
def generate_reaction_sets(set_type_name, set_size, reaction_types_dict):
    """
    Generates reaction sets.
    """
    all_sets = []
    set_type = reaction_types_dict[set_type_name]
    for i in range(10):
        random_set = sample(set_type, set_size)
        all_sets.append(random_set)
        
    return all_sets
    
def write_output_to_file(my_set, set_type_name, set_size):
    """
    Writes the output of each generated set to the appropriate file.
    """
    pass
    
if __name__ == "__main__":
    
    # Step 1: Take the input file and the max_growth value from the command line
    if len(argv) != 4:
        print("Please give me the following arguments in the order specified:")
        print("1) the .csv file containing the results of single reaction analysis.")
        print("2) max_growth: float; the maximum growth of the model you're examining.")
        print("3) the model name, eg iJO1366.")
        exit(0)
        
    infile, max_growth, model_name = argv[1], float(argv[2]), argv[3]
    
        
    with open(infile) as inf:
        lines = inf.readlines()
        
    #print(lines)
        
    # Step 2: Classify the reactions and store the result in a dictionary.
    # keys: names of th reaction types; str
    # values: the reactions belonging to each type; list
    
    reaction_types_dict = reaction_classifier(lines)
    #for k, v in reaction_types_dict.items():
    #    print(k, len(v))
    #print(infeasible_reactions)
    
    #print(len(essential_reactions))
    #print(len(no_effect_reactions))
    #print(len(influential_reactions))
    #print(len(infeasible_reactions))
    
    # Step 3: Create directory tree
    create_output_directory_tree(model_name)
    
    # Step 4: Generate reaction sets:
    # from each reaction type, take sets of size 5 and 10,
    # with 10 replicates within each.
    essentials = generate_reaction_sets('essential', 5, reaction_types_dict)
    with open("test", "w") as test:
        for essential in essentials:
            essential = " ".join(essential)
            print(essential, type(essential))
            test.write(essential + "\n")
    
    
    
    
