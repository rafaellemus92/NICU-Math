#!/bin/bash
D=.
cd $D
until grep -q QUEUE1_DONE $D/queue1.log; do sleep 5; done
echo "=== C5opt N=24 ==="; python3 c5_opt.py 24 2:0.96,2.5:1.42,3:1.64,3.5:1.85,4:2.12 2>&1 | tee c5opt_24.log
echo "=== C5 sweep N=32 ==="; python3 c5.py 32 16 2>&1 | tee c5_32.log
echo "=== C5opt N=32 ==="; python3 c5_opt.py 32 3:1.64,4:2.12 2>&1 | tee c5opt_32.log
echo "=== C4 N=48 newton ==="; python3 c4.py 48 newton 2>&1 | tee c4_48.log
echo "=== C1 N=64 dt=0.0025 phi=0 ==="; python3 c1.py 64 0.0025 0.0 2>&1 | tee c1_64_dt0.0025.log
echo "=== IF-RK4 N=64 dt=0.005 ==="; python3 ns_if.py 64 0.005 if 0.0,0.971073032,2.159844949 2>&1 | tee if_64.log
echo "=== C3 N=64 ==="; python3 c3.py 64 2>&1 | tee c3_64.log
echo QUEUE2_DONE
