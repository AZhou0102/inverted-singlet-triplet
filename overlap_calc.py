import subprocess
import re
import csv
import os

#multifwn path
MULTIWFN_EXEC = "Multiwfn_noGUI"

CHK_FOLDER = "./chk_files/"

CSV_OUTPUT = "overlap_results.csv"

def get_homo_lumo_indices(chk_file):
    """
    calls Multiwfn to determine HOMO and LUMO indices
    """
    input_str = "0\nq\n"  #quits after displaying orbital numbers
    proc = subprocess.run([MULTIWFN_EXEC, chk_file], input=input_str, capture_output=True, text=True)
    out = proc.stdout

    match = re.search(r"Orbital\s+(\d+)\s+is HOMO.*?\n\s*Orbital\s+(\d+)\s+is LUMO", out)
    if match:
        homo = int(match.group(1))
        lumo = int(match.group(2))
        return homo, lumo

    raise RuntimeError("failed  parsing HOMOLUMO orbitals")



def run_multiwfn_overlap(chk_file, homo, lumo):
    """
    calls Multiwfn to calculate overlap and centroid distance of HOMO and LUMO orbital lobes
    """
    # input commands
    # 100 "other functions"
    # 11 "Calculate overlap and centroid distance between two orbitals"
    # inputs indices(e.g. "21,22")
    # 0,0 to exit
    input_commands = f"100\n11\n{homo},{lumo}\n0,0\n"

    proc = subprocess.run([MULTIWFN_EXEC, chk_file], input=input_commands, capture_output=True, text=True)
    out = proc.stdout
    
    #parses output
    
    centroid_dist = None
    overlap_norm = None
    overlap_square = None
    
    cd_match = re.search(r"Centroid distance between the two orbitals:\s*([\d\.\-E+]+) Angstrom", out)
    on_match = re.search(r"Overlap integral of norm of the two orbitals:\s*([\d\.\-E+]+)", out)
    os_match = re.search(r"Overlap integral of square of the two orbitals:\s*([\d\.\-E+]+)", out)

    if cd_match:
        centroid_dist = float(cd_match.group(1))
    if on_match:
        overlap_norm = float(on_match.group(1))
    if os_match:
        overlap_square = float(os_match.group(1))
    
    return centroid_dist, overlap_norm, overlap_square

def main():
    files = [f for f in os.listdir(CHK_FOLDER) if f.endswith(".chk")]
    results = []
    print(f"found {len(files)} checkpoint files.")
    
    for chk in files:
        full_path = os.path.join(CHK_FOLDER, chk)
        print(f"processing {chk}...")
        
        homo, lumo = get_homo_lumo_indices(full_path)
        print(f"  HOMO: {homo}, LUMO: {lumo}")
        
        centroid_dist, overlap_norm, overlap_square = run_multiwfn_overlap(full_path, homo, lumo)
        print(f"  Centroid distance: {centroid_dist}")
        print(f"  Overlap integral (norm): {overlap_norm}")
        print(f"  Overlap integral (square): {overlap_square}")
        
        results.append({
            "filename": chk,
            "homo": homo,
            "lumo": lumo,
            "centroid_distance_A": centroid_dist,
            "overlap_norm": overlap_norm,
            "overlap_square": overlap_square
        })
    
    #write CSV
    with open(CSV_OUTPUT, "w", newline="") as csvfile:
        fieldnames = ["filename", "homo", "lumo", "centroid_distance_A", "overlap_norm", "overlap_square"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n done and saved @ {CSV_OUTPUT}")

if __name__ == "__main__":
    main()
