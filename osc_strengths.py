import csv
import re
import os
import pandas as pd

#remember to specify which NEMO molecule's directory you want to examine
molecule = "./Hz3TBPCz3_s1_td/"

#the rest of the paths dont need to be changed
#UNLESS you are not working with S1 calculations or are looking at a different temperature
internal_geo_path = "ensembleS1/Geometries/"
geometries_folder = os.path.join(molecule, internal_geo_path)
CSV_OUTPUT = "oscillator_strengths.csv"

internal_lx_path = "ensembleS1/Magnitudes_300K_.lx"
LX_FILE = os.path.join(molecule, internal_lx_path)

internal_freq_path = "ensembleS1/freqS1.log"
FREQ_FILE = os.path.join(molecule, internal_freq_path)

def extract_mode_frequencies(freq_log_file):
    mode_freq_map = {}
    
    with open(freq_log_file) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        if "Frequencies --" in lines[i]:
            
            freq_line = lines[i]
            freqs = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", freq_line)))

            #gets the mode numbers (usually two lines above, should be a sequence of three integers)
            mode_line = lines[i - 2]
            modes = list(map(int, re.findall(r"\d+", mode_line)))

            for mode, freq in zip(modes, freqs):
                mode_freq_map[mode] = freq

        i += 1

    return mode_freq_map


def extract_strongest_singlet(log_file):
    with open(log_file) as f:
        lines = f.readlines()

    strengths = []
    i = 0
    while i < len(lines):
        if "Excited state" in lines[i]:
            energy_line = lines[i]
            mult_line = lines[i+2]
            strength_line = lines[i+4]

            if "Singlet" in mult_line:

                energy_match = re.search(r"excitation energy \(eV\) =\s+([\d.]+)", energy_line)
                if energy_match:
                    energy = float(energy_match.group(1))
                else:
                    energy = None

                #oscillator strength
                strength = float(strength_line.split(":")[-1].strip())

                #stores indices and values
                strengths.append((i, strength, energy))
        i += 1

    if strengths:
        _, max_strength, max_energy = max(strengths, key=lambda x: x[1])
        print(f"Max strength: {max_strength}, energy: {max_energy}")
        return max_strength, max_energy

    print('done')
    return None, None

def get_dominant_modes(LX_FILE, idx):

    df = pd.read_csv(LX_FILE)
    mode_columns = df.columns[df.columns.str.startswith("mode_")]
    
    results = []

    displacements = df.loc[idx - 1, mode_columns]
    max_mode_col = displacements.abs().idxmax()
    max_value = displacements[max_mode_col]
    mode_number = int(max_mode_col.split("_")[1])
    freq = df.loc[idx - 1, "freq"]
    mass = df.loc[idx - 1, "mass"]

    results.append({
        "geometry_index": idx,
        "mode": mode_number,
        "displacement": max_value,
        "frequency": freq,
        "mass": mass
    })

    return idx, mode_number, max_value, freq, mass


def main():

    freq_map = extract_mode_frequencies(FREQ_FILE)

    files = [f for f in os.listdir(geometries_folder) if f.endswith(".log")]
    results = []
    print(f"found {len(files)} geometry logs")
    
    for log in files:
        full_path = os.path.join(geometries_folder, log)
        
        match = re.search(r"Geometry-(\d+)-\.log", log)
        if match:
            geo_number = int(match.group(1))

        print(f"reading {log}, geo_number {geo_number}")
        
        geometry_strength, geometry_energy  = extract_strongest_singlet(full_path)
        print(f"strongest singlet: {geometry_strength}")
        
        index, mode_number, max_value, freq, mass = get_dominant_modes(LX_FILE, geo_number)
        
        results.append({"filename":log,
                        "geom_number":geo_number,
                        "geom_max_strength": geometry_strength,
                        "geom_energy_eV": geometry_energy,
                        "geom_energy_nm": 1240 / geometry_energy,
                        "mode_num": mode_number,
                        "modal_frequency_cm": freq_map[mode_number],
                        "m_displacement": max_value,
                        "m_frequency_rad": freq,
                        "m_mass": mass
                    })

        
    with open(CSV_OUTPUT, "w", newline="") as csvfile:

# geom is abbreviation for geometry, corresponding to the data in geometry's qchem log file
# m is abbreviation for magnitude, corresponding to the data in the Magnitudes.lx NEMO input file
        fieldnames = ["filename", "geom_number", "geom_max_strength",
                      "geom_energy_eV", "geom_energy_nm", 
                      "mode_num", "modal_frequency_cm",
                      "m_displacement", "m_frequency_rad", "m_mass"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"done and saved @ {CSV_OUTPUT}")

if __name__ == "__main__":
    main()
