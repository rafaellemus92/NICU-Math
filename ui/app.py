# ui/app.py
import os
import requests
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

DEFAULT_TIMEOUT = (5, 60)

session = requests.Session()

def api_get(path: str):
    return session.get(f"{API_URL}{path}", timeout=DEFAULT_TIMEOUT)

def api_post(path: str, json: dict):
    return session.post(f"{API_URL}{path}", json=json, timeout=DEFAULT_TIMEOUT)

st.set_page_config(page_title="NICU Evidence", layout="wide")
st.title("NICU Synthetic Research & Scenario Engine")
st.warning("Synthetic research and education only. Do not enter patient data. "
           "Models are unvalidated and must not guide treatment.")

# ---- Health badge ----
health = "unknown"
try:
    rz = api_get("/healthz")
    if rz.ok and rz.json().get("status") == "ok":
        health = "ok"
except Exception:
    health = "down"

st.caption(f"API: `{API_URL}` • health: {'✅ ok' if health=='ok' else '❌ down'}")

tab1, tab2 = st.tabs(["🔎 Evidence", "🧮 Scenario (Bayes)"])

# ----------------------------- Evidence tab -----------------------------
with tab1:
    st.subheader("Explore a synthetic research question")
    st.caption("Evidence retrieval is disabled in the default offline mode.")
    q = st.text_input("Question or keywords", placeholder="e.g., causes of neonatal metabolic acidosis")
    k = st.slider("Top results", 3, 12, 6)

    go = st.button("Search & Answer", type="primary")

    if go and q.strip():
        try:
            r = api_post("/answer", {"query": q, "k": k})
            r.raise_for_status()
            data = r.json()

            st.markdown("### Answer")
            st.markdown(data.get("answer_markdown", "_No answer_"))

            st.markdown("### Sources")
            for s in data.get("sources", []):
                title = s.get("title") or s.get("path") or "document"
                score = s.get("score")
                label = f"{title}" + (f" • score {score:.3f}" if isinstance(score, (int, float)) else "")
                with st.expander(label):
                    excerpt = s.get("excerpt") or s.get("content") or ""
                    st.write(excerpt)

        except Exception as e:
            st.error(f"API error: {e}")

