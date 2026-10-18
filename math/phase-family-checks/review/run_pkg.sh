#!/bin/bash
cd "$(dirname "$0")/../../all-time-phase-response"
echo "== unittest"; python3 -m unittest -v test_response 2>&1
echo "== check_observable_remainder"; python3 check_observable_remainder.py 2>&1; echo "exit $?"
echo "== pilot refined"; python3 pilot.py --coarse-N 18 --output results/reproduction_refined.json 2>&1; echo "exit $?"
