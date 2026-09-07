"""Optional local Streamlit UI. Install with: pip install -e .[app]"""
from __future__ import annotations

import json

try:
    import streamlit as st
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install the optional app dependency: pip install -e .[app]") from exc

from .evaluator import analyze_case

st.set_page_config(page_title="DIKWP DesireBalance OS", layout="wide")
st.title("DIKWP DesireBalance OS")
st.caption("Desire metrology, sustainable prosperity conversion, and anti-involution planning. Not a social scoring system.")
raw = st.text_area("Paste a case JSON", height=360)
if st.button("Analyze") and raw:
    report = analyze_case(json.loads(raw))
    st.metric("Mean Desire Quality", report["summary"]["mean_desire_quality_index"])
    st.metric("Mean Involution Pressure", report["summary"]["mean_involution_pressure_index"])
    st.json(report)
