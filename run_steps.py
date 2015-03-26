# Kaitlyn Stumpf
# CSC334, Spring 2015
# 3/11/2015
# Midterm1, Pipeline
# X-Ray, Protein

# This code takes a path to a pdb file. It then does the following:

# Step 1: Runs isXray.py to determine if the pdb file's experimental method was X-Ray. If it was,
# returns a data.txt file about the pdb file.

# Step 2: Runs extract.py and extracts the molecule type & specific ids/names requested by the user.
# Can return one, several, or all of the requested molecule type.

# Step 3: Runs prune.py and writes a new pdb file without solvent or "something else" HETATM lines.

# Step 4: Runs writeHydScript.py and writes a personalized "remove hydrogens" jmol script for the pdb.

# Step 5: Runs JMol, loads the newly written script, visualizes the pdb with hydrogens,
# and creates a ###_H.pdb file that contains hydrogens and renumbered ATOM lines and reorganized CONECT lines.

# Step 6: Visualizes the protein. Flashes through chains, water, ligands, hetatms, and amino acids. 
# This step was moved between steps 1 and 2.

# Step 7. Creates a script for computing bonds and then loads this script in JMol. The script creates a text file containing all of the bonds. 
# Then reformats the bonds so that they are in pairs, with each pair written on its own line.

# Step 8-9. Creates scripts for extracting the ligand with and without hydrogens added, and then runs these scripts in JMol.

# Attempted Code:
# Step 10. Creates a script for extracting specifically requested chains using JMol. The script creates a text file containing all of the chains requested.
# (Couldn't get this to work in the time allotted.)


# Import the subprocess module.
# this is used to run external programs from inside python
import subprocess

# Import the os.path module, which is used to check if a file exists
# and the sys module for interacting with the system:
import os.path, sys


def main():
    # First ask the user for a path to a file
    inFilePath = raw_input("Please enter a path to an input PDB file (e.g. /Users/josephfourier/Documents/my_file.txt): ")

    # Make sure that the file exists and continue to ask the user for a file
    # until they provide a legal file
    while not os.path.isfile(inFilePath):
        print("The file you entered (" + inFilePath + ") does not exist.")
        inFilePath = raw_input("Please enter a path to an input PDB file (or type 'q' to quit): ")
        if (inFilePath == 'q'):
            print("Exiting.")
            sys.exit(0) # exit the system if the user types q

    outFileName= inFilePath[-8:-4] + "_DATA.txt" # If inFilePath was "./1HVR.pdb", would capture "1HVR"

    runXray(inFilePath, outFileName)
    writeDisplayScript(inFilePath)
    runJMolScript(inFilePath, 'D')
    runExtract(inFilePath, outFileName)
    runPrune(inFilePath)

    writeHydScript(inFilePath)
    runJMolScript(inFilePath, 'H')

    writeBondScript(inFilePath)
    modifyBondScript(inFilePath)

    writeLigandScript(inFilePath)
    runJMolScript(inFilePath, 'L')

    writeLigandHydScript(inFilePath)
    runJMolScript(inFilePath, 'LH')

    #writeChainScript(inFilePath)

    print("\tDone. Now exiting.")

'''
 STEP 1: Run isXray.py
'''
def runXray(inFilePath, outFileName):
    xRay = ["python", "isXray.py", inFilePath, outFileName]

    subprocess.call(xRay)

    print("\tCreated data.txt file for " + inFilePath[-8:-4])
    print
    inBetweenFunctions()


'''
 Step 2: Run python script to extract the files requested by the user.
'''
def runExtract(inFilePath, outFileName):
    print("Will extract the information requested by the user.")

    # Next we run our python script extract.py.
    extract = ["python", "extract.py", inFilePath, outFileName]

    subprocess.call(extract) #call the python script

    print("\tExtracted the information requested for " + inFilePath[-8:-4])
    print
    inBetweenFunctions()


'''
Step 3: Run python script to prune the solvent and 'something else' from the pdb file.
'''
def runPrune(inFilePath):
    print("Will prune the pdb file and return one without solvent and 'something else' HETATM and lines.")
    
    # Next we run our python script prune.py
    prune = ["python", "prune.py", inFilePath]

    subprocess.call(prune)

    print("\tPruned the pdb file " + inFilePath[-8:-4] + " of its HETATM solvent lines and 'something else'.")
    print
    inBetweenFunctions()


