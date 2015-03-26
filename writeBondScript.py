# Kaitlyn Stumpf                                                                       
# CSC334, Spring 2015                                                               
# 3/12/2015                                                                            
# Midterm: Part Two, Computing Bonds
# Doesn't quite work properly. If changed line = line, everything would be great.

import sys

def writeBondScript(inFilePath):
    pdb_name = inFilePath[-8:-4]
    file_name = pdb_name + "_BOND_JMolScript.scr"
    output_file = open(file_name, "w")

    line = "load " + inFilePath + "; x=getProperty(\"bondInfo[SELECT atom* WHERE type='single'][SELECT atomno]\"); print x;"
    output_file.write(line)
    output_file.close()


if __name__ == '__main__':
    if (len(sys.argv) < 1):
        print("Please enter a pdb file path.")
    writeBondScript(sys.argv[1])

