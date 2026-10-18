"""b = 0 on the long run's time grid (nu = 1/28, a = c = d = 1): A, B1, B2 of E, Z, S every 0.5 to t = 20,
eight phases, from the reduced one-dimensional equation.  Writes results/reduced_family_t20.json, which
measured_constants.py reads.  Run: python3 reduced_family_t20.py
"""
import numpy as np, json
from reduced_family import harmonics

M, dt, nu, T = 96, 5e-4, 1/28, 20.0
phis = 2*np.pi*np.arange(8)/8
y = 2*np.pi*np.arange(M)/M; k = np.fft.fftfreq(M)*M
states = [1.0 - np.exp(1j*(y+p)) for p in phis]

def rhs(t, wh):
    return -1j*np.exp(-nu*t)*np.sin(y)*wh + nu*np.fft.ifft(-(k**2+1)*np.fft.fft(wh))

def diag(t, wh):
    why = np.fft.ifft(1j*k*np.fft.fft(wh)); Ua = np.exp(-nu*t)
    E = Ua**2/4 + np.mean(np.abs(wh)**2)/4
    Z = Ua**2/4 + np.mean(np.abs(wh)**2 + np.abs(why)**2)/4
    S = -(Ua/2)*np.mean(np.cos(y)*np.real(np.conj(1j*wh)*why))
    return E, Z, S

n = int(round(T/dt)); every = int(round(0.5/dt)); t = 0.0; out = []
print("   t     E:A      E:B1      Z:A      Z:B1      S:A      S:B1")
for i in range(n+1):
    if i % every == 0:
        vals = np.array([diag(t, w) for w in states])
        row = dict(t=round(t, 3))
        for name, col in (("E", 0), ("Z", 1), ("S", 2)):
            h = harmonics(vals[:, col], phis); row[name] = dict(A=h[0][0], B1=h[1][0], B2=h[2][0])
        out.append(row)
        if round(t, 3) in (0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20):
            print(f"{t:5.1f} {row['E']['A']:8.4f} {row['E']['B1']:+9.5f} {row['Z']['A']:8.4f} {row['Z']['B1']:+9.5f} {row['S']['A']:+8.4f} {row['S']['B1']:+9.5f}   (|Z:B2| {abs(row['Z']['B2']):.0e})")
    if i < n:
        new = []
        for w in states:
            k1 = rhs(t, w); k2 = rhs(t+dt/2, w+dt/2*k1); k3 = rhs(t+dt/2, w+dt/2*k2); k4 = rhs(t+dt, w+dt*k3)
            new.append(w + dt/6*(k1+2*k2+2*k3+k4))
        states = new; t += dt
json.dump(out, open("results/reduced_family_t20.json", "w"))
