# Kaitlyn Stumpf
# CSC334, Spring 2015
# 3/11/2015
# Midterm: Part One

# Start with a PDB file. PDB file is passed into the main function.
# Run python code that tells its experimental method. 
# If it is X-ray, returns True. Else, returns False.
# If it is X-ray, the following is collected:
#     The kinds of molecules present in the pdb file.
#     A classification of each hetatm line. (Either nonstandard res, ligand, etc)
#     A summary of all chains, ligands, nonstandard residues, solvents, or other in the pdb file.

# Ligands are not in SEQRES and have a chainID and a resName of length 3.
# Nonstandard residues are in SEQRES but not one of the 22 amino acids.
# Solvent is assumed to be HOH.
# Other is a HETATM that fits none of the above categories.


import sys
'''
The main function executes isXray() to test if the pdb file's experimental method was X-Ray.
If so, it gets a list of the kind of molecules present in the file. This list is written to the output file.
Then, it classifies all the HETATM as either nonstandard residues, ligands, or solvent.
These classified lines are written to the output file.
'''
def main(file_name, output_name):
    is_Xray = isXray(file_name)
    if is_Xray:
        output_file = open(output_name, "w")
        # If is xray, determine what is inside the file: ATOM, HETATM, DNA, RNA, LIGANDS, NON-STAN RES, OTHER
        molecule_list = determineMolecules(file_name)
        # Write the types found into the output file.
        output_file.write(file_name + " contains the following molecule types: \n")
        for molecule_type in molecule_list:
            output_file.write(molecule_type + "\n")

        # Then classify each hetatm line.
        classified_hetatm = classifyHETATM(file_name)
        output_file.write("\n")
        output_file.write("Here is a list of classified HETATMs, of the form: TYPE HETATMLINE \n")
        for hetatm_line in classified_hetatm:
            # Write each classified hetatm line into the output file.
            output_file.write(hetatm_line)
        output_file.write("\n")

        # Then create an array of possible molecules to select from.
        molecule_info = identifyMolecules(file_name)
        chain_list = molecule_info[0]
        ligand_list = molecule_info[1]
        nsr_list = molecule_info[2]
        solvent_list = molecule_info[3]
        other_list = molecule_info[4]

        # Write an organized summary of all chains, ligands, nonstandard residues, and solvents into the output file.
        output_file.write("Here are the specific names of chains, ligands, nonstandard residues, and solvents: \n")
        output_file.write("Chains: ")
        for chain in chain_list:
            output_file.write(chain + " ")
        output_file.write("\nLigands: ")
        for ligand in ligand_list:
            output_file.write(ligand + " ")
        output_file.write("\nNonstandard Residues: ")
        for nsr in nsr_list:
            output_file.write(nsr+ " ")
        output_file.write("\nSolvents: ")
        for solvent in solvent_list:
            output_file.write(solvent + " ")
        output_file.write("\nOther: ")
        for other in other_list:
            output_file.write(other + " ")
    

        output_file.close()
        return molecule_info # Ideally this would be pipelined into extract.py


'''
Determines whether a PDB file's experimental method is X-Ray.
If so, returns True. Otherwise, returns False.
'''
def isXray(file_name):
    pdb_file = open(file_name, "r")
    for line in pdb_file:
        lineList = line.split()
        if (len(lineList) >= 7):
            # If X-Ray, return True. Else, return False.
            if lineList[0] == "REMARK" and lineList[5] == "X-RAY":
                return True
    return False


