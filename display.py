# Kaitlyn Stumpf                                                                        
# CSC334, Spring 2015                                                               
# 3/12/2015                                                                                         
# Midterm: Part Two, Visualizing

import sys

def display(inFilePath):
    pdb_name = inFilePath[-8:-4]
    file_name = pdb_name + "_DISPLAY_JMolScript.scr"
    output_file = open(file_name, "w")

    load = "load " + inFilePath + "; delay 0.5;"
    echo = 'set echo top left; echo "Here is what the protein ' + pdb_name + ' is made of:"; delay 1;'
    chain = "echo 'chains'; color chains; delay 1; select all; color Jmol; delay 0.5;"
    water = "echo 'water'; display water; delay 1; display all; delay 0.5;"
    ligand = "echo 'ligand'; display ligand; delay 1; display all; delay 0.5;"
    hetatm = "echo 'hetatm'; display hetero; delay 1; display all; delay 0.5;"
    amino = "echo 'amino'; select amino; color amino; delay 1; select all; color Jmol;"
    end = "echo 'The end. Close jmol when ready to continue.'"
    
    lines = [load, echo, chain, ligand, hetatm, amino, end]
    for line in lines:
        output_file.write(line)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) < 1):
        print("Please enter a pdb file path.")
    display(sys.argv[1])



