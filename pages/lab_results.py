"""Lab Results page - metabolic and cardiovascular lab input."""

import streamlit as st
from health_utils import REFERENCE_RANGES, classify_value, get_status_color


def render():
    st.header("Lab Results")
    st.markdown(
        "Enter your most recent blood work. Leave fields at 0 if you don't "
        "have that test. The key markers below cover metabolic and "
        "cardiovascular risk for founders aged 40-60."
    )

    labs = st.session_state.labs

    # --- Metabolic Panel ---
    st.subheader("Metabolic Panel")
    col1, col2, col3 = st.columns(3)

    with col1:
        fasting_glucose = st.number_input(
            "Fasting Glucose (mg/dL)",
            min_value=0.0,
            max_value=500.0,
            value=float(labs.get("fasting_glucose", 0)),
            step=1.0,
            help="Optimal: 70-99 mg/dL",
        )
    with col2:
        hba1c = st.number_input(
            "HbA1c (%)",
            min_value=0.0,
            max_value=15.0,
            value=float(labs.get("hba1c", 0)),
            step=0.1,
            help="Optimal: 4.0-5.6%",
        )
    with col3:
        fasting_insulin = st.number_input(
            "Fasting Insulin (uIU/mL)",
            min_value=0.0,
            max_value=100.0,
            value=float(labs.get("fasting_insulin", 0)),
            step=0.1,
            help="Optimal: 2-8 uIU/mL",
        )

    # --- Lipid Panel ---
    st.subheader("Lipid Panel")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_cholesterol = st.number_input(
            "Total Cholesterol (mg/dL)",
            min_value=0.0,
            max_value=500.0,
            value=float(labs.get("total_cholesterol", 0)),
            step=1.0,
            help="Optimal: <200 mg/dL",
        )
    with col2:
        ldl = st.number_input(
            "LDL Cholesterol (mg/dL)",
            min_value=0.0,
            max_value=400.0,
            value=float(labs.get("ldl", 0)),
            step=1.0,
            help="Optimal: <100 mg/dL",
        )
    with col3:
        hdl = st.number_input(
            "HDL Cholesterol (mg/dL)",
            min_value=0.0,
            max_value=200.0,
            value=float(labs.get("hdl", 0)),
            step=1.0,
            help="Optimal: >60 mg/dL",
        )
    with col4:
        triglycerides = st.number_input(
            "Triglycerides (mg/dL)",
            min_value=0.0,
            max_value=1000.0,
            value=float(labs.get("triglycerides", 0)),
            step=1.0,
            help="Optimal: <150 mg/dL",
        )

    # --- Cardiovascular ---
    st.subheader("Cardiovascular Markers")
    col1, col2, col3 = st.columns(3)

    with col1:
        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=0.0,
            max_value=250.0,
            value=float(labs.get("systolic_bp", 0)),
            step=1.0,
            help="Optimal: <120 mmHg",
        )
    with col2:
        diastolic_bp = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=0.0,
            max_value=150.0,
            value=float(labs.get("diastolic_bp", 0)),
            step=1.0,
            help="Optimal: <80 mmHg",
        )
    with col3:
        hscrp = st.number_input(
            "hs-CRP (mg/L)",
            min_value=0.0,
            max_value=50.0,
            value=float(labs.get("hscrp", 0)),
            step=0.1,
            help="Optimal: <1.0 mg/L. Marker of systemic inflammation.",
        )

    # --- Traffic light summary ---
    all_labs = {
        "fasting_glucose": fasting_glucose,
        "hba1c": hba1c,
        "fasting_insulin": fasting_insulin,
        "total_cholesterol": total_cholesterol,
        "ldl": ldl,
        "hdl": hdl,
        "triglycerides": triglycerides,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "hscrp": hscrp,
    }

    entered = {k: v for k, v in all_labs.items() if v > 0}
    if entered:
        st.markdown("---")
        st.subheader("Quick Status")
        cols = st.columns(min(len(entered), 5))
        for i, (key, val) in enumerate(entered.items()):
            ref = REFERENCE_RANGES[key]
            status = classify_value(val, ref)
            color = get_status_color(status)
            with cols[i % len(cols)]:
                st.markdown(
                    f"<div style='padding:8px;border-left:4px solid {color};margin-bottom:8px'>"
                    f"<strong>{ref['label']}</strong><br>"
                    f"{val} {ref['unit']}<br>"
                    f"<span style='color:{color}'>{status.upper()}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if st.button("Save Lab Results", type="primary"):
        st.session_state.labs = all_labs
        st.success("Lab results saved. Proceed to Wearable Data.")
