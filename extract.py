# Kaitlyn Stumpf
# CSC334, Spring 2015
# 3/11/2015
# Midterm: Part One: Extract

# Extract.py 

import sys
'''
The main function of extract.py takes a file_name and an outFileName, and from there reconstructs the chains, ligands,
nsr, and solvent names in the pdb. Ideally, were subprocess's returncode to return a function value and not a 0 or 1, 
this molecule_info could just be pipelined in from xRay.py.

A list of the types of molecules present in the pdb is given to the user.

Depending on whether the user chooses a chain, ligand, nonstandard res, or solvent, a different function will be called,
asking the user if they want one or multiple or all of the type they named. 
Their request will then be extracted into a txt file(s).
'''
def main(file_name, outFileName):
    # Create various lists of chains, ligands, nsr, and solvents, for use depending on what the user wants to extract.
    # Will be passed into the various extraction functions.
    # Ideally this would be pipelined straight from xRay.py, but subprocess cannot return the value of the func it runs.
    # subprocess can return only 0 or 1, as a representation of whether the process ran successfully.
    output_file = open(outFileName, "r")
    lines = output_file.readlines()
    chain_list = lines[-5].split()[1:]
    ligand_list = lines[-4].split()[1:]
    nsr_list = lines[-3].split()[2:]
    solvent_list = lines[-2].split()[1:]
    other_list = lines[-1].split()[1:]
    molecule_info = [chain_list, ligand_list, nsr_list, solvent_list]
    
    # Create a list of the molecule types in the pdb file.
    molecule_types = []
    if len(chain_list) > 0:
        molecule_types.append("Chain")
    if len(ligand_list) > 0:
        molecule_types.append("Ligand")
    if len(nsr_list) > 0:
        molecule_types.append("Nonstandard Residue")
    if len(solvent_list) > 0:
        molecule_types.append("Solvent")
    if len(other_list) > 0:
        molecule_types.append("Something Else")

    # Print a GUI listing Molecule Types and asking the user to select one.
    print
    print "Molecule Types Available:", molecule_types
    print
    print("Please enter a molecule type from the ones listed above, and it will be extracted.")
    print("For example. Input: Nonstandard Residue")
    print
    molecule = raw_input("Input: ")

# Keep in case I find a way to pipeline molecule_info in from isXray.py
#    chain_list = molecule_info[0]
#    ligand_list = molecule_info[1]
#    nonstandardres_list = molecule_info[2]
#    solvent_list = molecule_info[3]
#    other_list = molecule_info[4]

    # Determines which type of extraction must occur, and calls the appropriate function.
    if molecule == "Chain":
        chain(file_name, chain_list)
    elif molecule == "Solvent":
        solvent(file_name, solvent_list)
    elif molecule == "Ligand":
        ligand(file_name, ligand_list)
    elif molecule == "Nonstandard Residue":
        nonstandardres(file_name, nsr_list)
    elif molecule == "Something Else":
        somethingElse(file_name, other_list)

'''
Given a pdb file_name and a list of the solvents in the file,
it prompts the user for which solvent(s) to extract.
It then calls the function to extract those solvents.
'''
def solvent(file_name, solvent_list):
    print
    print("SOLVENT LIST:", solvent_list)
    print("Please pick and type the name of a solvent from the list above. ex. Input: HOH")
    print("If you want all solvents, input: All")
    print("For multiple solvents, enter them with a space in between each: HOH AHOH")
    print
    solvent_id = raw_input("Input: ")
    if solvent_id == 'All':
        extractSolvents(file_name, solvent_list)
    else:
        solvents = solvent_id.split()
        extractSolvents(file_name, solvents)
    

