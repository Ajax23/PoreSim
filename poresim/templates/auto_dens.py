import os
import porems as pms
import poresim as ps
import poreana as pa
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Add Todos
    print("Finish fill scripts ...")
    print("Finish ana.sh file ...")
    print("Add following script to running shell")
    # cd ../ana
    # sh ana.sh
    # python ana.py

    # Load molecule
    mol = pms.Molecule("molecule", "MOLSHORT", inp="MOLLINK")

    # Set analysis
    ana_list = {}
    ana_list["MOLSHORT"] = {"traj": "traj.xtc",
                            "dens": True, "diff": False, "mol": mol, "atoms": []}

    box = pa.utils.load("../_gro/pore.yml")["dimensions"]
    res = pa.utils.load("../_gro/pore.yml")["reservoir"]

    # Run analysis
    for ana_name, ana_props in ana_list.items():
        sample = pa.Sample(box, ana_props["traj"], ana_props["mol"], ana_props["atoms"], [
                           1 for x in ana_props["atoms"]])
        if ana_props["dens"]:
            sample.init_density("dens_"+ana_name+".obj")
        if ana_props["diff"]:
            sample.init_diffusion_bin("diff_"+ana_name+".obj", bin_num=35)
        sample.sample(is_parallel=True)

    # Calculate density
    dens = pa.density.bins("dens_MOLSHORT.obj",
                           target_dens=TARGETDENS, box_res=res)

    # Fill and rerun
    num_diff = dens["diff"]
    if num_diff > 10:
        ps.utils.copy("../_fill/fillBackup.sh", "../_fill/fill.sh")
        ps.utils.replace("../_fill/fill.sh", "FILLDENS", str(int(num_diff)))

        os.system("cd ../_fill;sh fill.sh;cd ../min;SUBMITCOMMAND")
    else:
        ps.utils.copy("../_fill/fillBackup.sh", "../_fill/fill.sh")
        ps.utils.replace("../_fill/fill.sh", "FILLDENS", str(int(0)))

        os.system("cd ../_fill;sh fill.sh")
