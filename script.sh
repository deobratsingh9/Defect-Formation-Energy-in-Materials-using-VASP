#!/bin/bash
#SBATCH -J SiC_Defects
#SBATCH -N 2
#SBATCH --ntasks-per-node=16
#SBATCH -t 002:00:00
#SBATCH -A xxx

# Load VASP
module add VASP/5.4.4.16052018-wannier90-nsc1-intel-2018a-eb

# Prevent oversubscription
export OMP_NUM_THREADS=1

# Log everything
exec > job.log 2>&1

# =========================
# FUNCTION TO RUN VASP
# =========================
run_vasp () {

    echo "=================================="
    echo "Running in folder: $PWD"
    echo "=================================="

    # ---------- RELAX ----------
    if [[ -f INCAR_relax && -f KPOINTS_relax ]]; then
        echo ">>> RELAXATION STEP"

        cp INCAR_relax INCAR
        cp KPOINTS_relax KPOINTS

        mpprun vasp_std > vasp_relax.out

        if [[ -f OUTCAR ]]; then
            cp OUTCAR OUTCAR.relax
        fi

        if [[ -f CONTCAR ]]; then
            cp CONTCAR POSCAR
        fi
    else
        echo "No relaxation inputs found, skipping..."
    fi

    # ---------- STATIC ----------
    if [[ -f INCAR_static && -f KPOINTS_static ]]; then
        echo ">>> STATIC STEP"

        cp INCAR_static INCAR
        cp KPOINTS_static KPOINTS

        mpprun vasp_std > vasp_static.out

        if [[ -f OUTCAR ]]; then
            cp OUTCAR OUTCAR.static
        fi

        if [[ -f vasprun.xml ]]; then
            cp vasprun.xml vasprun.static.xml
        fi
    else
        echo "No static inputs found, skipping..."
    fi

    # Cleanup
    rm -f WAVECAR WAVEDER

    echo "Done: $PWD"
    echo ""
}

# =========================
# RUN BULK
# =========================
if [[ -d Bulk_SiC ]]; then
    echo "===== BULK_SiC ====="
    cd Bulk_SiC
    run_vasp
    cd ..
fi

# =========================
# RUN V_C
# =========================
if [[ -d V_C ]]; then

    echo "===== V_C ROOT ====="
    cd V_C

    # run if INCAR_relax exists in V_C itself
    run_vasp

    echo "===== V_C CHARGE STATES ====="

    for sub in */ ; do
        [[ -d "$sub" ]] || continue

        echo "---- Entering $sub ----"
        cd "$sub"

        run_vasp

        cd ..
    done

    cd ..
fi

echo "=================================="
echo " ALL JOBS FINISHED "
echo "=================================="