'''
Returns a list of the kind of molecules the PDB file contains.
This could include ATOM, HETATM, PROTEIN, DNA, RNA, SOLVENT, NONSTANDARD RESIDUE, LIGAND.
'''
def determineMolecules(file_name):
    pdb_file = open(file_name, "r")
    
    has_found_atom = False
    has_found_hetatm = False
    has_found_protein = False
    has_found_DNA = False
    has_found_RNA = False
    has_found_solvent = False
    has_found_nsr = False
    has_found_ligand = False
    has_found_other = False
    
    moleculesPresent = []
    seqRes = getSeqRes(file_name)
    chain_list = getChains(file_name)

    resName = None
    chainID = None

    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
        if line[0:4] == "ATOM" or line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]

            #ATOM
            if line[0:4] == "ATOM" and has_found_atom == False:
                has_found_atom = True
                moleculesPresent.append("ATOM")
            # PROTEIN
            elif (line[0:4] == "ATOM" and len(resName) == 3 and has_found_protein == False):
                has_found_protein = True
                moleculesPresent.append("PROTEIN")
            # DNA
            elif (line[0:4] == "ATOM" and resName == "DT" and has_found_DNA == False):
                has_found_DNA = True
                moleculesPresent.append("DNA")
            # RNA
            elif (line[0:4] == "ATOM" and resName == "DU" and has_found_RNA == False):
                has_found_RNA = True
                moleculesPresent.append("RNA")
            # HETATM
            elif (line[0:6] == "HETATM" and has_found_hetatm == False):
                has_found_hetatm = True
                moleculesPresent.append("HETATM")
            # SOLVENT
            elif (line[0:6] == "HETATM" and (resName == "HOH" or resName == "AHOH" or resName == "BHOH") and has_found_solvent == False):
                has_found_solvent = True
                moleculesPresent.append("SOLVENT")
            # Nonstandard Residue
            # With 1HVR, the nsr was found in seqRes. Is this always the case?
            elif (line[0:6] == "HETATM" and resName in seqRes and has_found_nsr == False):
                has_found_nsr = True
                moleculesPresent.append("NONSTANDARD RESIDUE")
            # Ligand
            # Not in seqres and has chain and length of resname is 3 (according to deposit.rcsb.org/format-faq-v1.html)
            elif (line[0:6] == "HETATM" and (resName not in seqRes) and (chainID in chain_list) and has_found_ligand == False) and resName != "HOH" and (len(resName) == 3):
                has_found_ligand = True
                moleculesPresent.append("LIGAND")
            # OTHER (If gets through all other elifs and hasn't been classified.
            elif line[0:6] == "HETATM" and resName not in seqRes and len(resName) != 3 and (resName != "HOH" and resName != "AHOH" and resName != "BHOH") and has_found_other == False:
                has_found_other = True
                moleculesPresent.append("SOMETHING ELSE")
    return moleculesPresent


'''
Sorts through all of the HETATM lines in a given pdb.
It determines whether the line is a solvent, ligand, nonstandard residue, or something else.
It labels the beginning of the line with that classification, and the whole string is added to a list
which is returned by the function.

This list can be iterated through and output to the final text file.
'''
def classifyHETATM(file_name):
    # Midterm only asked for HETATM classification. ANISOU classification would be easy to add.
    pdb_file = open(file_name, "r")
    
    stanRes = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY", "HIS", "ILE", "LEU", "LYS", \
"MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL"]
    seqRes = getSeqRes(file_name)
    chain_list = getChains(file_name)
    resName = None
    chainID = None

    hetatmList = []
    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
        if line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]
            # If it's a hetatm that is hoh, it's water.
            if line[0:6] == "HETATM" and (resName == "HOH" or resName == "AHOH" or resName == "BHOH"):
                newline = "Solvent (water): " + line
                hetatmList.append(newline)
            # If it's a hetatm that is not listed in seqres, has a chainID and a name of length 3, it's a ligand.
            elif line[0:6] == "HETATM" and (resName not in seqRes) and (chainID in chain_list) and resName != "HOH" and (len(resName) == 3):
                newline = "Ligand: " + line
                hetatmList.append(newline)
            # If it's a hetatm that is in seqres, it's a non-standard residue.
            elif line[0:6] == "HETATM" and resName in seqRes:
                newline = "Nonstandard Residue: " + line
                hetatmList.append(newline)
            # Else if hetatm doesn't fit above descriptions, it's something else entirely.
            elif line[0:6] == "HETATM" and resName not in seqRes and len(resName) != 3 and resName != "HOH":
                newline = "Something Else: " + line
                hetatmList.append(newline)

    pdb_file.close()
    return hetatmList


'''
Identifies the specific chains, ligands, nonstandard residues, and solvent names.
Returns a dictionary containing all of this data stored in various lists.
'''
def identifyMolecules(file_name):
    chains_list = getChains(file_name)
    ligands_list = getLigands(file_name)
    nonStanRes_list = getNonStanRes(file_name)
    solvent_list = getSolvent(file_name)
    other_list = getOther(file_name, ligands_list)
    molecule_list = chains_list + ligands_list + nonStanRes_list + solvent_list
