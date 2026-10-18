"""Sup norms of the reduced (b = 0) base flow over time, and the Gronwall integrals that
an explicit perturbation bound needs.

u0 = (U, 0, w), U = a e^{-nu t} sin y, w = Re[wh(y,t) e^{ix}].
  ||u0||_inf     <= max_y sqrt(U^2 + |wh|^2)
  ||grad u0||_inf <= max_y sqrt(U'^2 + |wh|^2 + |wh_y|^2)        (Frobenius; w_x = Re[i wh e^{ix}])
Integrals:
  I1(T) = int_0^T ||grad u0||_inf dt                 (L^2 Gronwall exponent/2 for the perturbation)
  I2(T) = int_0^T (2 B^2/nu - nu) dt, B = ||u0||_inf + ||grad u0||_inf   (H^1 Riccati exponent)
  J(T)  = int_0^T exp(2 int_0^s (2B^2/nu - nu)) ds   (the Riccati denominator integral), reported as log10.
Run: python3 base_flow_norms.py [a] [T]   (a = c = d; default 1, T = 400 viscous plus the inviscid run)
"""
import numpy as np, math

def integrate(a, c, d, phi, nu, T, M=128, dt=2e-3, every=50):
    y = 2*np.pi*np.arange(M)/M
    k = np.fft.fftfreq(M)*M
    wh = c - d*np.exp(1j*(y+phi))
    def rhs(t, wh):
        U = a*np.exp(-nu*t)*np.sin(y)
        return -1j*U*wh + nu*np.fft.ifft(-(k**2+1)*np.fft.fft(wh))
    n = int(round(T/dt)); t = 0.0
    ts, sup_u, sup_g, l2g, sup_h = [], [], [], [], []
    for i in range(n+1):
        if i % every == 0:
            U = a*np.exp(-nu*t)*np.sin(y); Up = a*np.exp(-nu*t)*np.cos(y); Upp = -U
            whh = np.fft.fft(wh)
            why = np.fft.ifft(1j*k*whh); whyy = np.fft.ifft(-(k**2)*whh)
            ts.append(t)
            sup_u.append(float(np.max(np.sqrt(U**2 + np.abs(wh)**2))))
            sup_g.append(float(np.max(np.sqrt(Up**2 + np.abs(wh)**2 + np.abs(why)**2))))
            # second derivatives: U'', w_xx = -w, w_xy, w_yy  (Frobenius bound over x at each y)
            sup_h.append(float(np.max(np.sqrt(Upp**2 + np.abs(wh)**2 + 2*np.abs(why)**2 + np.abs(whyy)**2))))
            l2g.append(float(np.sqrt((2*np.pi)**3 * (np.mean(Up**2) + 0.5*np.mean(np.abs(wh)**2 + np.abs(why)**2)))))  # ||grad u0||_{L^2} on the 2pi box
        if i < n:
            k1 = rhs(t, wh); k2 = rhs(t+dt/2, wh+dt/2*k1); k3 = rhs(t+dt/2, wh+dt/2*k2); k4 = rhs(t+dt, wh+dt*k3)
            wh = wh + dt/6*(k1+2*k2+2*k3+k4); t += dt
    return np.array(ts), np.array(sup_u), np.array(sup_g), np.array(l2g), np.array(sup_h)

if __name__ == "__main__":
    import sys
    a = c = d = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    print(f"amplitudes a = c = d = {a}")
    cases = ((1/28, 400.0), (0.0, 20.0)) if len(sys.argv) <= 2 else ((1/28, float(sys.argv[2])),)
    for nu, T in cases:
        print(f"=== nu = {nu:.5f}, phi = 0 (the cos phi = +1 member; other phases below)")
        ts, su, sg, l2, sh = integrate(a, c, d, 0.0, nu, T)
        imax = int(np.argmax(sg))
        print(f"  ||grad u0||_inf: max {sg[imax]:.3f} at t = {ts[imax]:.2f};  at t=0 {sg[0]:.3f};  at T {sg[-1]:.2e};  ||u0||_inf max {su.max():.3f};  ||grad^2 u0||_inf max {sh.max():.3f} at t = {ts[int(np.argmax(sh))]:.2f}")
        I1 = np.trapezoid(sg, ts)
        if nu > 0:
            G = 2*sg + sh                           # coefficient after integrating by parts: 2||grad u0||_inf + ||grad^2 u0||_inf
            A = 2*G - nu
            cumA = np.concatenate([[0.0], np.cumsum(0.5*(A[1:]+A[:-1])*np.diff(ts))])
            Phi2_log = 2*cumA                      # log Phi(s)^2
            m = Phi2_log.max()
            log10J = (m + math.log(np.trapezoid(np.exp(Phi2_log - m), ts)))/math.log(10)
            print(f"  I1 = int ||grad u0||_inf dt = {I1:.3f}  (L^2 amplification bound exp(I1) = 1e{I1/math.log(10):.1f})")
            print(f"  int ||grad^2 u0||_inf dt = {np.trapezoid(sh, ts):.3f}")
            print(f"  int (2G - nu) dt, G = 2||grad u0||_inf + ||grad^2 u0||_inf:  total {cumA[-1]:.1f};  max over t {cumA.max():.1f} at t = {ts[int(np.argmax(cumA))]:.2f};  log10 Phi_max = {cumA.max()/math.log(10):.1f}")
            print(f"  log10 J = log10 int Phi^2 = {log10J:.1f}")
            for tt in (1, 2, 5, 10, 20, 50, 100, 200, 400):
                j = int(np.searchsorted(ts, tt)); j = min(j, len(ts)-1)
                print(f"     t={tt:4d}: ||grad u0||_inf {sg[j]:.3f} ||grad^2 u0||_inf {sh[j]:.3f}  int_0^t ||grad u0||_inf {np.trapezoid(sg[:j+1], ts[:j+1]):.2f}  log10 Phi(t) {cumA[j]/math.log(10):.1f}")
            # phase dependence of the exponents
            for phi in (math.pi/2, math.pi):
                ts2, su2, sg2, _, sh2 = integrate(a, c, d, phi, nu, T)
                G2 = 2*sg2 + sh2
                print(f"  phi = {phi:.3f}: max ||grad u0||_inf {sg2.max():.3f}, I1 = {np.trapezoid(sg2, ts2):.3f}, int (2G - nu) = {np.trapezoid(2*G2 - nu, ts2):.1f}")
            np.savez(f"base_flow_norms_a{a}.npz", ts=ts, sup_u=su, sup_g=sg, sup_h=sh, log10J=log10J, cumA=cumA)
        else:
            print(f"  inviscid: ||grad u0||_inf at t = 5, 10, 20: {sg[np.searchsorted(ts, 5)]:.2f}, {sg[np.searchsorted(ts, 10)]:.2f}, {sg[-1]:.2f}  (grows like a t: w_y ~ t)")
            print(f"  I1(T) = {I1:.1f} at T = {T}  (~ T^2/2 growth: no uniform-in-T constant)")