# ----------------------------- Scenario (Bayes) tab -----------------------------
with tab2:
    st.subheader("Monte Carlo scenario")

    model = st.selectbox(
        "Model",
        ["Metabolic acidosis (48h)", "NEC (72h)", "Extubation success (48–72h)"],
        index=0,
    )

    cols = st.columns([1,1,1,1])
    n_samples = st.slider("Samples", 1000, 20000, 5000, step=500)
    seed = st.number_input("Seed (optional)", value=42, step=1)

    payload = None
    endpoint = None
    title = ""

    if model.startswith("Metabolic"):
        title = "Metabolic acidosis in 48h"
        c1,c2,c3 = st.columns(3)
        ga = c1.number_input("Gestational age (weeks)", 22.0, 42.0, 28.0, step=0.5)
        bw = c2.number_input("Birth weight (g)", 300, 6000, 900, step=10)
        arg = c3.number_input("TPN arginine load (g/kg)", 0.0, 5.0, 1.2, step=0.1)
        sepsis = st.toggle("Suspected sepsis", value=True)
        c4,c5 = st.columns(2)
        hco3 = c4.number_input("Serum HCO₃⁻ (mmol/L) (optional)", 5.0, 40.0, 18.0, step=0.5)
        upH  = c5.number_input("Urine pH (optional)", 4.5, 9.0, 6.5, step=0.1)

        endpoint = "/scenario"
        payload = {
            "question": "Risk of metabolic acidosis in next 48h",
            "inputs": {
                "gest_age_wk": ga,
                "birth_weight_g": int(bw),
                "tpn_arg_load_g_per_kg": float(arg),
                "suspected_sepsis": bool(sepsis),
                "serum_bicarb": float(hco3),
                "urine_pH": float(upH),
            },
            "n_samples": int(n_samples),
            "seed": int(seed),
            "return_samples": False
        }

    elif model.startswith("NEC"):
        title = "NEC in 72h"
        c1,c2,c3 = st.columns(3)
        ga = c1.number_input("Gestational age (weeks)", 22.0, 42.0, 28.0, step=0.5)
        bw = c2.number_input("Birth weight (g)", 300, 6000, 900, step=10)
        dol = c3.number_input("Day of life", 0, 120, 7, step=1)
        c4,c5 = st.columns(2)
        feeds = c4.selectbox("Feeds", ["none","trophic","advancing","full"], index=2)
        milk  = c5.selectbox("Milk", ["human","fortified_human","formula","mixed"], index=0)
        probiotic = st.toggle("Probiotic", value=False)
        c6,c7,c8,c9 = st.columns(4)
        prbc = c6.toggle("PRBC in last 48h", value=False)
        uac  = c7.toggle("UAC present", value=False)
        press = c8.toggle("On pressors", value=False)
        abx = c9.toggle("Recent antibiotics", value=False)
        pda = st.toggle("PDA", value=False)

        endpoint = "/scenario/nec"
        payload = {
            "question": "Probability of NEC in next 72h",
            "inputs": {
                "gest_age_wk": ga, "birth_weight_g": int(bw), "day_of_life": int(dol),
                "feeds": feeds, "milk": milk, "probiotic": probiotic,
                "prbc_last48h": prbc, "uac_present": uac, "pressors": press,
                "recent_abx": abx, "pda": pda
            },
            "n_samples": int(n_samples),
            "seed": int(seed),
            "return_samples": False
        }

    else:  # Extubation
        title = "Extubation success (no re-intubation in 48–72h)"
        c1,c2,c3 = st.columns(3)
        ga = c1.number_input("Gestational age (weeks)", 22.0, 42.0, 28.0, step=0.5)
        pna = c2.number_input("Postnatal age (days)", 0, 180, 14, step=1)
        peep = c3.number_input("Current PEEP", 3.0, 10.0, 5.0, step=0.5)
        c4,c5,c6 = st.columns(3)
        fio2 = c4.number_input("FiO₂", 0.21, 1.0, 0.30, step=0.01)
        pco2 = c5.number_input("Last pCO₂", 20.0, 100.0, 55.0, step=1.0)
        ph = c6.number_input("Last pH", 7.10, 7.55, 7.32, step=0.01)
        c7,c8,c9 = st.columns(3)
        apnea = c7.number_input("Apnea events (12h)", 0, 50, 2, step=1)
        caffeine = c8.toggle("Caffeine on", value=True)
        prior_fail = c9.toggle("Prior failed extubation", value=False)

        endpoint = "/scenario/extubation"
        payload = {
            "question": "Probability of successful extubation (no re-intubation in 48–72h)",
            "inputs": {
                "gest_age_wk": ga, "postnatal_age_d": int(pna),
                "current_peep": float(peep), "fio2": float(fio2),
                "last_pco2": float(pco2), "last_pH": float(ph),
                "apnea_events_12h": int(apnea),
                "caffeine_on": bool(caffeine),
                "prior_failed_extubation": bool(prior_fail),
            },
            "n_samples": int(n_samples),
            "seed": int(seed),
            "return_samples": False
        }

    run = st.button("Run", type="primary")
    if run and payload and endpoint:
        try:
            r = api_post(endpoint, payload)
            r.raise_for_status()
            data = r.json()

            st.markdown(f"### {data['outcome_name']}")
            m = data["summary"]
            cA,cB,cC,cD = st.columns(4)
            cA.metric("Mean", f"{m['mean']*100:.1f}%")
            cB.metric("Median (p50)", f"{m['p50']*100:.1f}%")
            cC.metric("p05", f"{m['p05']*100:.1f}%")
            cD.metric("p95", f"{m['p95']*100:.1f}%")

            if data.get("hist_bins") and data.get("hist_counts"):
                bins = data["hist_bins"]; counts = data["hist_counts"]
                mids = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]
                df = pd.DataFrame({"prob": mids, "count": counts})
                chart = (
                    alt.Chart(df)
                    .mark_bar()
                    .encode(
                        x=alt.X("prob:Q", title="Probability", scale=alt.Scale(domain=[0,1])),
                        y=alt.Y("count:Q", title="Count"),
                        tooltip=["prob","count"]
                    )
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No histogram returned; showing preview only.")
                st.bar_chart(pd.Series(data.get("samples_preview", [])))

            with st.expander("Assumptions"):
                st.json(data.get("assumptions", {}))
            with st.expander("Raw response"):
                st.json(data)
        except Exception as e:
            st.error(f"API error: {e}")
