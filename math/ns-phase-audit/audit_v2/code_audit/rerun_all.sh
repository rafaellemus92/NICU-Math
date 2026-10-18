#!/bin/bash
# Sequential (one heavy process at a time) reproduction of the package's runs.
PKG=../../periodic_ns_lab_v2
OUT=../code_audit_rerun
cd "$PKG" || exit 1
stamp(){ echo "### $(date +%T) $*"; }
stamp sweep;   python3 run_extended.py --stage sweep --out "$OUT/sweep" --count 33 --n 24 --workers 1 > "$OUT/sweep.log" 2>&1; echo "exit $?"
for dt in .01 .005 .0025; do
  lab=dt$(python3 -c "print(float('$dt'))")
  stamp time $lab; python3 run_extended.py --stage single --out "$OUT/time_refinement" --n 32 --phase 0.9704087638177281 --end 2 --dt $dt --label $lab --workers 1 >> "$OUT/time_refinement.log" 2>&1; echo "exit $?"
done
for n in 24 32 48; do
  stamp curvature $n; python3 phase_sensitivity.py --n $n --phase 0 --end 2.2 --sample .01 --out "$OUT/curvature_N$n" > "$OUT/curvature_N$n.log" 2>&1; echo "exit $?"
done
stamp opt24; python3 phase_sensitivity.py --optimize --n 24 --phase 1.0 --out "$OUT/optimization_N24_T2" > "$OUT/opt24.log" 2>&1; echo "exit $?"
stamp opt32; python3 phase_sensitivity.py --optimize --n 32 --phase 0.9710730319801146 --out "$OUT/optimization_N32_T2" > "$OUT/opt32.log" 2>&1; echo "exit $?"
stamp refine; python3 run_extended.py --stage refine --out "$OUT/refine" --workers 1 --grids 64 48 32 --end 4 --phases 0 0.9710730319801146 2.1598449493429825 > "$OUT/refine.log" 2>&1; echo "exit $?"
stamp done
