import csv
from pathlib import Path
from pymatgen.core import Molecule
from pymatgen.symmetry.analyzer import PointGroupAnalyzer

def get_symmetry_info(xyz_path):
    mol = Molecule.from_file(xyz_path)
    pga = PointGroupAnalyzer(mol)
    point_group = pga.get_pointgroup()

    #counsts symmetry operations by type
    symm_ops = len(pga.get_symmetry_operations())
    rot_count = pga.get_rotational_symmetry_number()

    return {
        "point_group": point_group,
        "rotation_axes": rot_count,
        "num_symm_ops": symm_ops,
        "mirror_planes": 'n/a',
        "inversion_centers": 'n/a',
        "improper_rotations": 'n/a',
        "symm_equivalent_atoms": 'n/a'
    }

xyz_dir = Path("xyz_files")
output_csv = Path("symmetry_analysis.csv")

with output_csv.open("w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "filename",
        "point_group",
        "rotation_axes",
        "num_symm_ops",
        "mirror_planes",
        "inversion_centers",
        "improper_rotations",
        "symm_equivalent_atoms"
    ])
    for xyz_file in xyz_dir.glob("*.xyz"):
        info = get_symmetry_info(xyz_file)
        #converts list of lists to string for CSV
        eq_atoms_str = ";".join([",".join(map(str, group)) for group in info["symm_equivalent_atoms"]])
        writer.writerow([
            xyz_file.name,
            info["point_group"],
            info["rotation_axes"],
            info["num_symm_ops"],
            info["mirror_planes"],
            info["inversion_centers"],
            info["improper_rotations"],
            eq_atoms_str
        ])
        print(f"Processed {xyz_file.name}: {info['point_group']}")

print(f"Symmetry results saved to {output_csv}")