'''
Step 4: Run the python program to create the jmol script that will handle hydrogen placement.
'''
def writeHydScript(inFilePath):
    print("Will run a python program to create the jmol script that will handle h-placement.")

    writeScript = ["python", "writeHydScript.py", inFilePath]
    subprocess.call(writeScript)

    print("\tCreated a jmol script for placing hydrogens on " + inFilePath[-8:-4] + ".")
    print

    inBetweenFunctions()


'''
Step 7: Visualizes the protein. Flashes through chains, water, ligands, hetatms, and amino acids.
'''
def writeDisplayScript(inFilePath):
    print("Will run a python program to create the jmol script that will handle visualization of protein parts.")
    
    writeScript = ["python", "display.py", inFilePath]
    subprocess.call(writeScript)

    print("\tCreated a jmol script for visualizing the parts of " + inFilePath[-8:-4] + ".")
    print

    inBetweenFunctions()


'''
Step 5: Runs an external program (JMol) to place all the hydrogen atoms and fix the atom numbering.
Load JMol as a visualizer to see the newly placed hydrogens.
'''
def runJMolScript(inFilePath, scriptType):
    inMessage = ''
    outMessage = ''
    jmolScript = None

    if scriptType == "H":
        jmolScript = inFilePath[-8:-4] + "_H_JMolScript.scr"
        inMessage = 'Will run JMol in order to place all the hydrogen atoms and fix the atom numbering.'
        outMessage = '\tCreated a new PDB file with hydrogens, called: ' + inFilePath[-8:-4] + '_H.pdb'
#    elif scriptType == "B":
#        jmolScript = inFilePath[-8:-4] + "_BOND_JMolScript.scr"
#        inMessage = 'Will run JMol in order to compute the bonds.'
#        outMessage = '\tCreated a PDB-formatted file with ATOM and CONECT lines for atoms and bonds.'
    elif scriptType == "L":
        jmolScript = inFilePath[-8:-4] + "_LIGAND_JMolScript.scr"
        inMessage = 'Will run JMol in order to extract the ligands.'
        outMessage = '\tCreated a PDB-formatted file with ligands.'
    elif scriptType == "LH":
        jmolScript = inFilePath[-8:-4] + "_LIGANDHYD_JMolScript.scr"
        inMessage = 'Will run JMol in order to add hydrogens & extract the ligands.'
        outMessage = '\tCreated a PDB-formatted file with ligands (after adding hydrogens).'
    elif scriptType == "D":
        jmolScript = inFilePath[-8:-4] + "_DISPLAY_JMolScript.scr"
        inMessage = 'Will run JMol and display the different parts of the protein.'
        outMessage = '\tProtein has been visualized.'
    elif scriptType == "C":
        jmolScript = inFilePath[-8:-4] + "_CHAIN_JMolScript.scr"
        inMessage = 'Will run JMol and extract the requested chain.'
        outMessage = '\tThe chain has been extracted.'

    print(inMessage)
    jmolCommand = ["java", "-jar", "Jmol.jar", "-is", jmolScript]
    subprocess.call(jmolCommand)

    print(outMessage)
    print

    inBetweenFunctions()


'''
Step 6: Create a JMol script to compute bonds and produce a PDB-formatted file with ATOM and CONECT lines.
This will give us important data about atoms and bonds. 
'''
def writeBondScript(inFilePath):
    print("Will run a python program to create the jmol script that will compute bonds.")

    writeScript = ["python", "writeBondScript.py", inFilePath]
    subprocess.call(writeScript)
    pdb_name = inFilePath[-8:-4]
#    scriptName = inFilePath[-8:-4] + "_BOND_JMolScript.scr"


    line = "load " + inFilePath + "; x=getProperty(\"bondInfo[SELECT atom* WHERE type='single'][SELECT atomno]\"); print x;"

    jmolCommand = ["java", "-jar", "./JmolData.jar", "-ij", line] #scriptName]
    


    outFilePath = inFilePath[-8:-4] + "_BOND.txt"
    outFile = open(outFilePath, 'w')
    subprocess.call(jmolCommand, stdout=outFile)
    outFile.close()

    print("\tCreated a txt file containing the bonds of " + inFilePath[-8:-4] + ".")
    print

    inBetweenFunctions()


