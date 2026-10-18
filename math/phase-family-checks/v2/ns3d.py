"""3D periodic NS, pseudo-spectral, strict 2/3 dealiasing K=(N-1)//3, Lawson RK4. Torus-average diagnostics E, Z, S."""
import numpy as np
class NS:
    def __init__(self, N, nu, dt):
        self.N, self.nu, self.dt = N, nu, dt
        k1 = np.fft.fftfreq(N, 1/N); kx, ky, kz = np.meshgrid(k1, k1, k1, indexing='ij')
        self.K = np.array([kx, ky, kz]); self.k2 = kx**2+ky**2+kz**2; self.k2n = np.where(self.k2 == 0, 1, self.k2)
        kmax = (N-1)//3; self.deal = (abs(kx) <= kmax) & (abs(ky) <= kmax) & (abs(kz) <= kmax)
        x = np.arange(N)*2*np.pi/N; self.X, self.Y, self.Z = np.meshgrid(x, x, x, indexing='ij')
        self.E_ = np.exp(-nu*self.k2*dt); self.Eh = np.exp(-nu*self.k2*dt/2)
    fft = staticmethod(lambda f: np.fft.fftn(f, axes=(1, 2, 3)))
    ifft = staticmethod(lambda f: np.real(np.fft.ifftn(f, axes=(1, 2, 3))))
    def curl(self, uh):
        kx, ky, kz = self.K; return 1j*np.array([ky*uh[2]-kz*uh[1], kz*uh[0]-kx*uh[2], kx*uh[1]-ky*uh[0]])
    def proj(self, fh): return fh - self.K*(np.sum(self.K*fh, axis=0)/self.k2n)
    def nonlin(self, uh):
        ur = self.ifft(uh); om = self.ifft(self.curl(uh)); return -self.proj(self.fft(np.cross(om, ur, axis=0))*self.deal)
    def init(self, a, b, c, d, phi):
        X, Y, Z = self.X, self.Y, self.Z
        return self.fft(np.array([a*np.sin(Y), b*np.sin(Z), c*np.cos(X) - d*np.cos(X+Y+phi)]))*self.deal
    def step(self, uh):
        E_, Eh, dt = self.E_, self.Eh, self.dt
        a1 = self.nonlin(uh); a2 = self.nonlin(Eh*(uh+dt/2*a1)); a3 = self.nonlin(Eh*uh+dt/2*a2); a4 = self.nonlin(E_*uh+dt*Eh*a3)
        return E_*uh + dt/6*(E_*a1 + 2*Eh*(a2+a3) + a4)
    def diag(self, uh):
        N = self.N; oh = self.curl(uh); om = self.ifft(oh)
        E = 0.5*np.sum(abs(uh)**2)/N**6; Z = 0.5*np.sum(abs(oh)**2)/N**6
        S = sum(np.mean(om[i]*om[j]*np.real(np.fft.ifftn(1j*self.K[j]*uh[i]))) for i in range(3) for j in range(3))
        return E, Z, S
    def run(self, a, b, c, d, phi, checkpoints):
        uh = self.init(a, b, c, d, phi); out = {}; t = 0.0; n = int(round(max(checkpoints)/self.dt))
        for _ in range(n):
            uh = self.step(uh); t += self.dt
            for T in checkpoints:
                if abs(t-T) < self.dt/2: out[T] = self.diag(uh)
        return out
