"""Exact algebra and numerical checks of an unvalidated synthetic RC model."""
from fractions import Fraction as F
import numpy as np
import pytest
from scipy.linalg import expm
from scipy.integrate import quad
from physiology.rc_network import RCNetwork, example, closed_total


def rational_derivatives(C):
    # Independent junction elimination with Fraction conductances.
    g0 = g1 = g2 = F(1); total = g0 + g1 + g2
    block = [[g1-g1*g1/total, -g1*g2/total],
             [-g1*g2/total, g2-g2*g2/total]]
    L = [[F(0) for _ in range(4)] for _ in range(4)]
    for offset in (0, 2):
        for i in range(2):
            for j in range(2): L[offset+i][offset+j] = block[i][j]
    p = [F(1)] * 4; derivatives = []
    for _ in range(4):
        derivatives.append(sum(F(C[i])*p[i] for i in range(4)))
        p = [-sum(L[i][j]*p[j] for j in range(4))/C[i] for i in range(4)]
    return L, derivatives


def test_exact_derivatives_and_matched_initialization():
    lg, dg = rational_derivatives([1, 1, 2, 2]); lm, dm = rational_derivatives([1, 2, 1, 2])
    assert dg == [F(6), -F(4, 3), F(1, 3), -F(5, 54)]
    assert dm == [F(6), -F(4, 3), F(1, 3), -F(1, 9)]
    assert (dg[3]-dm[3])/6 == F(1, 324)
    assert lg == lm
    for name in ('grouped', 'mixed'):
        model = example(name);L, b = model.conductance()
        np.testing.assert_allclose(L, np.array(lg, dtype=float), atol=2e-16, rtol=0)
        np.testing.assert_allclose(b, [1/3]*4, atol=1e-16, rtol=0)
        assert np.linalg.eigvalsh(L).min() > 0
        state = model.instantaneous(1.)
        assert state['volume'].sum() == 6
        assert state['energy'] == 3
        assert sorted(model.compliance) == [1, 1, 2, 2]
        assert sorted(np.array(model.compliance)*model.terminal_resistance) == [1, 1, 2, 2]


@pytest.mark.parametrize('name', ['grouped','mixed'])
def test_full_trajectory_against_closed_form_and_scipy(name):
    model = example(name);t = np.linspace(0, 4, 81);p = model.pressures(t)
    total = np.array(model.compliance) @ p
    np.testing.assert_allclose(total, closed_total(t, name), atol=5e-14, rtol=3e-14)
    L, _ = model.conductance();A = L / np.array(model.compliance)[:, None]
    reference = np.column_stack([expm(-A*x) @ np.ones(4) for x in t])
    np.testing.assert_allclose(p, reference, atol=3e-14, rtol=3e-14)


def test_fixed_t1_endpoint_against_independent_hyperbolic_formula():
    g, m = example('grouped'), example('mixed')
    numeric = (np.array(g.compliance) @ g.pressures([1.]) - np.array(m.compliance) @ m.pressures([1.]))[0]/6
    vg = 2*np.exp(-1/3)+4*np.exp(-1/6)
    vm = np.exp(-.5)*(6*np.cosh(1/(2*np.sqrt(3)))+10/np.sqrt(3)*np.sinh(1/(2*np.sqrt(3))))
    assert numeric == pytest.approx((vg-vm)/6, abs=3e-15)


@pytest.mark.parametrize('name', ['grouped','mixed'])
def test_contracted_control_matches_independent_compartments(name):
    model = example(name, contracted=True);t = np.linspace(0, 4, 31)
    C = np.array(model.compliance)
    expected = np.exp(-t[None,:]/C[:,None])
    np.testing.assert_allclose(model.pressures(t), expected, atol=1e-15, rtol=2e-15)
    np.testing.assert_allclose(C @ model.pressures(t), 2*np.exp(-t)+4*np.exp(-t/2), atol=3e-15)
    np.testing.assert_allclose(closed_total(t,name,contracted=True), 2*np.exp(-t)+4*np.exp(-t/2))


def test_zero_trunk_limit_and_aggregate_invariance():
    t = np.linspace(0,4,17)
    a = example('grouped',contracted=True);b = example('mixed',contracted=True)
    np.testing.assert_allclose(np.array(a.compliance)@a.pressures(t),np.array(b.compliance)@b.pressures(t),atol=2e-15)
    near = RCNetwork(a.compliance,trunk_resistance=(1e-8,1e-8))
    np.testing.assert_allclose(near.pressures(t),a.pressures(t),atol=2e-8,rtol=0)


