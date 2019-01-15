#!/usr/bin/env python3
"""
Script to perform single reaction deletion anlysis on a model and write the
output to a .csv file.

Author: Lily Sakellaridi
"""

from pandas import DataFrame
from time import time
import os
from sys import argv, exit
import cobra.test
from cobra.flux_analysis import single_reaction_deletion

# Step 1: Take the model as input from the command line.

if len(argv) != 2:
    print("Please provide a genome scale model in sbml format.")
    exit(0)
    
model_name = argv[1]
#print(model_name)

# Step 2: Read in the model.

model = cobra.io.read_sbml_model(model_name)
#print(model.summary())

# Perform single reaction deletion analysis
result = single_reaction_deletion(model)
#print(result)

# Write the result to a csv file.
out_file = model_name + "_srd_result"
print(out_file)
isfile = os.path.isfile(out_file)
print(isfile)

if isfile:
    print("The result file already exists in the current directory; aborting process.")
    exit(0)
    
result.to_csv(out_file)

