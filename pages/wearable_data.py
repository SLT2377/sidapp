"""Wearable Data page - manual entry of key wearable metrics."""

import streamlit as st
from health_utils import WEARABLE_RANGES, classify_value, get_status_color


def render():
    st.header("Wearable Data")
    st.markdown(
        "Enter your recent averages from your wearable (Apple Watch, Oura, "
        "Whoop, Garmin, etc.). Use 7-day or 30-day averages for best results."
    )

    wearables = st.session_state.wearables

    col1, col2 = st.columns(2)

    with col1:
        resting_hr = st.number_input(
            "Resting Heart Rate (bpm)",
            min_value=0,
            max_value=200,
            value=int(wearables.get("resting_hr", 0)),
            step=1,
            help="7-day average. Optimal for age 40-60: 50-65 bpm.",
        )
        hrv = st.number_input(
            "Heart Rate Variability - RMSSD (ms)",
            min_value=0,
            max_value=300,
            value=int(wearables.get("hrv", 0)),
            step=1,
            help="7-day average. Higher is generally better. Optimal: >30 ms.",
        )

    with col2:
        sleep_hours = st.number_input(
            "Average Sleep Duration (hours)",
            min_value=0.0,
            max_value=14.0,
            value=float(wearables.get("sleep_hours", 0)),
            step=0.25,
            help="7-day average. Optimal: 7-9 hours.",
        )
        daily_steps = st.number_input(
            "Average Daily Steps",
            min_value=0,
            max_value=50000,
            value=int(wearables.get("daily_steps", 0)),
            step=500,
            help="7-day average. Optimal: 8,000+.",
        )

    all_wearables = {
        "resting_hr": resting_hr,
        "hrv": hrv,
        "sleep_hours": sleep_hours,
        "daily_steps": daily_steps,
    }

    # Summary
    entered = {k: v for k, v in all_wearables.items() if v > 0}
    if entered:
        st.markdown("---")
        st.subheader("Quick Status")
        cols = st.columns(len(entered))
        for i, (key, val) in enumerate(entered.items()):
            ref = WEARABLE_RANGES[key]
            status = classify_value(val, ref)
            color = get_status_color(status)
            with cols[i]:
                st.markdown(
                    f"<div style='padding:8px;border-left:4px solid {color};margin-bottom:8px'>"
                    f"<strong>{ref['label']}</strong><br>"
                    f"{val} {ref['unit']}<br>"
                    f"<span style='color:{color}'>{status.upper()}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    if st.button("Save Wearable Data", type="primary"):
        st.session_state.wearables = all_wearables
        st.success("Wearable data saved. Proceed to AI Insights.")
