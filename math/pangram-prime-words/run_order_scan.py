"""
Digit-assignment ("transliteration") experiment, base 26, English clusters,
1-2 vowels.  For each assignment: prime dictionary size, exhaustive
exact-cover existence (witness or proof of none) and, with --count, the exact
number of perfect pangrams (engine, 2 moduli).

usage: python3 run_order_scan.py named [--count]          # the orders in orders.py
       python3 run_order_scan.py random <seed0> <seed1>  # random permutations, existence only
"""
import json, os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))


def run_one(name, order, count=False):
    env = dict(os.environ, PANGRAM_ORDER=order)
    code = f"""
import json, time
from core import *
t0 = time.time()
prime = english_words(prime_only=True)
sols, nodes = exact_cover_c(prime, max_solutions=1, tag={name!r})
rec = dict(name={name!r}, order={order!r}, n_prime=len(prime), witness=show(prime, sols[0]) if sols else None,
           nodes=nodes, final_letters=''.join(ch for ch in ALPHABET if DIGIT[ch] % 2 and DIGIT[ch] % 13))
if {count!r} and sols:
    from engine import exact_count
    cnt, M = exact_count(prime, nprimes=2)
    rec['count'] = cnt[0]
rec['seconds'] = round(time.time() - t0, 1)
json.dump(rec, open('results/order_scan/{name}.json', 'w'), indent=1)
print(json.dumps(rec))
"""
    out = subprocess.run([sys.executable, "-c", code], env=env, cwd=HERE, capture_output=True, text=True)
    if out.returncode != 0:
        print(name, "FAILED", out.stderr[-500:], flush=True)
        return None
    rec = json.loads(out.stdout.strip().splitlines()[-1])
    print(f"{name:16s} prime words {rec['n_prime']:6,d}  final letters {rec['final_letters']:14s} "
          f"{'SOLUTION  ' + rec['witness'][:60] if rec['witness'] else 'none (' + f'{rec['nodes']:,}' + ' nodes)'}"
          + (f"  count {rec['count']:,}" if 'count' in rec else "") + f"  [{rec['seconds']}s]", flush=True)
    return rec


if sys.argv[1] == "named":
    from orders import ORDERS
    for name, order in ORDERS.items():
        run_one(name, order, count="--count" in sys.argv)
else:
    s0, s1 = int(sys.argv[2]), int(sys.argv[3])
    for seed in range(s0, s1):
        rnd = random.Random(seed)
        letters = list("abcdefghijklmnopqrstuvwxyz")
        rnd.shuffle(letters)
        run_one(f"random_{seed:03d}", "".join(letters))
