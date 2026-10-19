"""Passive four-terminal RC teaching network; no patient prediction.

Two massless junctions, each feeding two terminal compliances, share a prescribed
pressure boundary. Units: pressure cmH2O, volume mL, time seconds; R is
pressure*time/volume, C volume/pressure. Volumes are excess elastic volumes.
Closed matrix-exponential formulas are evaluated approximately in float64.
See rc_network.md for assumptions, conservation and limits. NumPy only.
"""
from dataclasses import dataclass
import numpy as np


def _array(value, name, shape, *, positive=False):
    a = np.asarray(value)
    if a.shape != shape or a.dtype.kind not in 'iuf':
        raise ValueError(f'{name} must be a real numeric array of shape {shape}')
    a = a.astype(float, copy=True)
    if not np.isfinite(a).all() or np.any(a <= 0 if positive else a < 0):
        raise ValueError(f'{name} must be finite and {"positive" if positive else "nonnegative"}')
    return a


def _scalar(value, name):
    return float(_array(value, name, ()))


def _times(value):
    a = np.asarray(value)
    if a.ndim != 1:
        raise ValueError('times must be one-dimensional')
    return _array(value, 'times', a.shape)


@dataclass(frozen=True)
class RCNetwork:
    """Four terminal capacitors in two sibling pairs; zero trunk means contraction.

    groups contains each terminal index exactly once. Nonzero trunk and all
    terminal resistances are passive; no node storage except terminal C.
    Input arrays are copied into immutable tuples. Unrepresentable numerical
    matrices are rejected, even when their real-arithmetic model would exist.
    """
    compliance: tuple
    terminal_resistance: tuple = (1., 1., 1., 1.)
    trunk_resistance: tuple = (1., 1.)
    groups: tuple = ((0, 1), (2, 3))

    def __post_init__(self):
        C = _array(self.compliance, 'compliance', (4,), positive=True)
        R = _array(self.terminal_resistance, 'terminal_resistance', (4,), positive=True)
        trunk = _array(self.trunk_resistance, 'trunk_resistance', (2,))
        groups = np.asarray(self.groups)
        if (groups.shape != (2, 2) or groups.dtype.kind not in 'iu'
                or sorted(groups.ravel().tolist()) != list(range(4))):
            raise ValueError('groups must partition indices 0..3 into two pairs')
        object.__setattr__(self, 'compliance', tuple(C))
        object.__setattr__(self, 'terminal_resistance', tuple(R))
        object.__setattr__(self, 'trunk_resistance', tuple(trunk))
        object.__setattr__(self, 'groups', tuple(tuple(int(i) for i in pair) for pair in groups))
        try:
            with np.errstate(over='raise', divide='raise', invalid='raise'):
                L, b = self.conductance()
                root = np.sqrt(C)
                S = L / root[:, None] / root[None, :]
                rates = np.linalg.eigvalsh(S)
                if not (np.isfinite(S).all() and np.isfinite(b).all()
                        and np.all(b > 0) and np.all(rates > 0)):
                    raise ValueError('network is not numerically positive definite')
        except (FloatingPointError, np.linalg.LinAlgError) as exc:
            raise ValueError('network coefficients are not representable') from exc

    def conductance(self):
        """Return L,b in C p'= -L p+b P, with b=L1 analytically."""
        L = np.zeros((4, 4)); b = np.zeros(4)
        for pair, trunk in zip(self.groups, self.trunk_resistance):
            idx = list(pair)
            g = 1 / np.asarray(self.terminal_resistance)[idx]
            if trunk == 0:
                block = np.diag(g); drive = g
            else:
                g0 = 1 / trunk
                total = g0 + g.sum()
                block = np.diag(g) - np.outer(g / total, g)
                drive = (g0 / total) * g
            L[np.ix_(idx, idx)] = block; b[idx] = drive
        return L, b

    def _pressure(self, value, name):
        a = np.asarray(value)
        if a.ndim == 0:
            return np.full(4, _scalar(value, name))
        return _array(value, name, (4,))

    def pressures(self, times, initial_pressure=1., boundary_pressure=0.):
        """Return pressures (4,n) for a constant boundary and scalar/vector p(0).

        For a piecewise-constant waveform, pass each segment's last state to
        the next segment with times relative to its start. Empty/unsorted or
        repeated observation times are permitted; no ODE time stepping occurs.
        Negative roundoff within 64*eps*max(initial,boundary) is floored to
        zero to preserve the passive nonnegative domain; larger violations fail.
        """
        t = _times(times); p0 = self._pressure(initial_pressure, 'initial_pressure')
        P = _scalar(boundary_pressure, 'boundary_pressure')
        C = np.asarray(self.compliance); root = np.sqrt(C)
        L, _ = self.conductance()
        try:
            with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
                if not np.isfinite(C * p0).all() or not np.isfinite(np.sum(C * p0)):
                    raise ValueError('initial excess volume is not representable')
                rates, vectors = np.linalg.eigh(L / root[:, None] / root[None, :])
                if not np.all(rates > 0):
                    raise ValueError('nonpositive numerical relaxation rate')
                # Positive rates: overflow of rate*time means complete decay.
                with np.errstate(over='ignore'):
                    decay = np.exp(-rates[:, None] * t[None, :])
                amplitudes = vectors.T @ (root * (p0 - P))
                p = P + (vectors @ (amplitudes[:, None] * decay)) / root[:, None]
                tolerance = (64 * np.finfo(float).eps) * max(float(np.max(p0)), P)
                if np.any(p < -tolerance):
                    raise ValueError('negative pressure exceeds roundoff allowance')
                p = np.maximum(p, 0.)
                p[:, t == 0] = p0[:, None]
                if not np.isfinite(p).all() or not np.isfinite(C[:, None] * p).all():
                    raise ValueError('pressure/volume trajectory is not representable')
        except (FloatingPointError, np.linalg.LinAlgError) as exc:
            raise ValueError('trajectory is not representable') from exc
        return p

    def instantaneous(self, pressure, boundary_pressure=0.):
        """Flows, derivative, energy and power for one nonnegative state.

        Positive flows point from boundary through trunk toward terminals.
        Energy/power identities use signed flows, including passive outflow.
        """
        p = self._pressure(pressure, 'pressure'); P = _scalar(boundary_pressure, 'boundary_pressure')
        C = np.asarray(self.compliance); R = np.asarray(self.terminal_resistance)
        q = np.zeros(4); junction = np.zeros(2); trunk_flow = np.zeros(2)
        try:
            with np.errstate(over='raise', divide='raise', invalid='raise'):
                for j, (pair, trunk) in enumerate(zip(self.groups, self.trunk_resistance)):
                    idx = list(pair); g = 1 / R[idx]
                    if trunk == 0:
                        junction[j] = P
                    else:
                        g0 = 1 / trunk; total = g0 + g.sum()
                        junction[j] = (g0 / total) * P + (g / total) @ p[idx]
                    q[idx] = g * (junction[j] - p[idx])
                    trunk_flow[j] = q[idx].sum()
                derivative = q / C
                volume = C * p
                energy = .5 * np.dot(volume, p)
                dissipation = np.dot(R, q * q) + np.dot(self.trunk_resistance, trunk_flow * trunk_flow)
                power = P * trunk_flow.sum()
                energy_derivative = np.dot(p, q)
                vals = np.r_[derivative, volume, energy, dissipation, power, energy_derivative]
                if not np.isfinite(vals).all():
                    raise ValueError('state diagnostics are not representable')
        except FloatingPointError as exc:
            raise ValueError('state diagnostics are not representable') from exc
        return dict(terminal_flow=q, trunk_flow=trunk_flow, junction_pressure=junction,
                    pressure_derivative=derivative, volume=volume, energy=energy,
                    dissipation=dissipation, boundary_power=power,
                    energy_derivative=energy_derivative)

    def relabeled(self, order):
        """New index i represents old index order[i]; transform graph and C together."""
        a = np.asarray(order)
        if a.shape != (4,) or a.dtype.kind not in 'iu' or sorted(a.tolist()) != list(range(4)):
            raise ValueError('order must be a permutation of 0..3')
        inverse = np.argsort(a)
        return RCNetwork(tuple(np.asarray(self.compliance)[a]),
                         tuple(np.asarray(self.terminal_resistance)[a]),
                         self.trunk_resistance,
                         tuple(tuple(int(inverse[i]) for i in pair) for pair in self.groups))


