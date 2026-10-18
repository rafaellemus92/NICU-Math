#!/bin/bash
D=.
cd $D
until [ -f $D/c1_N64_dt0.005.json ]; do sleep 5; done
echo "=== C3 N=24 ==="; python3 c3.py 24 2>&1 | tee c3_24.log
echo "=== C3 N=32 ==="; python3 c3.py 32 2>&1 | tee c3_32.log
echo "=== C3 N=48 ==="; python3 c3.py 48 2>&1 | tee c3_48.log
echo "=== C5 N=24 ==="; python3 c5.py 24 16 2>&1 | tee c5_24.log
echo "=== C4 N=24 ==="; python3 c4.py 24 2>&1 | tee c4_24.log
echo "=== C4 N=32 ==="; python3 c4.py 32 2>&1 | tee c4_32.log
echo "=== C1 N=32 dt=0.0025 ==="; python3 c1.py 32 0.0025 2>&1 | tee c1_32_dt0.0025.log
echo "=== C3 N=32 dt=0.0025 ==="; python3 c3.py 32 0.0025 notan 2>&1 | tee c3_32_dt0.0025.log
echo QUEUE1_DONE
