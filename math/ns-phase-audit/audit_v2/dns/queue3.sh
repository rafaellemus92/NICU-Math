#!/bin/bash
D=.
cd $D
until grep -q QUEUE2_DONE $D/queue2.log; do sleep 5; done
echo "=== C5 sweep N=24 M=32 ==="; python3 c5.py 24 32 2>&1 | tee c5_24_M32.log
echo QUEUE3_DONE