'''
Given a pdb file_name and a list of the solvents the user wants extracted,
it extracts each solvent into a separate .txt file that is appropriately named.
'''
def extractSolvents(file_name, solvent_list):
    for solvent in solvent_list:
        pdb_file = open(file_name)
        # For each solvent, create a file and write that solvent's hetatms to it.
        new_file_name = file_name[0:-4] + "_Solvent_" + solvent + ".txt"
        output_file = open(new_file_name, "w")

        resName = None
        for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
            if line[0:6] == "HETATM" or line[0:6] == "ANISOU":
                if line.split()[4].isdigit():
                    resName = line.split()[2][-4:]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                else:
                    resName = line.split()[3]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]

                # Gets the 3rd piece of data, the solvent name, from the HETATM records.
                solventID = str(resName.strip())
                # If the solventID matches solvent, put the hetatm line in the file.
                if solventID == solvent:
                    output_file.write(line)
        output_file.close()
        pdb_file.close()


'''
Given a pdb file_name and a list of the pdb file's ligands,
it prompts the user for which ligand(s) to extract.
It then calls the function to extract those ligands.
'''
def ligand(file_name, ligand_list):
    print
    print("LIGAND LIST:", ligand_list)
    print("Please pick and type the name of a ligand from the list above. ex. Input: XK2")
    print("If you want all ligands, input: All")
    print("For multiple ligands, enter them with a space in between each: XK2 VW3")
    print
    ligand_id = raw_input("Input: ")
    if ligand_id == "All":
        extractLigands(file_name, ligand_list)
    else:
        ligands = ligand_id.split()
        extractLigands(file_name, ligands)
    

'''
Given a pdb file_name and a list of the ligands to extract,
each ligand is extracted into a separate .txt file that is appropriately named.
'''
def extractLigands(file_name, ligand_list):
    for ligand in ligand_list:
        pdb_file = open(file_name)
        # For each ligand, create a file and write that chain's hetatms to it.
        new_file_name = file_name[0:-4] + "_Ligand_" + ligand + ".txt"
        output_file = open(new_file_name, "w")

        resName = None
        for line in pdb_file:
            if line[0:6] == 'HETATM' or line[0:6] == "ANISOU":
                # Sometimes the second and third lines have no space between them.     
                # This deals with that.                                                   
                if line.split()[4].isdigit():
                    resName = line.split()[2][-4:]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                else:
                    resName = line.split()[3]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                # Gets the 3rd piece of data, the ligand name, from the HETATM records.
                ligandID = resName.strip()
                # If the ligandID matches ligand, put the hetatm line in the file.
                if ligandID == ligand:
                    output_file.write(line)
        output_file.close()
        pdb_file.close()


'''
Given a pdb file_name and a list of the pdb's nonstandard residues,
it prompts the user for which nonstandard residue(s) to extract.
It then calls the function to extract those residues.
'''
def nonstandardres(file_name, nsr_list):
    print
    print("NONSTANDARD RESIDUE LIST:", nsr_list)
    print("Please pick and type the name of a nonstandard residue from the list above. ex. Input: CSO")
    print("If you want all nonstandard residues, input: All")
    print("For multiple nonstandard residues, enter them with a space in between each: CSO FLI")
    print
    nsr_id = raw_input("Input: ")
    if nsr_id == "All":
        extractNSR(file_name, nsr_list)
    else:
        nsr = nsr_id.split()
        extractNSR(file_name, nsr)


'''
Given a pdb file_name and a list of nonstandard residues that the user wants extracted,
each nonstandard residue is extracted into a separate .txt file that is appropriately named.
'''
def extractNSR(file_name, nsr_list):
    for nsr in nsr_list:
        pdb_file = open(file_name)
        # For each nonstandard residue, create a file and write that chain's hetatms to it.              
        new_file_name = file_name[0:-4] + "_NonstandardRes_" + nsr + ".txt"
        output_file = open(new_file_name, "w")

        resName = None
        for line in pdb_file:
            if line[0:6] == 'HETATM' or line[0:6] == "ANISOU":
                # Sometimes the second and third lines have no space between them.                     
                # This deals with that.                                                                        
                if line.split()[4].isdigit():
                    resName = line.split()[2][-4:]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                else:
                    resName = line.split()[3]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                # Gets the 3rd piece of data, the nsr name, from the HETATM records.
                nsrID = resName.strip()
                # If the nsrID matches nsr, put the hetatm line in the file.
                if nsrID == nsr:
                    output_file.write(line)
        output_file.close()
        pdb_file.close()



