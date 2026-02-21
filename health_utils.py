"""
Shared utilities for the Founder Health MVP.
Reference ranges, risk scoring, and session state helpers.
"""

# Clinical reference ranges for lab markers
# Sources: AHA, ADA, NCEP ATP III guidelines
REFERENCE_RANGES = {
    # Metabolic panel
    "fasting_glucose": {
        "label": "Fasting Glucose",
        "unit": "mg/dL",
        "optimal": (70, 99),
        "borderline": (100, 125),
        "high_label": "Pre-diabetic / Diabetic",
        "low_label": "Hypoglycemia",
    },
    "hba1c": {
        "label": "HbA1c",
        "unit": "%",
        "optimal": (4.0, 5.6),
        "borderline": (5.7, 6.4),
        "high_label": "Pre-diabetic / Diabetic",
        "low_label": "Normal",
    },
    "fasting_insulin": {
        "label": "Fasting Insulin",
        "unit": "µIU/mL",
        "optimal": (2.0, 8.0),
        "borderline": (8.1, 19.9),
        "high_label": "Insulin Resistance",
        "low_label": "Normal",
    },
    # Lipid panel
    "total_cholesterol": {
        "label": "Total Cholesterol",
        "unit": "mg/dL",
        "optimal": (125, 199),
        "borderline": (200, 239),
        "high_label": "High",
        "low_label": "Low",
    },
    "ldl": {
        "label": "LDL Cholesterol",
        "unit": "mg/dL",
        "optimal": (0, 99),
        "borderline": (100, 159),
        "high_label": "High",
        "low_label": "Normal",
    },
    "hdl": {
        "label": "HDL Cholesterol",
        "unit": "mg/dL",
        "optimal": (60, 200),
        "borderline": (40, 59),
        "high_label": "Normal (higher is better)",
        "low_label": "Low (cardiovascular risk)",
    },
    "triglycerides": {
        "label": "Triglycerides",
        "unit": "mg/dL",
        "optimal": (0, 149),
        "borderline": (150, 199),
        "high_label": "High",
        "low_label": "Normal",
    },
    # Cardiovascular
    "systolic_bp": {
        "label": "Systolic Blood Pressure",
        "unit": "mmHg",
        "optimal": (90, 119),
        "borderline": (120, 139),
        "high_label": "Hypertension",
        "low_label": "Hypotension",
    },
    "diastolic_bp": {
        "label": "Diastolic Blood Pressure",
        "unit": "mmHg",
        "optimal": (60, 79),
        "borderline": (80, 89),
        "high_label": "Hypertension",
        "low_label": "Hypotension",
    },
    "hscrp": {
        "label": "hs-CRP (Inflammation)",
        "unit": "mg/L",
        "optimal": (0.0, 1.0),
        "borderline": (1.1, 3.0),
        "high_label": "Elevated (cardiovascular risk)",
        "low_label": "Normal",
    },
}

# Wearable metric reference ranges for 40-60 year olds
WEARABLE_RANGES = {
    "resting_hr": {
        "label": "Resting Heart Rate",
        "unit": "bpm",
        "optimal": (50, 65),
        "borderline": (66, 80),
        "high_label": "Elevated",
        "low_label": "Athletic / Low",
    },
    "hrv": {
        "label": "Heart Rate Variability (RMSSD)",
        "unit": "ms",
        "optimal": (30, 200),
        "borderline": (20, 29),
        "high_label": "Excellent",
        "low_label": "Low (stress / recovery concern)",
    },
    "sleep_hours": {
        "label": "Average Sleep Duration",
        "unit": "hours",
        "optimal": (7.0, 9.0),
        "borderline": (6.0, 6.9),
        "high_label": "Oversleeping",
        "low_label": "Sleep deprived",
    },
    "daily_steps": {
        "label": "Average Daily Steps",
        "unit": "steps",
        "optimal": (8000, 100000),
        "borderline": (5000, 7999),
        "high_label": "Active",
        "low_label": "Sedentary",
    },
}


def classify_value(value, ref):
    """Classify a lab/wearable value as optimal, borderline, or out-of-range."""
    if value is None or value == 0.0:
        return "missing"
    low_opt, high_opt = ref["optimal"]
    low_bord, high_bord = ref["borderline"]
    if low_opt <= value <= high_opt:
        return "optimal"
    if low_bord <= value <= high_bord:
        return "borderline"
    if value < low_opt:
        return "low"
    return "high"


def get_status_color(classification):
    """Return a color for the classification."""
    return {
        "optimal": "#2ecc71",
        "borderline": "#f39c12",
        "high": "#e74c3c",
        "low": "#e74c3c",
        "missing": "#95a5a6",
    }.get(classification, "#95a5a6")


def get_status_emoji(classification):
    """Return a status indicator for the classification."""
    return {
        "optimal": "OK",
        "borderline": "WATCH",
        "high": "FLAG",
        "low": "FLAG",
        "missing": "--",
    }.get(classification, "--")


def build_health_summary(profile, labs, wearables):
    """Build a structured text summary of all health data for the AI explainer."""
    lines = []

    lines.append("=== FOUNDER HEALTH PROFILE ===")
    lines.append(f"Age: {profile.get('age', 'Not provided')}")
    lines.append(f"Sex: {profile.get('sex', 'Not provided')}")
    lines.append(f"Height: {profile.get('height_cm', 'N/A')} cm")
    lines.append(f"Weight: {profile.get('weight_kg', 'N/A')} kg")
    if profile.get('height_cm') and profile.get('weight_kg'):
        h_m = profile['height_cm'] / 100
        bmi = profile['weight_kg'] / (h_m ** 2) if h_m > 0 else 0
        lines.append(f"BMI: {bmi:.1f}")
    lines.append(f"Primary goal: {profile.get('goal', 'Not specified')}")
    lines.append(f"Known conditions: {profile.get('conditions', 'None reported')}")
    lines.append("")

    lines.append("=== LAB RESULTS ===")
    for key, ref in REFERENCE_RANGES.items():
        val = labs.get(key)
        if val is not None and val != 0.0:
            status = classify_value(val, ref)
            lines.append(
                f"{ref['label']}: {val} {ref['unit']} [{status.upper()}]"
            )
    lines.append("")

    lines.append("=== WEARABLE DATA ===")
    for key, ref in WEARABLE_RANGES.items():
        val = wearables.get(key)
        if val is not None and val != 0.0:
            status = classify_value(val, ref)
            lines.append(
                f"{ref['label']}: {val} {ref['unit']} [{status.upper()}]"
            )

    return "\n".join(lines)
