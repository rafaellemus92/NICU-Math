# api/app/bayes.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import numpy as np

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


# ---------- Shared shapes ----------

class ScenarioRequest(BaseModel):
    question: str
    inputs: Dict[str, Any]
    n_samples: int = Field(5000, ge=100, le=20000)
    seed: Optional[int] = None
    return_samples: bool = False


class ScenarioResponse(BaseModel):
    outcome_name: str
    summary: Dict[str, float]
    hist_bins: Optional[List[float]] = None
    hist_counts: Optional[List[int]] = None
    samples_preview: Optional[List[float]] = None
    assumptions: Dict[str, Any]


@dataclass
class SimResult:
    p: np.ndarray
    name: str
    assumptions: Dict[str, Any]


# ---------- Simple helper utilities ----------

def _rng(seed: Optional[int]) -> np.random.Generator:
    return np.random.default_rng(None if seed is None else int(seed))


def _summarize(p: np.ndarray) -> Dict[str, float]:
    return {
        "mean": float(np.mean(p)),
        "p50":  float(np.quantile(p, 0.50)),
        "p05":  float(np.quantile(p, 0.05)),
        "p95":  float(np.quantile(p, 0.95)),
    }


def _hist(p: np.ndarray) -> Dict[str, Any]:
    counts, bins = np.histogram(p, bins=40, range=(0.0, 1.0))
    return {"hist_counts": counts.tolist(), "hist_bins": bins.tolist()}


# ---------- Toy domain models (logistic links with noise) ----------
# These are deliberately simple and transparent so you can replace with your
# own coefficients later. All produce a probability in [0,1].

def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _extubation_model(rng: np.random.Generator, n: int, x: Dict[str, Any]) -> SimResult:
    # Baseline log-odds, then feature contributions (rough priors – tune freely)
    logit = -0.2
    logit += 0.05 * (float(x.get("gest_age_wk", 28.0)) - 28.0)
    logit += -0.06 * max(0.0, float(x.get("fio2", 0.30)) - 0.30) * 100  # per 0.01 above 0.30
    logit += -0.03 * (float(x.get("last_pco2", 55.0)) - 55.0)
    logit +=  0.25 * (1.0 if x.get("caffeine_on", True) else 0.0)
    logit += -0.4  * (1.0 if x.get("prior_failed_extubation", False) else 0.0)
    logit += -0.05 * (float(x.get("apnea_events_12h", 2)) - 2)

    # Per-sample random effect
    eps = rng.normal(loc=0.0, scale=0.6, size=n)
    p = _sigmoid(logit + eps)

    return SimResult(
        p=p,
        name="Probability of successful extubation (no re-intubation in 48–72h)",
        assumptions={
            "link": "logistic",
            "noise_sd": 0.6,
            "notes": "Toy model for demo; replace with calibrated coefficients as desired."
        },
    )


def _nec_model(rng: np.random.Generator, n: int, x: Dict[str, Any]) -> SimResult:
    logit = -2.6  # ~7% baseline
    logit += -0.04 * (float(x.get("gest_age_wk", 28.0)) - 28.0)
    logit +=  0.20 * (1.0 if x.get("prbc_last48h", False) else 0.0)
    logit +=  0.15 * (1.0 if x.get("uac_present", False) else 0.0)
    logit +=  0.18 * (1.0 if x.get("pressors", False) else 0.0)
    logit += -0.15 * (1.0 if x.get("probiotic", False) else 0.0)
    # Feeds/milk categorical bumps (completely illustrative)
    feeds = str(x.get("feeds", "advancing"))
    milk  = str(x.get("milk", "human"))
    logit += {"none": -0.2, "trophic": 0.05, "advancing": 0.15, "full": 0.25}.get(feeds, 0.0)
    logit += {"human": -0.1, "fortified_human": 0.0, "formula": 0.15, "mixed": 0.05}.get(milk, 0.0)

    eps = rng.normal(loc=0.0, scale=0.5, size=n)
    p = _sigmoid(logit + eps)

    return SimResult(
        p=p,
        name="Probability of NEC in next 72h",
        assumptions={"link": "logistic", "noise_sd": 0.5, "notes": "Illustrative prior."},
    )


def _metabolic_acidosis_model(rng: np.random.Generator, n: int, x: Dict[str, Any]) -> SimResult:
    logit = -1.2
    logit += -0.05 * (float(x.get("serum_bicarb", 18.0)) - 18.0)
    logit +=  0.25 * (1.0 if x.get("suspected_sepsis", True) else 0.0)
    logit +=  0.08 * (float(x.get("tpn_arg_load_g_per_kg", 1.2)) - 1.2)
    eps = rng.normal(loc=0.0, scale=0.5, size=n)
    p = _sigmoid(logit + eps)

    return SimResult(
        p=p,
        name="Risk of metabolic acidosis in 48h",
        assumptions={"link": "logistic", "noise_sd": 0.5, "notes": "Illustrative prior."},
    )


def _run_model(req: ScenarioRequest, model_fn) -> ScenarioResponse:
    rng = _rng(req.seed)
    sim = model_fn(rng, int(req.n_samples), req.inputs)

    payload: Dict[str, Any] = {
        "outcome_name": sim.name,
        "summary": _summarize(sim.p),
        **_hist(sim.p),
        "assumptions": {**sim.assumptions,
                        "validation_status": "unvalidated toy model",
                        "scope": "synthetic research and education only; not treatment guidance"},
    }
    if req.return_samples:
        payload["samples_preview"] = sim.p[:100].tolist()
    return ScenarioResponse(**payload)


# ---------- Routes ----------

@router.post("/scenario/extubation", response_model=ScenarioResponse, tags=["scenario"])
def extubation(req: ScenarioRequest) -> ScenarioResponse:
    return _run_model(req, _extubation_model)


@router.post("/scenario/nec", response_model=ScenarioResponse, tags=["scenario"])
def nec(req: ScenarioRequest) -> ScenarioResponse:
    return _run_model(req, _nec_model)


@router.post("/scenario", response_model=ScenarioResponse, tags=["scenario"])
def metabolic_acidosis(req: ScenarioRequest) -> ScenarioResponse:
    # default generic endpoint used by your UI's "Metabolic acidosis (48h)"
    return _run_model(req, _metabolic_acidosis_model)