# IST analysis tools

This repository contains Python scripts to analyze NEMO-generated ensembles and Gaussian/Q-Chem output files.
Outputs include oscillator strengths, orbital overlap integrals, r1^2 values, and molecular symmetry properties.
Example outputs are shown for all scripts.

## Synopsis of scripts/notebooks

### `osc_strengths.py`

Extracts the maximum oscillator strength from each geometry in a NEMO ensemble  to find the corresponding dominant vibrational modes.

- Input:
  - path to a NEMO molecule directory (edit `molecule = "..."` in the script).
- Output:
  - `oscillator_strengths.csv` including:
    - max oscillator strength and corresponding energy per geometry
    - index of dominant vibrational mode, displacement, frequency, and mass
- requires in the path:
  - `ensembleS1/Geometries/*.log`
  - `ensembleS1/freqS1.log`
  - `ensembleS1/Magnitudes_300K_.lx`

### `overlap_calc.py`

Uses Multiwfn to compute spatial separation and overlap of HOMO LUMO orbitals.
Relies on Multiwfn's analytical method of using wavefunction integrals (see Multiwfn's documentation 3.100.11)

- Input:
  - folder of `.xyz` files (default: `xyz_files/`) (note that hpc2 contains a script to convert .chk files to .xyz files)
- Output:
  - `overlap_results.csv` with:
    - HOMO and LUMO indices
    - centroid distance / spatial separation between orbitals
    - Overlap integral (both norm and square)
- Requires:
  - Multiwfn binary (default name: `Multiwfn_noGUI`) to be in `PATH`

### `symmetry_analysis.py`

Computes molecular point group symmetry and other measures for each `.xyz` file in a directory.

- Input:
  - directory of `xyz_files/` with `.xyz` molecular files
- Output:
  - `symmetry_analysis.csv` containing:
    - Point group
    - Rotational symmetry number
    - Number of symmetry operations
    - Other symmetry-related metadata (`"n/a"` for now)
- Depends on:
  - pymatgen
 
### `r1r2_calculator.ipynb`

Calculates the r₁² and r₂² excitation parameters for a given optimized geometry from an EOM-CCSD calculation.

Usage:
    Copy and paste the full text of the “Left eigenvector” section from your .log file into the notebook input cell.


## Usage

Clone repo:
   ```bash
   git clone https://github.com/yourusername/nemo-analysis.git
   cd nemo-analysis

Install dependencies:
  pip install pandas pymatgen

Set up Multiwfn:
  Multiwfn_noGUI must be in `PATH`
```
---

## Citations

NEMO

    Leonardo E. de Sousa, NEMO: Nuclear Ensemble Method for Optical spectra, GitHub repository, 
    https://github.com/LeonardoESousa/NEMO (accessed July 2025).

Multiwfn

    Tian Lu, Feiwu Chen, Multiwfn: A Multifunctional Wavefunction Analyzer, J. Comput. Chem. 33, 580–592 (2012), DOI: 10.1002/jcc.22885

    Tian Lu, A comprehensive electron wavefunction analysis toolbox for chemists: Multiwfn, J. Chem. Phys. 161, 082503 (2024), DOI: 10.1063/5.0216272

Gaussian 16

    M. J. Frisch et al., Gaussian 16, Revision C.01, Gaussian Inc., Wallingford CT, 2016.

Q-Chem

    Y. Shao et al., Advances in molecular quantum chemistry contained in the Q-Chem 4 program package, Mol. Phys. 113, 184–215 (2015)

Pymatgen

    Shyue Ping Ong, Wei Chen, Zhiqiang Dong, Quanqi Wang, and Kristin Persson.
    Python Materials Genomics (pymatgen): A robust, open-source python library for materials analysis.
    Comput. Mater. Sci. 68, 314–319 (2013).
    DOI: 10.1016/j.commatsci.2012.10.028
