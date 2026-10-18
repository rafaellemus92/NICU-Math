#!/bin/sh
# Quick end-to-end checks (few minutes, < 1 GB RAM). Run from the project root.
set -e
make pairs diff brute
echo "== equal-sum search (expect: 5-pair solutions: 0)"; ./pairs 40000 | tail -2
echo "== equal-difference search (expect: D=204, 258, 534)"; ./diff 20000 | tail -4
echo "== brute-force partition counts (expect 27152 73155 30128 122443)"; ./brute 4 ABCDEFGHIJKL:5 ABCDEFGHIJKL:4 ABCDEFGHIJKL:3 ABCDEFGHIJKLM:5
echo "== python tests"; python3 tests/test_solutions.py