def example(arrangement, *, contracted=False):
    """Preregistered unit-resistance example; no parameter fitting."""
    if arrangement not in ('grouped', 'mixed'):
        raise ValueError('arrangement must be grouped or mixed')
    C = (1., 1., 2., 2.) if arrangement == 'grouped' else (1., 2., 1., 2.)
    return RCNetwork(C, trunk_resistance=(0., 0.) if contracted else (1., 1.))


def closed_total(times, arrangement, *, contracted=False):
    """Float64 evaluation of exact total-volume formulas for the fixed example.

    Initial pressure1, release boundary0; units mL. Exponential sums avoid
    overflow/cancellation of the equivalent hyperbolic representation.
    """
    t = _times(times)
    if arrangement not in ('grouped', 'mixed'):
        raise ValueError('arrangement must be grouped or mixed')
    if contracted:
        return 2 * np.exp(-t) + 4 * np.exp(-t / 2)
    if arrangement == 'grouped':
        return 2 * np.exp(-t / 3) + 4 * np.exp(-t / 6)
    s = np.sqrt(3.)
    return (3 + 5 / s) * np.exp(-((1 - 1 / s) / 2) * t) + (3 - 5 / s) * np.exp(-((1 + 1 / s) / 2) * t)


def main():
    import json
    times = np.array([0., .25, .5, 1., 2., 4.])
    result = {'scope': 'synthetic passive linear network; not clinically validated',
              'times_seconds': times.tolist(), 'initial_pressure': 1., 'boundary_pressure': 0.}
    fractions = {}
    for name in ('grouped', 'mixed'):
        model = example(name); p = model.pressures(times)
        volumes = np.asarray(model.compliance)[:, None] * p
        fractions[name] = volumes.sum(axis=0) / 6
        result[name] = {'total_volume': volumes.sum(axis=0).tolist(),
                        'retained_fraction': fractions[name].tolist(),
                        'terminal_volume_at_1': volumes[:, 3].tolist(),
                        'closed_form_max_abs_error': float(np.max(np.abs(volumes.sum(axis=0) - closed_total(times, name))))}
    result['primary_t1_fraction_difference'] = float(fractions['grouped'][3] - fractions['mixed'][3])
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
