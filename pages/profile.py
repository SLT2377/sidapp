"""Profile page - founder demographics and health goals."""

import streamlit as st


def render():
    st.header("Your Health Profile")
    st.markdown(
        "Tell us about yourself so the AI can personalize its analysis "
        "for a 40-60 year-old founder's health context."
    )

    profile = st.session_state.profile

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=30,
            max_value=80,
            value=profile.get("age", 50),
            step=1,
        )
        sex = st.selectbox(
            "Biological Sex",
            ["Male", "Female"],
            index=0 if profile.get("sex", "Male") == "Male" else 1,
        )
        height_cm = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=float(profile.get("height_cm", 175)),
            step=0.5,
        )
        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=250.0,
            value=float(profile.get("weight_kg", 80)),
            step=0.5,
        )

    with col2:
        goal = st.selectbox(
            "Primary Health Goal",
            [
                "Optimize metabolic health",
                "Reduce cardiovascular risk",
                "Improve energy & recovery",
                "Longevity / healthspan",
                "Weight management",
            ],
            index=0,
        )
        conditions = st.text_area(
            "Known Conditions or Medications (optional)",
            value=profile.get("conditions", ""),
            placeholder="e.g., family history of heart disease, on statins, hypothyroid...",
        )
        family_history = st.multiselect(
            "Family History (select all that apply)",
            [
                "Heart disease",
                "Type 2 diabetes",
                "Stroke",
                "High blood pressure",
                "High cholesterol",
                "None / Unknown",
            ],
            default=profile.get("family_history", []),
        )

    # BMI display
    if height_cm and weight_kg:
        h_m = height_cm / 100
        bmi = weight_kg / (h_m ** 2) if h_m > 0 else 0
        bmi_category = (
            "Underweight" if bmi < 18.5
            else "Normal" if bmi < 25
            else "Overweight" if bmi < 30
            else "Obese"
        )
        st.metric("Calculated BMI", f"{bmi:.1f}", delta=bmi_category, delta_color="off")

    if st.button("Save Profile", type="primary"):
        st.session_state.profile = {
            "age": age,
            "sex": sex,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "goal": goal,
            "conditions": conditions,
            "family_history": family_history,
        }
        st.success("Profile saved. Proceed to Lab Results.")