#    molecule_info = {"Chains": chains_list, "Ligands": ligands_list, "Nonstandard Residues": nonStanRes_list, "Solvent": solvent_list, "All Molecules": molecule_list}
    molecule_info = [chains_list, ligands_list, nonStanRes_list, solvent_list, other_list, molecule_list]
    return molecule_info


'''
Returns a list of all of the nonstandard residues in the PDB.
'''
def getNonStanRes(file_name):
    pdb_file = open(file_name, "r")
    seqRes = getSeqRes(file_name)
    chain_list = getChains(file_name)
    resName = None
    chainID = None


    nonStanRes_list = []
    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
        if line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]
            if line[0:6] == "HETATM" and resName in seqRes:
                if resName not in nonStanRes_list:
                    nonStanRes_list.append(resName)

    return nonStanRes_list


'''
Returns a list of all the OTHER lines in the PDB.
'''
def getOther(file_name, ligand_list):
    pdb_file = open(file_name, "r")
    seqRes = getSeqRes(file_name)
    chain_list = getChains(file_name)
    resName = None
    chainID = None

    others_list = []
    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
        if line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]

            if line[0:6] == "HETATM" and resName not in seqRes and resName not in ligand_list and (resName != "HOH" and resName != "AHOH" and resName != "BHOH"):
                if resName not in others_list:
                    others_list.append(resName)
    return others_list


'''
Returns a list of all of the ligands in a PDB.
'''
def getLigands(file_name):
    pdb_file = open(file_name, "r")
    seqRes = getSeqRes(file_name)
    chain_list = getChains(file_name)
    resName = None
    chainID = None

    ligands_list = []
    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.
        if line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]

            if line[0:6] == "HETATM" and resName not in seqRes and (resName != "HOH") and chainID in chain_list and (len(resName) == 3):
                if resName not in ligands_list:
                    ligands_list.append(resName)

    return ligands_list


# Assumes that solvent is always water.
'''
Assumes that the solvent will be water.
Returns a list containing "HOH" if there is water, or an empty list otherwise.
'''
def getSolvent(file_name):
    pdb_file = open(file_name, "r")
    chain_list = getChains(file_name)
    resName = None
    chainID = None

    solvent_list = []
    for line in pdb_file:
        # Sometimes the second and third lines have no space between them.
        # This deals with that.                               
        if line[0:6] == "HETATM":
            if line.split()[3] in chain_list:
                resName = line.split()[2][-4:]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[3]
            else:
                resName = line.split()[3]
                if resName[0] == "A" or resName[0] == "B":
                    resName = resName[1:]
                chainID = line.split()[4]

            if line[0:6] == "HETATM" and (resName == "HOH" or resName == "AHOH" or resName == "BHOH"):
                if resName not in solvent_list:
                    solvent_list.append(resName)
    return solvent_list


'''
Based off of Tori's discovery with 1HVR many classes ago, ligands are not in SEQRES while nonstandard residues are.
Thus, it is helpful to get all of the residues stored in SEQRES in a list.
This returns a list of the residues stored in SEQRES, for use in other functions. 
'''
def getSeqRes(file_name):
    pdb_file = open(file_name, "r")
    res_list = []
#    stanRes = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY", "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL"]
    for line in pdb_file:
    # NOTE: Only considers residues listed in SEQRES
        if line[0:6] == "SEQRES":
            ls = line.split()[4:]
            for res in ls:
                if not res in res_list:
                    res_list.append(res)
    pdb_file.close()
    return res_list


'''
getChains returns a list of all of the chains in the PDB file.
'''
def getChains(file_name):
    chain_list = []
    pdb_file = open(file_name, "r")
    resName = None
    chainID = None

    for line in pdb_file:
        if line[0:4] == "ATOM":
            # If the 2nd and 3rd lines have blended together.
            if line.split()[4].isdigit():
                chainID = line.split()[3]
            else:
                chainID = line.split()[4]
            if not chainID in chain_list:
                chain_list += [chainID]
    pdb_file.close()
    return chain_list

if __name__ == '__main__':
	if (len(sys.argv) < 2):
	    print("Please enter a pdb file name and an output file name.")
	else:
	    main(sys.argv[1], sys.argv[2])
