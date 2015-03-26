Kaitlyn Stumpf
CSC334, Spring 2015
3/12/2015
Midterm, X-Ray Protein

I chose to complete the X-Ray Protein midterm.
Read runPython.txt to learn how to run my program and discover different inputs that test what it can do.
Read run_steps.py to see the python wrapper and discover exactly what my program does.

Here is a short list of what it does:

1. Runs isXray.py to determine if pdb file's experimental method was Xray.
   If it was, returns a ####_DATA.txt file about what the pdb file contains.
   This text file lists the different molecule types present, classifies the HETATM lines, and names all chains, ligands, nonstandard residues, solvents, and "something else" that is present.
2. Runs extract.py and extracts the molecule type and specific names requested by the user. The extract options are a single item, multiple items, or all items.
3. Runs prune.py and writes a new pdb file without solvent or "something else" HETATM lines.
4. Runs writeHydScript.py and writes a personalized "remove hydrogens" JMol script for the pdb.
5. Runs JMol, loads the newly written script, visualizes the pdb with hydrogens, and creates a ####_H.pdb file that contains hydrogens and renumbered ATOM lines and reorganized CONECT lines.
6. Visualizes the protein. Flashes through chains, water, ligands, hetatms, and amino acids. (This step was moved between 1 and 2).
7. Creates a script for computing bonds and then loads this script in JMol. The script creates a text file containing all of the bonds. Then reformats the bonds so that they are in pairs, with each pair written on its own line.
8-9. Creates scripts for extracting the ligand with and without hydrogens added, and then runs these scripts in JMol.
10. Creates a script for extracting specifically requested chains using JMol. The script creates a text file containing all of the chains requested. Couldn’t quite get the correct output in the text file.