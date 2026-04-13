"""
Personalisierungs-Decision-Support-Tool (MVP)
=============================================
Streamlit-App: kombiniert Campaign-Fatigue-Analyse (empirisch) mit
Max' Risk-Score-Framework zu einem interaktiven Go/No-Go-Tool.

Start: streamlit run Cringe-Tipping/app.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from decision_engine import (
    AutomationDegree,
    Channel,
    ImpactType,
    PersonalizationDecisionEngine,
    PersonalizationLevel,
    PersonalizationRequest,
    Signal,
    UseCase,
)
from campaign_fatigue import CampaignFatigueAnalyzer

# ── Page Config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Personalisierungs-Decision-Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/raw/bank_marketing/bank-additional-full.csv")

# ── Sidebar: Eingabeformular ──────────────────────────────────────────────────

with st.sidebar:
    st.title("🎯 Use-Case-Konfiguration")
    st.caption("Alle Felder ausfüllen — Tool berechnet automatisch.")

    st.subheader("Use Case")
    use_case = UseCase(st.selectbox("Use Case", [e.value for e in UseCase]))
    channel  = Channel(st.selectbox("Kanal", [e.value for e in Channel]))
    kpi      = st.text_input("Primär-KPI", value="Conversion Rate")

    st.subheader("Personalisierungsgrad")
    pers_level = PersonalizationLevel(
        st.select_slider(
            "Gewünschter Grad",
            options=[e.value for e in PersonalizationLevel],
            value=PersonalizationLevel.SEGMENT.value,
        )
    )
    automation = AutomationDegree(
        st.selectbox("Automatisierungsgrad", [e.value for e in AutomationDegree])
    )
    impact = ImpactType(
        st.selectbox("Impact-Typ", [e.value for e in ImpactType])
    )

    st.subheader("Datenbasis")
    behavioral = st.checkbox("Verhaltensdaten (Clickstream, GA4)", value=True)
    crm        = st.checkbox("CRM / Transaktionshistorie", value=False)
    geo        = st.checkbox("Geo / Device-Daten", value=False)
    special    = st.checkbox("⚠️ Besondere Kategorien (Art. 9)", value=False)

    st.subheader("Risiko-Toleranz")
    risk_tol = st.slider(
        "Risiko-Toleranz", min_value=0.0, max_value=1.0, value=0.5, step=0.05,
        help="0 = sehr konservativ, 1 = risikofreudig"
    )

    evaluate_btn = st.button("▶ Entscheid berechnen", use_container_width=True, type="primary")

# ── Engine ausführen ──────────────────────────────────────────────────────────

req = PersonalizationRequest(
    use_case=use_case,
    channel=channel,
    automation_degree=automation,
    impact_type=impact,
    personalization_level=pers_level,
    uses_behavioral_data=behavioral,
    uses_crm_data=crm,
    uses_geo_device=geo,
    uses_special_categories=special,
    kpi=kpi,
    risk_tolerance=risk_tol,
)

engine = PersonalizationDecisionEngine()
result = engine.evaluate(req)

# ── Header ────────────────────────────────────────────────────────────────────

st.title("Personalisierungs-Decision-Support-Tool")
st.caption(f"Use Case: **{use_case.value}** | Kanal: **{channel.value}** | Level: **{pers_level.value}**")

# ── Ampel-Banner ──────────────────────────────────────────────────────────────

signal_config = {
    Signal.GREEN:  {"color": "#1B5E20", "bg": "#E8F5E9", "border": "#4CAF50", "emoji": "🟢", "label": "GO"},
    Signal.YELLOW: {"color": "#E65100", "bg": "#FFF8E1", "border": "#FF9800", "emoji": "🟡", "label": "GO MIT GUARDRAILS"},
    Signal.RED:    {"color": "#B71C1C", "bg": "#FFEBEE", "border": "#F44336", "emoji": "🔴", "label": "NO-GO"},
}
cfg = signal_config[result.signal]

st.markdown(
    f"""
    <div style="
        background:{cfg['bg']};
        border-left: 6px solid {cfg['border']};
        border-radius: 8px;
        padding: 16px 24px;
        margin-bottom: 24px;
    ">
        <span style="font-size:2rem;">{cfg['emoji']}</span>
        <span style="font-size:1.6rem; font-weight:700; color:{cfg['color']}; margin-left:12px;">
            {cfg['label']}
        </span>
        <span style="color:#555; margin-left:16px; font-size:0.95rem;">
            Empfohlener Level: <strong>{result.recommended_level.value}</strong>
            {'&nbsp;&nbsp;|&nbsp;&nbsp;⚠️ Art. 22 DSGVO ausgelöst' if result.article22_triggered else ''}
            {'&nbsp;&nbsp;|&nbsp;&nbsp;📋 DPIA erforderlich' if result.dpia_required else ''}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPI-Metriken ──────────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)