def test_relabel_entire_graph_parameters_state_and_outputs():
    model = RCNetwork((1,2,3,4),(1,2,4,3),(1,2));order = np.array([2,0,3,1])
    other = model.relabeled(order);p0=np.array([1.,.3,.7,.2]);t=np.linspace(0,3,11)
    L,b=model.conductance();L2,b2=other.conductance()
    np.testing.assert_allclose(L2,L[np.ix_(order,order)])
    np.testing.assert_allclose(b2,b[order])
    np.testing.assert_allclose(other.pressures(t,p0[order],.2),model.pressures(t,p0,.2)[order],atol=2e-14)
    s=model.instantaneous(p0,.2);r=other.instantaneous(p0[order],.2)
    np.testing.assert_allclose(r['terminal_flow'],s['terminal_flow'][order])
    for key in ('energy','dissipation','boundary_power','energy_derivative'):
        assert r[key] == pytest.approx(s[key],abs=1e-14)


@pytest.mark.parametrize('trunk', [(1.,1.),(0.,0.),(.3,2.)])
@pytest.mark.parametrize('P', [0.,.7])
def test_conservation_energy_and_resistor_laws(trunk,P):
    model=RCNetwork((1,2,1,2),trunk_resistance=trunk);p=np.array([1.,.2,.7,.4]);s=model.instantaneous(p,P)
    L,b=model.conductance()
    np.testing.assert_allclose(np.array(model.compliance)*s['pressure_derivative'],-L@p+b*P,atol=5e-16)
    assert np.sum(s['terminal_flow']) == pytest.approx(np.sum(s['trunk_flow']),abs=1e-16)
    for j,(pair,R0) in enumerate(zip(model.groups,trunk)):
        if R0: assert s['trunk_flow'][j] == pytest.approx((P-s['junction_pressure'][j])/R0,abs=5e-16)
    assert s['energy_derivative'] == pytest.approx(s['boundary_power']-s['dissipation'],abs=1e-15)
    assert s['dissipation'] >= 0


@pytest.mark.parametrize('p0', [np.ones(4),np.array([1.,.2,.7,.4])])
def test_passive_decay_and_integrated_energy_balance(p0):
    model=example('mixed');t=np.linspace(0,4,41);p=model.pressures(t,p0)
    energy=.5*np.array(model.compliance)@(p*p)
    assert np.all(np.diff(energy)<0)
    for state in p.T:
        info=model.instantaneous(state)
        assert info['energy_derivative'] < 0
    integral,_=quad(lambda x:model.instantaneous(model.pressures([x],p0)[:,0])['dissipation'],0,4,epsabs=1e-11)
    assert energy[0]-energy[-1] == pytest.approx(integral,abs=1e-11)


def test_constant_boundary_equilibrium_and_segment_chaining():
    model=example('mixed');t=np.array([0.,.5,1.])
    np.testing.assert_allclose(model.pressures(t,.4,.4),.4,atol=1e-16)
    a=model.pressures([.5],1,.2)[:,0]
    np.testing.assert_allclose(model.pressures([.5],a,.2)[:,0],model.pressures([1.],1,.2)[:,0],atol=1e-15)
    p0=np.array([0.,0.,1.,0.]);p=model.pressures([0.,1e-12,1.,1e6],p0)
    assert np.all(p>=0)
    model.instantaneous(p[:,1])
    assert model.pressures([],p0).shape==(4,0)
    np.testing.assert_array_equal(model.pressures([1.,0.,1.],p0)[:,1],p0)


@pytest.mark.parametrize('C', [(0,1,1,1),(-1,1,1,1),(np.nan,1,1,1),(np.inf,1,1,1),(True,)*4,(1j,)*4,(1,2,3),('1',)*4,(1e-320,)*4])
def test_invalid_compliance(C):
    with pytest.raises(ValueError):RCNetwork(C)


@pytest.mark.parametrize('kwargs', [dict(terminal_resistance=(0,1,1,1)),dict(terminal_resistance=(np.inf,)*4),dict(trunk_resistance=(-1,1)),dict(trunk_resistance=(np.nan,1)),dict(groups=((0,1),(1,3))),dict(groups=((0.,1.),(2.,3.)))])
def test_invalid_network_parameters(kwargs):
    with pytest.raises(ValueError):RCNetwork((1,1,2,2),**kwargs)


@pytest.mark.parametrize('times', [[-1],[np.nan],[np.inf],[[1]],['1'],[True],[1j]])
def test_invalid_times(times):
    with pytest.raises(ValueError):example('mixed').pressures(times)


@pytest.mark.parametrize('pressure', [-1,np.nan,np.inf,True,1j,[1,2,3]])
def test_invalid_pressures(pressure):
    model=example('mixed')
    with pytest.raises(ValueError):model.pressures([1],pressure)
    with pytest.raises(ValueError):model.instantaneous(pressure)


def test_unrepresentable_state_and_defensive_copy():
    c=np.array([1.,1.,2.,2.]);model=RCNetwork(c);c[0]=0
    assert model.compliance[0]==1
    with pytest.raises(ValueError):model.pressures([],1e308)
    with pytest.raises(ValueError):model.instantaneous(1e308)
    with pytest.raises(ValueError):model.relabeled([0,0,2,3])
    with pytest.raises(ValueError):example('unknown')
