proteinAnalysisCLI
==================

<h3>What is proteinAnalysisCLI?</h3>
<p>proteinAnalysisCLI is a command line interface for analyzing, extracting, pruning, and visualizing a given RCSB Protein Data Bank pdb file. It relies on the <a href="http://jmol.sourceforge.net/">jMol software</a> for visualization.
</p>

<h3>Configuration:</h3>
<p>
Download the .zip file located to the right.
From the command line, enter the project directory and run the program by typing the following: 
<ul>
   <li>python run_steps.py</li>
</ul>
When prompted for a .pdb file, use one of the four example files provided:
<ul>
   <li>1HVR.pdb, 4MC1.pdb, 4QJ6.pdb, or 4U8W.pdb</li>
</ul>
</p>

<h3>Functionality</h3>
<p>
<ol>
<li>Runs isXray.py to determine if pdb file's experimental method was Xray.
   If it was, returns a ####_DATA.txt file which does the following:
   <ul>
      <li>Describes the different molecule types present</li>
      <li>Classifies the HETATM lines</li>
      <li>Names all chains, ligands, nonstandard residues, solvents, and "something else" present</li>
   </ul>
</li>
<li>Visualizes the protein in jMol. Flashes through chains, water, ligands, hetatms, and amino acids.</li>
<li>Runs extract.py and extracts the molecule(s) based on the molecule type & specific molecule names provided by the user. 
   The extract options are:
   <ul>
      <li>Single item</li>
      <li>Multiple items</li>
      <li>All items</li>
   </ul>
</li>
<li>Runs prune.py and writes a new pdb file without solvent or "something else" HETATM lines.</li>
<li>Runs writeHydScript.py and writes a personalized "remove hydrogens" JMol script for the pdb.</li>
<li>Runs JMol, loads the newly written script, visualizes the pdb with hydrogens, and creates a ####_H.pdb file that contains hydrogens and renumbered ATOM lines and reorganized CONECT lines.</li>
<li>Creates a script for computing bonds and then loads this script in JMol. The script creates a text file containing all of the bonds. Then reformats the bonds so that they are in pairs, with each pair written on its own line.</li>
<li>Creates scripts for extracting the ligand with and without hydrogens added, and then runs these scripts in JMol.</li>
</ol>
</p>

<h3>Future Endeavours</h3>
<p>
Create a script for extracting specifically requested chains using JMol. The script will create a text file containing all of the chains requested.
</p>
