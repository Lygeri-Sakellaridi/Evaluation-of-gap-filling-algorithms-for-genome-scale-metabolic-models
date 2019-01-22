#!/usr/bin/env python3
"""
Parse the reactions.txt file from BiGG into a database compatible with cobratoolbox.
Author: Lily Sakellaridi
"""

from sys import argv, exit
import os

def read_input(bigg_file):
    """
    Read the contents of bigg_reactions and convert into open line format.
    
    bigg_file: tab-separated file with columns: rxn_id, rxn_formula, model_list,
    database_links, old_big_ids
    """
    with open(bigg_file) as bf:
        lines = bf.readlines()
        
    return lines

def parse_database(bigg_lines):
    """
    Parse the bigg database in a dictionary with keys: reaction identifiers, values: reaction formulas.
    
    bigg_lines: lines of tab-separated file with columns: rxn_id, rxn_formula, model_list,
    database_links, old_big_ids
    """
    
    bigg_dict = {}
    for line in bigg_lines[1:]:
        line = line.split("\t")
        bigg_id = line[0]
        rxn_formula = line[2]
        rxn_formula = rxn_formula.replace('-', '=')
        if bigg_id in bigg_dict.keys():
            print("You have duplicate keys. Check your input file: bigg_ids must be unique. Aborting process.")
            exit(0)
        else:
            bigg_dict[bigg_id] = rxn_formula
    return bigg_dict
        
    
    
def write_output(bigg_dict):
    """
    Writes bigg_dict into a database that can be used with cobratoolbox.
    
    bigg_dict: dictionary where keys: bigg ids, values: reaction formulas
    """
    exists = os.path.isfile("bigg_reaction.lst")
    
    if exists:
        print("The file bigg_reaction.lst exists already in the specified path. Aborting process.")
        exit(0)
        
    with open("bigg_reaction.lst", "w") as out_file:
        for bigg_id, rxn_formula in bigg_dict.items():
            row = bigg_id + ": " + rxn_formula + "\n"
            out_file.write(row)
        
    
    
if __name__=="__main__":
    # Step 1: Retrieve the input file from the command line
    
    if len(argv) != 2:
        print("Please pass the bigg_models_reactions.txt file as a command line argument.")
        exit(0)
        
    bigg_file = argv[1]
    
    # Step 2: Read the file's contents
    
    bigg_lines = read_input(bigg_file)
    
    # Step 3: Convert the contents of bigg_reactions.txt into a dictionary
    # where keys: identifiers, and values: formulas.
    bigg_dict = parse_database(bigg_lines)
    
    # Step 4: Write the output to .lst format for use with cobratoolbox.
    write_output(bigg_dict)