c1.metric("Performance-Lift", f"+{result.performance_lift:.0%}", help="Relativer Lift vs. Generic (keine Personalisierung)")
c2.metric("Risk Score", f"{result.risk_score:.2f} / 1.0", delta=f"{'⚠ Hoch' if result.risk_score >= 0.7 else '✓ OK'}", delta_color="inverse")
c3.metric("Netto-Business-Value", f"{result.net_business_value:+.3f}", help="NBV = gewichteter Lift − Risiko")
c4.metric("Rechtsbasis", result.legal_basis.split("—")[0].strip())

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["📊 NBV-Kurve", "🛡 Guardrails & Risiken", "🧪 Experiment-Plan", "📄 1-Pager Export"])

# ── Tab 1: NBV-Kurve ──────────────────────────────────────────────────────────

with tab1:
    st.subheader("Netto-Business-Value über Personalisierungsgrade")
    st.caption(
        "Zeigt Performance-Lift, Risk Score und NBV für alle vier Personalisierungsgrade. "
        "Der NBV-Peak markiert den optimalen Punkt — rechts davon überwiegen die Risiken."
    )

    profiles = result.level_profiles
    levels   = [p.level.value for p in profiles]
    lifts    = [p.performance_lift for p in profiles]
    risks    = [p.risk_score for p in profiles]
    nbvs     = [p.net_value for p in profiles]

    # Welcher Balken ist der aktuell gewählte?
    chosen_idx = next(i for i, p in enumerate(profiles) if p.level == pers_level)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("Performance-Lift & Risk Score", "Netto-Business-Value (NBV)"),
        vertical_spacing=0.12,
        row_heights=[0.55, 0.45],
    )

    # Lift-Bars
    fig.add_trace(go.Bar(
        x=levels, y=lifts,
        name="Performance-Lift",
        marker_color=["#42A5F5" if i != chosen_idx else "#1565C0" for i in range(len(levels))],
        opacity=0.85,
        text=[f"+{l:.0%}" for l in lifts],
        textposition="outside",
    ), row=1, col=1)

    # Risk-Linie
    fig.add_trace(go.Scatter(
        x=levels, y=risks,
        name="Risk Score",
        mode="lines+markers",
        line=dict(color="#EF5350", width=3),
        marker=dict(size=10, symbol="diamond"),
        yaxis="y2",
    ), row=1, col=1)

    # Risk-Schwellen
    for threshold, label, color in [
        (0.60, "Einwilligung empfohlen", "rgba(255,152,0,0.15)"),
        (0.75, "DPIA-Schwelle", "rgba(244,67,54,0.12)"),
    ]:
        fig.add_hline(y=threshold, line_dash="dot", line_color=color.replace("0.15", "1").replace("0.12", "1"),
                      annotation_text=label, annotation_position="right",
                      row=1, col=1)

    # NBV-Bars
    nbv_colors = []
    for i, p in enumerate(profiles):
        sig = result.signal if i == chosen_idx else None
        if p.net_value < 0:
            nbv_colors.append("#EF5350")
        elif p.level == result.recommended_level:
            nbv_colors.append("#2E7D32")
        elif i == chosen_idx:
            nbv_colors.append("#1565C0")
        else:
            nbv_colors.append("#78909C")

    fig.add_trace(go.Bar(
        x=levels, y=nbvs,
        name="NBV",
        marker_color=nbv_colors,
        opacity=0.9,
        text=[f"{n:+.3f}" for n in nbvs],
        textposition="outside",
    ), row=2, col=1)

    fig.add_hline(y=0, line_color="black", line_width=1.2, row=2, col=1)

    # Aktuellen Level markieren
    fig.add_vline(
        x=chosen_idx, line_dash="dash", line_color="#1565C0", opacity=0.5,
        annotation_text=f" Gewählt: {pers_level.value}", annotation_position="top right",
    )
    # Empfohlenen Level markieren
    rec_idx = next(i for i, p in enumerate(profiles) if p.level == result.recommended_level)
    if rec_idx != chosen_idx:
        fig.add_vline(
            x=rec_idx, line_dash="dash", line_color="#2E7D32", opacity=0.5,
            annotation_text=f" Empfohlen: {result.recommended_level.value}", annotation_position="top left",
        )

    fig.update_layout(
        height=560,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis2=dict(overlaying="y", side="right", range=[0, 1.1], title="Risk Score"),
        margin=dict(t=60, b=20),
    )
    fig.update_yaxes(title_text="Performance-Lift (relativ)", row=1, col=1)
    fig.update_yaxes(title_text="NBV", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

    # Campaign Fatigue Kurve (empirisch)
    st.subheader("Empirischer Tipping Point: Campaign Fatigue (Bank-Marketing-Daten)")
    st.caption(
        "Die quadratische Regression zeigt den empirisch gemessenen Punkt, "
        "ab dem zusätzliche Kontakte (= höherer Personalisierungsdruck) die Response Rate senken."
    )

    try:
        analyzer = CampaignFatigueAnalyzer(max_campaigns=10)
        fatigue_result = analyzer.run(DATA_PATH)
        stats = fatigue_result.campaign_stats

        x_vals   = stats["campaign_contacts"].values
        y_vals   = stats["response_rate"].values
        ci_low   = stats["ci_low"].values
        ci_high  = stats["ci_high"].values
        n_obs    = stats["n_observations"].values

        x_smooth = np.linspace(x_vals.min(), x_vals.max(), 300)
        b0, b1, b2 = fatigue_result.beta_0, fatigue_result.beta_1, fatigue_result.beta_2
        y_quad = b0 + b1 * x_smooth + b2 * x_smooth**2

        tp = fatigue_result.tipping_point

        fig2 = go.Figure()

        # KI-Band
        fig2.add_trace(go.Scatter(
            x=np.concatenate([x_vals, x_vals[::-1]]),
            y=np.concatenate([ci_high, ci_low[::-1]]),
            fill="toself", fillcolor="rgba(66,165,245,0.15)",
            line=dict(color="rgba(255,255,255,0)"),
            name="95%-KI",
        ))

        # Datenpunkte
        fig2.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode="markers",
            marker=dict(size=[max(8, n / n_obs.max() * 22) for n in n_obs], color="#1565C0", opacity=0.8),
            name="Response Rate (beobachtet)",
            text=[f"n={n:,}" for n in n_obs],
            hovertemplate="%{text}<br>Rate: %{y:.1%}<extra></extra>",
        ))

        # Quadrat. Kurve
        fig2.add_trace(go.Scatter(
            x=x_smooth, y=y_quad,
            mode="lines", line=dict(color="#E53935", width=3),
            name=f"Quadrat. Fit (R²={fatigue_result.r2_quadratic:.3f})",
        ))

        # Tipping Point
        if 0 < tp <= x_vals.max() + 2:
            tp_y = b0 + b1 * tp + b2 * tp**2
            fig2.add_vline(x=tp, line_dash="dot", line_color="darkorange", line_width=2)
            fig2.add_annotation(
                x=tp, y=tp_y, text=f"Tipping Point<br>x* = {tp:.1f} Kontakte",
                showarrow=True, arrowhead=2, arrowcolor="darkorange",
                font=dict(color="darkorange", size=12),
                ax=40, ay=-40,
            )

        fig2.update_layout(
            height=400,
            xaxis_title="Anzahl Kontakte (campaign)",
            yaxis_title="Response Rate",
            yaxis_tickformat=".0%",
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=40, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Tipping Point", f"{tp:.1f} Kontakte")
        col_b.metric("R² (quadratisch)", f"{fatigue_result.r2_quadratic:.4f}")
        col_c.metric("F-Test p-Wert", f"{fatigue_result.f_p_value:.5f}",
                     delta="signifikant" if fatigue_result.f_p_value < 0.05 else "nicht signifikant",
                     delta_color="normal" if fatigue_result.f_p_value < 0.05 else "inverse")

    except FileNotFoundError:
        st.warning(
            "Bank-Marketing-Datei nicht gefunden. "
            "Bitte `data/raw/bank_marketing/bank-additional-full.csv` ablegen."
        )

# ── Tab 2: Guardrails & Risiken ───────────────────────────────────────────────

with tab2:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Top-Risiko-Treiber")
        if result.top_risk_drivers:
            for driver in result.top_risk_drivers:
                st.error(f"⚠ {driver}")
        else:
            st.success("Keine kritischen Risiko-Treiber identifiziert.")

        st.subheader("Rechtsbasis")
        st.info(f"**{result.legal_basis}**")

        if result.article22_triggered:
            st.error(
                "**Art. 22 DSGVO ausgelöst:** Diese Konfiguration trifft automatisierte "
                "Einzelentscheidungen mit erheblichem Impact. Explizite Einwilligung und "
                "Human-Review-Gate sind Pflicht."
            )
        if result.dpia_required:
            st.warning(
                "**DPIA erforderlich:** Datenschutz-Folgenabschätzung vor Go-Live durchführen. "
                "(Art. 35 DSGVO — hohe Risiken für betroffene Personen)"
            )

    with col_right:
        st.subheader("Guardrails (Pflicht-To-dos)")
        for i, g in enumerate(result.guardrails, 1):
            is_mandatory = g.startswith("PFLICHT")
            if is_mandatory:
                st.error(f"{i}. {g}")
            else:
                st.warning(f"{i}. {g}")

# ── Tab 3: Experiment-Plan ────────────────────────────────────────────────────

with tab3:
    st.subheader("Experiment-Design")
    ep = result.experiment_plan

    c1, c2, c3 = st.columns(3)
    c1.metric("Design", ep.get("design", ""))
    c2.metric("Holdout-Gruppe", f"{ep.get('holdout_pct', '')}%")
    c3.metric("Mindest-Laufzeit", f"{ep.get('min_runtime_days', '')} Tage")

    st.markdown(f"**Primär-KPI:** {ep.get('primary_kpi', '')}")
    st.markdown(f"**Signifikanzniveau:** α = {ep.get('significance_level', 0.05)}")

    st.subheader("Guardrail-KPIs (Monitoring)")
    for kpi_item in ep.get("guardrail_kpis", []):
        st.markdown(f"- {kpi_item}")

    st.info(ep.get("note", ""))

# ── Tab 4: 1-Pager Export ─────────────────────────────────────────────────────

with tab4:
    st.subheader("1-Pager für Legal / Stakeholder")
    st.caption("Markdown-Dokument — direkt kopieren oder als .md herunterladen.")

    st.download_button(
        label="⬇ 1-Pager als .md herunterladen",
        data=result.one_pager_md,
        file_name=f"personalisierung_entscheid_{use_case.value.lower().replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown(result.one_pager_md)
