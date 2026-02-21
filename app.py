"""
Founder Health MVP
==================
Help 40-60 year-old founders optimize metabolic and cardiovascular health
using labs + one wearable + an AI explainer.

Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Founder Health MVP",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state defaults
for key, default in {
    "profile": {},
    "labs": {},
    "wearables": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Sidebar navigation ---
st.sidebar.title("Founder Health MVP")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["1 - Profile", "2 - Lab Results", "3 - Wearable Data", "4 - AI Insights"],
)

# Show completion status in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Status**")
has_profile = bool(st.session_state.profile.get("age"))
has_labs = any(v for v in st.session_state.labs.values() if v)
has_wearables = any(v for v in st.session_state.wearables.values() if v)
st.sidebar.markdown(f"Profile: {'Done' if has_profile else 'Pending'}")
st.sidebar.markdown(f"Labs: {'Done' if has_labs else 'Pending'}")
st.sidebar.markdown(f"Wearable: {'Done' if has_wearables else 'Pending'}")

# --- Page routing ---
if page == "1 - Profile":
    from pages import profile
    profile.render()
elif page == "2 - Lab Results":
    from pages import lab_results
    lab_results.render()
elif page == "3 - Wearable Data":
    from pages import wearable_data
    wearable_data.render()
elif page == "4 - AI Insights":
    from pages import insights
    insights.render()
