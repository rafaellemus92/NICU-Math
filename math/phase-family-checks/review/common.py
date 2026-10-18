import sys, importlib.util
from pathlib import Path
PKG = Path(__file__).resolve().parents[2] / 'all-time-phase-response'
OUT = Path(__file__).resolve().parent / 'out'
sys.path.insert(0, str(PKG))
from response import Response, audit, integrate, harmonics  # noqa
import numpy as np
NU = 1/28
def harm_cos(vals, m):
    p = 2*np.pi*np.arange(len(vals))/len(vals)
    return (1 if m == 0 else 2)*np.mean(np.asarray(vals)*np.cos(m*p)[:, None], axis=0)
def harm_sin(vals, m):
    p = 2*np.pi*np.arange(len(vals))/len(vals)
    return 2*np.mean(np.asarray(vals)*np.sin(m*p)[:, None], axis=0)
