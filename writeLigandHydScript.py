# Kaitlyn Stumpf                                       
# CSC334, Spring 2015                       
# 3/12/2015                                                               
# Midterm: Part Three, Extracting the Ligand after adding Hydrogens

import sys

def writeLigandHydScript(inFilePath):
    pdb_name = inFilePath[-8:-4]
    file_name = pdb_name + "_LIGANDHYD_JMolScript.scr"
    output_file = open(file_name, "w")

    line = "load " + inFilePath + "; set echo top left; echo 'Here is " + pdb_name + "'s ligand, colored white. Close JMol when ready to continue.'; set pdbAddHydrogens TRUE; calculate hydrogens; select ligand; color white; write PDB " + pdb_name + "_LigandH.pdb";

    output_file.write(line)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) < 1):
        print("Please enter a pdb file path.")
    writeLigandHydScript(sys.argv[1])
