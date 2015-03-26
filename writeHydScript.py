# Kaitlyn Stumpf
# CSC334, Spring 2015
# 3/11/2015
# Midterm: Part One, Placing Hydrogens

import sys

def writeHydScript(inFilePath):
    pdb_name = inFilePath[-8:-4]
    file_name = pdb_name + "_H_JMolScript.scr"
    output_file = open(file_name, "w")
    
    line = "load " + inFilePath + "; set echo top left; echo 'Here is " + pdb_name + " with hydrogens. Close JMol when ready to continue.'; set pdbAddHydrogens TRUE; calculate hydrogens; select *; write PDB " + inFilePath[-8:-4] + "_H.pdb;"

    output_file.write(line)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) < 1):
        print("Please enter a pdb file path.")
    writeHydScript(sys.argv[1])
