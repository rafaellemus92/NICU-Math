#!/bin/bash
D=.
cd $D
until grep -q QUEUE3_DONE $D/queue3.log; do sleep 5; done
echo "=== N=64 dt=0.01 rk4/if phi=0 ==="
python3 ns_if.py 64 0.01 rk4 0.0 2>&1 | tee -a dtcheck_64.log
python3 ns_if.py 64 0.01 if 0.0 2>&1 | tee -a dtcheck_64.log
echo "=== N=96 C1 phi=0 ==="; python3 c1.py 96 0.005 0.0 2>&1 | tee c1_96.log
echo QUEUE4_DONE
