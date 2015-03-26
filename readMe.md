Kaitlyn Stumpf
CSC334, Spring 2015
3/12/2015
Midterm, X-Ray Protein
======================

<h3>What is proteinAnalysisCLI?</h3>
<p>proteinAnalysisCLI is a command line interface for analyzing, extracting, pruning, and visualizing a given RCSB Protein Data Bank pdb file. It relies on the <a href="http://jmol.sourceforge.net/">jMol software</a> for visualization.
</p>

<h3>Configuration:</h3>
<p>
Download the .zip file located to the right.
From the command line, enter the project directory and run the program by typing the following: 
        python run_steps.py
When prompted for a .pdb file, use one of the four example files provided:
<ul>
   <li>1HVR.pdb</li>
   <li>4MC1.pdb</li>
   <li>4QJ6.pdb</li>
   <li>4U8W.pdb</li>
</ul>
</p>

<h3>Functionality</h3>
<p>
1. Runs isXray.py to determine if pdb file's experimental method was Xray.
   If it was, returns a ####_DATA.txt file which does the following:
   <ul>
      <li>Describes the different molecule types present</li>
      <li>Classifies the HETATM lines</li>
      <li>Names all chains, ligands, nonstandard residues, solvents, and "something else" present</li>
   </ul>
2. Visualizes the protein in jMol. Flashes through chains, water, ligands, hetatms, and amino acids.
3. Runs extract.py and extracts the molecule(s) based on the molecule type & specific molecule names provided by the user. 
   The extract options are:
   <ul>
      <li>Single item</li>
      <li>Multiple items</li>
      <li>All items</li>
   </ul>
4. Runs prune.py and writes a new pdb file without solvent or "something else" HETATM lines.
5. Runs writeHydScript.py and writes a personalized "remove hydrogens" JMol script for the pdb.
6. Runs JMol, loads the newly written script, visualizes the pdb with hydrogens, and creates a ####_H.pdb file that contains hydrogens and renumbered ATOM lines and reorganized CONECT lines.
7. Creates a script for computing bonds and then loads this script in JMol. The script creates a text file containing all of the bonds. Then reformats the bonds so that they are in pairs, with each pair written on its own line.
8-9. Creates scripts for extracting the ligand with and without hydrogens added, and then runs these scripts in JMol.
10. Creates a script for extracting specifically requested chains using JMol. The script creates a text file containing all of the chains requested. Couldn’t quite get the correct output in the text file.
</p>