'''
Step 12: Takes the text file of bonds and organizes them into pairs, with each pair on a separate line.
Writes these bond pairs to a new text file named ####_BOND_PAIRS.txt.
'''
def modifyBondScript(inFilePath):
    print("Will create a text file containing bond pairs.")
    old_bond_name = inFilePath[-8:-4] + "_BOND.txt"
    new_bond_name = inFilePath[-8:-4] + "_BOND_PAIRS.txt"
    
    old_file = open(old_bond_name, "r")
    new_file = open(new_bond_name, "w")
    
    lines = old_file.readlines()
    
    for i in range(0, len(lines) - 1, 2):
        newLine = lines[i].rstrip() + " " + lines[i+1]
        new_file.write(newLine)

    old_file.close()
    new_file.close()

    print("\tCreated a txt file containing the bond pairs of " + inFilePath[-8:-4] + ".")
    print
    
    inBetweenFunctions()

'''                                                                                                     
Step 8: Create a JMol script to color the ligand white and extract its ATOM and bond lines.
This will give us important data about the ligand's atoms and bonds.                          
'''
def writeLigandScript(inFilePath):
    print("Will run a python program to create the jmol script that will compute ligands.")

    writeScript = ["python", "writeLigandScript.py", inFilePath]
    subprocess.call(writeScript)

    print("\tCreated a jmol script for extracting the ligands of " + inFilePath[-8:-4] + ".")
    print

    inBetweenFunctions()


'''                                                                                                   
Step 9: Create a JMol script to color the ligand white and extract its ATOM and bond lines.
This also creates the hydrogens.
This will give us important data about atoms and bonds.                                           
'''
def writeLigandHydScript(inFilePath):
    print("Will run a python program to create the jmol script that will add hydrogens and extract the ligand.")

    writeScript = ["python", "writeLigandHydScript.py", inFilePath]
    subprocess.call(writeScript)

    print("\tCreated a jmol script for extracting the ligands/bonds of " + inFilePath[-8:-4] + " with hydrogens added.")
    print

    inBetweenFunctions()


'''                                                                            
Step 11: Create a JMol script to color the chain white and extract its ATOM and bond lines. 
This will give us important data about the chain's atoms and bonds.                        
'''
def writeChainScript(inFilePath):
    file_name = inFilePath[-8:-4] + "_DATA.txt"
    pdb_file = open(file_name, "r")
    lines = pdb_file.readlines()
    chain_list = lines[-5].split()[1:]
    print("Will run a python program to create the jmol script that will extract the requested chain.")
    print("Chain List: ", chain_list)
    print("Please pick and type the name of a chain from the list above. ex. Input: A")
    print("If you want all chains, input: All")
    print("For multiple chains, input with spaces in between. ex. Input: A B ")
    print
    chains = None
    chain_id = raw_input("Input: ")
    if chain_id == 'All':
        chains = chain_list
    else:
        chains = chain_id.split()

#    writeScript = ["python", "writeChainScript.py", inFilePath, chains]
#    subprocess.call(writeScript)

#    scriptName = inFilePath[-8:-4] + "_CHAIN_JMolScript.scr"
    line = "load " + inFilePath + ";"
    #select ligand; color white; write PDB " + pdb_name + "_Ligand.pdb";

    for chain in chain_list:
        line += "select : " + chain + "; color white; delay 1; print " + chain + "; select all; color Jmol; delay 0.5;"
    print(line)

    jmolCommand = ["java", "-jar", "JmolData.jar", "-ij", line]

    outFilePath = inFilePath[-8:-4] + "_CHAIN.txt"
    outFile = open(outFilePath, 'w')
    subprocess.call(jmolCommand, stdout=outFile)
    outFile.close()

    print("\tCreated a txt file containing the bonds of " + inFilePath[-8:-4] + ".")
    print

    inBetweenFunctions()


'''
Determines whether the user wants to continue or quit.
'''
def inBetweenFunctions():
    resp = raw_input("Press enter to continue or q to quit: ")
    if (resp == "q"):
        print("\tBye.")
        sys.exit(0)
    print("\n")

if __name__ == "__main__":
    main()
