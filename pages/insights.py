"""AI Health Insights page - Claude-powered health analysis."""

import streamlit as st
import plotly.graph_objects as go
from health_utils import (
    REFERENCE_RANGES,
    WEARABLE_RANGES,
    classify_value,
    get_status_color,
    build_health_summary,
)

SYSTEM_PROMPT = """\
You are a health-literate AI assistant for founders aged 40-60 who want to \
optimize metabolic and cardiovascular health. You are NOT a doctor and must \
always remind users to consult their physician before making changes.

Your job:
1. Interpret the lab results and wearable data provided in plain English.
2. Highlight what looks good, what needs attention, and what is urgent.
3. Explain WHY each flagged marker matters for a busy founder's healthspan.
4. Suggest 3-5 specific, evidence-based lifestyle actions ranked by impact.
5. Note which markers should be re-tested and when.

Guidelines:
- Be direct and concise. Founders are time-pressed.
- Use simple language; avoid unexplained medical jargon.
- When data is missing, say so and recommend getting that test.
- Frame everything around longevity and sustained performance.
- Always end with a clear disclaimer that this is educational, not medical advice.\
"""


def _get_claude_analysis(health_summary: str) -> str:
    """Call Claude API with the health summary and return the analysis."""
    import anthropic

    client = anthropic.Anthropic()

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Here is my complete health data. Please analyze it and "
                    "give me a clear, actionable health briefing.\n\n"
                    f"{health_summary}"
                ),
            }
        ],
    ) as stream:
        full_response = []
        for text in stream.text_stream:
            full_response.append(text)
        return "".join(full_response)


def _render_risk_gauge(label, value, ref):
    """Render a simple gauge chart for a metric."""
    status = classify_value(value, ref)
    color = get_status_color(status)

    low_opt, high_opt = ref["optimal"]
    _, high_bord = ref["borderline"]
    max_val = high_bord * 1.5

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": label, "font": {"size": 14}},
        number={"suffix": f" {ref['unit']}", "font": {"size": 16}},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0, low_opt], "color": "#fadbd8"},
                {"range": [low_opt, high_opt], "color": "#d5f5e3"},
                {"range": [high_opt, high_bord], "color": "#fdebd0"},
                {"range": [high_bord, max_val], "color": "#fadbd8"},
            ],
        },
    ))
    fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def render():
    st.header("AI Health Insights")

    profile = st.session_state.profile
    labs = st.session_state.labs
    wearables = st.session_state.wearables

    # Check data completeness
    has_profile = bool(profile.get("age"))
    has_labs = any(v for v in labs.values() if v)
    has_wearables = any(v for v in wearables.values() if v)

    if not has_profile:
        st.warning("Please complete your Profile first (step 1).")
        return

    if not has_labs and not has_wearables:
        st.warning("Please enter Lab Results or Wearable Data before requesting insights.")
        return

    # --- Visual Dashboard ---
    st.subheader("Your Health Dashboard")

    # Lab gauges
    entered_labs = {k: v for k, v in labs.items() if v and v > 0}
    if entered_labs:
        st.markdown("**Lab Results**")
        cols = st.columns(min(len(entered_labs), 5))
        for i, (key, val) in enumerate(entered_labs.items()):
            ref = REFERENCE_RANGES[key]
            with cols[i % len(cols)]:
                fig = _render_risk_gauge(ref["label"], val, ref)
                st.plotly_chart(fig, use_container_width=True)

    # Wearable gauges
    entered_wearables = {k: v for k, v in wearables.items() if v and v > 0}
    if entered_wearables:
        st.markdown("**Wearable Metrics**")
        cols = st.columns(len(entered_wearables))
        for i, (key, val) in enumerate(entered_wearables.items()):
            ref = WEARABLE_RANGES[key]
            with cols[i]:
                fig = _render_risk_gauge(ref["label"], val, ref)
                st.plotly_chart(fig, use_container_width=True)

    # --- AI Analysis ---
    st.markdown("---")
    st.subheader("AI-Powered Analysis")

    st.info(
        "This will send your health data to Claude (Anthropic) for analysis. "
        "Ensure you have set the ANTHROPIC_API_KEY environment variable."
    )

    if st.button("Generate Health Briefing", type="primary"):
        health_summary = build_health_summary(profile, labs, wearables)

        with st.expander("Raw data sent to AI (click to inspect)"):
            st.code(health_summary, language="text")

        with st.spinner("Claude is analyzing your health data..."):
            try:
                analysis = _get_claude_analysis(health_summary)
                st.markdown("### Your Personalized Health Briefing")
                st.markdown(analysis)
            except Exception as e:
                error_msg = str(e)
                if "ANTHROPIC_API_KEY" in error_msg or "api_key" in error_msg.lower():
                    st.error(
                        "API key not configured. Set the ANTHROPIC_API_KEY "
                        "environment variable and restart the app."
                    )
                else:
                    st.error(f"Error contacting AI service: {error_msg}")