'''
Given a pdb file_name and a list of the pdb's "something else" lines,
it prompts the user for which "something else" to extract.
It then calls the function to extract those "elses".
'''
def somethingElse(file_name, somethingelse_list):
    print
    print("SOMETHING ELSE LIST:", somethingelse_list)
    print("Please pick and type the name of a 'something else' from the list above. ex. Input: CSO")
    print("If you want all, input: All")
    print("For multiple, enter them with a space in between each: CSO FLI")
    print
    somethingelse_id = raw_input("Input: ")
    if somethingelse_id == "All":
        extractSE(file_name, somethingelse_list)
    else:
        somethingelse = somethingelse_id.split()
        extractSE(file_name, somethingelse)


'''
Given a pdb file_name and a list of the "something else" that the user wants extracted,
each "something else" is extracted into a separate .txt file that is appropriately named.
'''
def extractSE(file_name, se_list):
    for se in se_list:
        pdb_file = open(file_name)
        # For each nonstandard residue, create a file and write that chain's hetatms to it.
        new_file_name = file_name[0:-4] + "_SomethingElse_" + se + ".txt"
        output_file = open(new_file_name, "w")

        resName = None
        for line in pdb_file:
            if line[0:6] == 'HETATM' or line[0:6] == "ANISOU":
                # Sometimes the second and third lines have no space between them. 
                # This deals with that.         
                if line.split()[4].isdigit():
                    resName = line.split()[2][-4:]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:]
                else:
                    resName = line.split()[3]
                    if resName[0] == "A" or resName[0] == "B":
                        resName = resName[1:] 
                # Gets the 3rd piece of data, the se name, from the HETATM records.
                seID = resName.strip()
                # If the seID matches se, put the hetatm line in the file.
                if seID == se:
                    output_file.write(line)
        output_file.close()
        pdb_file.close()


# Removed test whether x-ray, because this is done earlier in the pipeline.
'''
Given a pdb file_name and a list of the pdb's chains,
it prompts the user for which chain(s) they want to extract.
It then calls the function to extract these chains.
'''
def chain(file_name, chain_list):
    print
    print("CHAIN LIST:", chain_list)
    print("Please pick and type the name of a chain from the list above. ex. Input: A")
    print("If you want all chains, input: All")
    print("For multiple chains, input with spaces in between. ex. Input: A B ")
    print
    chain_id = raw_input("Input: ")
    if chain_id == 'All':
        extractChains(file_name, chain_list)
    else:
        chains = chain_id.split()
        extractChains(file_name, chains)


'''
Given a pdb file and a list of chains that the user wants to extract,
it extracts each chain into a separate .txt file that is appropriately named.
'''
def extractChains(file_name, chain_list):
    # Open pdb file
    for chain in chain_list:
        pdb_file = open(file_name)
        # For each chain, create a file and write that chain's atoms to it.
        new_file_name = file_name[0:-4] + "_Chain_" + str(chain) + ".txt"
        output_file = open(new_file_name, "w")

        chainID1 = None
        for line in pdb_file:
            if line[0:4] == 'ATOM' or line[0:6] == "HETATM" or line[0:6] == "ANISOU":
                # Sometimes the second and third lines have no space between them.
                # This deals with that.                                                   
                if line.split()[4].isdigit():
                    chainID1 = line.split()[3]
                else:
                    chainID1 = line.split()[4]                
                # Gets the 4th piece of data, the chainID, from the ATOM records.
                chainID = str(chainID1.strip())
                # If the chainID matches chain, put the atom line in the file.
                if chainID == chain:
                    output_file.write(line)
        output_file.close()
        pdb_file.close()

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Please enter a pdb file name and data.txt file.")
    else:
        main(sys.argv[1], sys.argv[2])
