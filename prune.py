# Kaitlyn Stumpf
# CSC334, Spring 2015
# 3/11/2015
# Midterm Part 1: Pruning

# This script checks if the file contains hetero atoms (HETATM). 
# If so, check if it contains water (the solvent). If so, the water is eliminated. 

# Input: file_name, from the command line. 
# Output: .pdb file containing all but the HETATM water lines and "something else", titled Pruned_####.pdb.
# NOTE: PRESERVES LIGAND AND NONSTANDARD RESIDUE LINES.

# This .pdb file will be pipelined into another part of the project.

import sys

def prune(file_name):
    pdb_file = open(file_name, "r")

    has_found_hetatm = False

    # Check if file contains hetero atoms.
    for line in pdb_file:
        if (line[0:6] == "HETATM" and has_found_hetatm != True):
            has_found_hetatm = True
            break
    pdb_file.close()

    # If there are hetatms, check for water and copy all lines except those hetatm water lines.
    if has_found_hetatm == True:
        pdb_file = open(file_name, "r")
        new_pdb_name = file_name[-8:-4] + "_Pruned.pdb"
        new_pdb = open(new_pdb_name, "w")

        resName = None
        # Then prune water and "something else" using resname.
        pdb_file = open(file_name, "r")
        for line in pdb_file:
            if line[0:6] == "HETATM" or line[0:6] == "ANISOU":
                if line.split()[4].isdigit():
                    resName = line.split()[2][-4:]
                else:
                    resName = line.split()[3]
                # If not water and not something else
                # print("resname", resName, len(resName), resName != "HOH")
                if (resName != "HOH" and resName != "AHOH" and resName != "BHOH") and (len(resName) == 3):
                    new_pdb.write(line)
            # If not hetatm line
            else:
                new_pdb.write(line)
        new_pdb.close()
        pdb_file.close()

    # Could also prune "something else" here, if I have the time.

if __name__ == '__main__':
    if (len(sys.argv[1]) < 1):
        print("Please enter a pdb file name.")
    else:
        prune(sys.argv[1])
