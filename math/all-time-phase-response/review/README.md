# review: the computations behind the review

The review of this folder (summarised in
[../README.md](../README.md#how-this-fits-the-repository)) quotes some numbers
that are not in the package's own results. The scripts here compute them, and
the logs are their saved output. They were written by Claude for the review
on 18 October 2026 and are not part of the ChatGPT/Codex delivery.

Run each from this folder, with Python 3 and NumPy:

```sh
python3 -I -B exact_b2_check.py > exact_b2_check.log
python3 -I -B audit_t1_check.py > audit_t1_check.log
python3 -I -B radius_ceiling.py > radius_ceiling.log
python3 -I -B longtime_ratio.py > longtime_ratio.log
```

They import [`../response.py`](../response.py) (and through it
[`../../ns-phase-audit/audit_v2/dns/ns.py`](../../ns-phase-audit/audit_v2/dns/ns.py))
and read
[`../../ns-phase-audit/audit_v2/exact/nsseries.py`](../../ns-phase-audit/audit_v2/exact/nsseries.py),
[`../../ns-phase-audit/audit_v2/xcheck/p1_finite_time.log`](../../ns-phase-audit/audit_v2/xcheck/p1_finite_time.log)
and [`../../ns-phase-audit/audit_v2/AUDIT.md`](../../ns-phase-audit/audit_v2/AUDIT.md).
The other files are unchanged. This integration edits AUDIT.md only in §4.2
(the P1 solution-level row, which now cites this folder), §7.1 and §7.5. The
§4.3 row that audit_t1_check.py reads is untouched. The scripts write nothing
except standard output. Times are wall times on one core of the machine used
here (Python 3.13, NumPy 2.5); a rerun reproduces every number in the logs
except the timings.

| Script | Time | What it shows |
|---|---|---|
| [`exact_b2_check.py`](exact_b2_check.py) ([log](exact_b2_check.log)) | about 4 min | Runs the repository's exact series (ν symbolic; E and Z through t¹⁰, S through t⁹) at 14 rational b and interpolates exactly in b. All 943 coefficients (one per observable, order, harmonic and power of ν) of E, Z and S are even in b (the held-out b and the degree bound check the interpolation). (E2, Z2, S2)(0) = (1/4, 1/4, 0) for every ν and φ. [t⁶] cos 2φ of Z2 is −6487/1555200. Within the computed orders, each \|m\| ≥ 2 harmonic of the b², b⁴ and b⁶ parts first appears at the earliest order that wavevector counting allows (PROOF.md section 5 states the rule for b² and b⁴; in E it comes with a factor ν), and the b = 0 part keeps \|m\| ≤ 1. The b⁴ terms start at (13/216)t³ in S, (13/864)t⁴ in Z and −(13ν/2160)t⁵ in E. `response.py` (N = 48, dt = 0.00125, φ = 0.37, ν = 1/28) matches the series to 13–15 digits for E2 and Z2 at t ≤ 0.1, and for S2 to about 13 digits at t ≤ 0.05 and to 1.1e−12 at t = 0.1, below the last series term (3.6e−12). |
| [`audit_t1_check.py`](audit_t1_check.py) ([log](audit_t1_check.log)) | about 1 min | Reads the finite-β values of [AUDIT.md](../../ns-phase-audit/audit_v2/AUDIT.md) §4.3 from their log, checks that AUDIT.md quotes them, and extrapolates c2/β² to β → 0 (−1.2077213e−3). The package's variational Z2, Laurent m = 2 at T = 1 on the same N = 24, dt = 0.01 discretisation, is −1.2077219e−3: a relative difference of 4.5e−7, within the 7e−7 that the log's 7 printed digits allow. |
| [`radius_ceiling.py`](radius_ceiling.py) ([log](radius_ceiling.log)) | under 1 s | The ceiling on the radius certified by PROOF.md condition (1) at a = c = d = 1, ν = 1/28: at most 7.2 × 10⁻²² (7.142 × 10⁻²²), at s = 4; it is smaller for every larger s, and the section 4 radius β obeys a smaller ceiling still. The tested b = 0.05 and 0.1 are 7 × 10¹⁹ and 1.4 × 10²⁰ times larger. |
| [`longtime_ratio.py`](longtime_ratio.py) ([log](longtime_ratio.log)) | about 3.5 min | Runs the package's b⁴ check (b = 0.1 and 0.05, φ = 0.37, dt = 0.005) past T = 0.5, on 24³ and 32³ grids. The ratio \|R(0.1)\|/\|R(0.05)\| stays within 0.05% of 16 up to t = 1, within 2.4% at t = 2 on 32³ (5.2% on 24³, which is under-resolved there), and leaves the pre-set 14–18 window by t = 4 on both grids (Z 18.0–18.2, S 13.6–13.7). |

## The radius ceiling and its assumptions

The ceiling uses only that the largest |b| condition (1) allows,
ν e^(−K_s∫M_s)/(2K_s F_s), decreases in K_s and in ∫M_s; that K_s must
satisfy section 2's second inequality for the test pair f = sin(y) e_x,
h = sin(z) e_y; and that M_s is at least the norm of the shear part of U. So
it holds whatever values the uncomputed constants take. Smaller figures that
the review obtained from a numerically computed base integral, or from the
appendix majorant, are not quoted in this folder because nothing here
reproduces them.

## What these do not show

All four are checks of the second-order formulas, of the finite systems or of
the size of the radius. None tests the theorem's all-time bounds or its decay
rates: the theorem applies only to b far smaller than anything a full
double-precision solve can resolve, and nothing here concerns b = 1,
statement (B) or the Millennium problem.
