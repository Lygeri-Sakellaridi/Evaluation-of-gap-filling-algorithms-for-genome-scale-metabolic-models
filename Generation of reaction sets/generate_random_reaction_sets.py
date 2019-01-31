#!/usr/bin/env python3
"""
Script to generate random sets of reactions to remove. The input is a space-separated
text file that contains all reactions of a specifi type, ie essential.

Author: Lily Sakellaridi
"""

from sys import argv, exit
from random import sample

def generate_random_set(reaction_file, set_size):
    """
    Generates a random reaction set of specified size.
    """
    with open(reaction_file) as rf:
        reactions = rf.readline().rstrip().split(' ')
        random_set = sample(reactions, set_size)
        return random_set
        

if __name__=="__main__":
    # Step 1: Get the input arguments.
    if len(argv) != 3:
        print("The first argument is the text file that contains all reactions of a specific type.")
        print("The second argument is the set size (int).")
        exit(0)
        
    reaction_file = argv[1]
    #print(reaction_file)
    
    set_size = int(argv[2])
    #print(set_size, type(set_size))
    
    # Step 2: Generate 10 random sets.
    
            
    with open("random_reaction_set", "w") as out:
        for i in range(10):
            random_set = generate_random_set(reaction_file, set_size)
            random_set = " ".join(random_set)
            out.write(random_set + "\n")

