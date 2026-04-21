import math
from dataclasses import dataclass

import pandas as pd
import streamlit as st


# -----------------------------
# Konfiguration
# -----------------------------
st.set_page_config(
    page_title="Risk-Score-Simulator",
    page_icon="⚠️",
    layout="wide",
)

CRITICAL_THRESHOLD = 0.7


# -----------------------------
# Hilfsfunktionen
# -----------------------------
def calculate_volume(feature_count: int) -> float:
    """
    Mappt die Anzahl der Features auf den Volume-Score.
    Formel aus dem Projekt:
    Volume = min(0.1 + 0.03 * Featureanzahl, 0.9)
    """
    if feature_count < 0:
        raise ValueError("feature_count darf nicht negativ sein.")
    return min(0.1 + 0.03 * feature_count, 0.9)


def granularity_score(level: str) -> float:
    """
    Mappt die Granularity-Stufe auf den Score.
    """
    mapping = {
        "Generisch": 0.2,
        "Segmentbasiert": 0.6,
        "Individuell": 0.9,
    }
    if level not in mapping:
        raise ValueError(f"Unbekannte Granularity-Stufe: {level}")
    return mapping[level]


def adjusted_sensitivity(base_sensitivity: float, sensitive_feature_share: int) -> float:
    """
    Optionale leichte Anpassung der Sensitivity anhand des Anteils sensibler Features.
    sensitive_feature_share: 0 bis 100
    Logik:
    - Basiswert kommt vom Slider
    - je höher der Anteil sensibler Features, desto etwas höher der Endwert
    """
    if not 0 <= base_sensitivity <= 1:
        raise ValueError("base_sensitivity muss zwischen 0 und 1 liegen.")
    if not 0 <= sensitive_feature_share <= 100:
        raise ValueError("sensitive_feature_share muss zwischen 0 und 100 liegen.")

    uplift = 0.2 * (sensitive_feature_share / 100.0)
    return min(base_sensitivity + uplift, 1.0)


def calculate_risk(volume: float, sensitivity: float, granularity: float) -> float:
    """
    Berechnet den finalen Risk Score.
    """
    for value, name in [
        (volume, "volume"),
        (sensitivity, "sensitivity"),
        (granularity, "granularity"),
    ]:
        if not 0 <= value <= 1:
            raise ValueError(f"{name} muss zwischen 0 und 1 liegen.")

    return 0.3 * volume + 0.3 * sensitivity + 0.4 * granularity


def risk_label(score: float) -> str:
    """
    Ordnet den Score einem Risikobereich zu.
    """
    if score < 0.3:
        return "Niedrig"
    if score < 0.7:
        return "Mittel"
    return "Hoch"


def risk_color(score: float) -> str:
    """
    Gibt eine Farbe für den Score zurück.
    """
    if score < 0.3:
        return "green"
    if score < 0.7:
        return "orange"
    return "red"


def features_remaining_until_threshold(
    current_features: int,
    base_sensitivity: float,
    sensitive_feature_share: int,
    granularity_level: str,
    threshold: float = CRITICAL_THRESHOLD,
) -> int:
    """
    Berechnet, wie viele zusätzliche Features noch möglich sind,
    bis die kritische Schwelle erreicht oder überschritten wird.

    Annahme:
    - Sensitivity und Granularity bleiben konstant.
    - Nur Volume steigt durch zusätzliche Features.
    """
    current = current_features
    for extra in range(0, 200):
        feature_count = current + extra
        volume = calculate_volume(feature_count)
        sensitivity = adjusted_sensitivity(base_sensitivity, sensitive_feature_share)
        granularity = granularity_score(granularity_level)
        risk = calculate_risk(volume, sensitivity, granularity)

        if risk >= threshold:
            return max(extra - 1, 0)

    return 200


@dataclass
class Scenario:
    feature_count: int
    base_sensitivity: float
    sensitive_share: int
    granularity_level: str

    @property
    def volume(self) -> float:
        return calculate_volume(self.feature_count)

    @property
    def sensitivity(self) -> float:
        return adjusted_sensitivity(self.base_sensitivity, self.sensitive_share)

    @property
    def granularity(self) -> float:
        return granularity_score(self.granularity_level)

    @property
    def risk(self) -> float:
        return calculate_risk(self.volume, self.sensitivity, self.granularity)


# -----------------------------
# Titel
# -----------------------------
st.title("Interaktiver Risk-Score-Simulator")
st.caption(
    "Konzeptionelles Governance-Tool zur Veranschaulichung der Datenschutzschwelle "
    "bei KI-gestützter Personalisierung."
)

st.markdown(
    """
Dieser Simulator zeigt, wie sich **Featureanzahl**, **Sensitivität** und
**Granularität** auf den Risk Score auswirken. Die kritische Schwelle liegt bei **0,7**.
"""
)

# -----------------------------
# Eingaben
# -----------------------------
left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("Einstellungen")

    feature_count = st.slider(
        "Anzahl der verwendeten Features",
        min_value=1,
        max_value=30,
        value=10,
        step=1,
        help="Beeinflusst den Volume-Score.",
    )

    base_sensitivity = st.slider(
        "Basis-Sensitivität der Daten",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Grundbewertung der Datensensitivität vor zusätzlicher Anpassung.",
    )

    sensitive_feature_share = st.slider(
        "Anteil sensibler Features (%)",
        min_value=0,
        max_value=100,
        value=20,
        step=5,
        help="Erhöht die Sensitivity leicht, wenn viele sensible Merkmale genutzt werden.",
    )

    granularity_level = st.selectbox(
        "Granularität / Personalisierungsstufe",
        options=["Generisch", "Segmentbasiert", "Individuell"],
        index=1,
        help="Bestimmt, wie individuell die Ansprache bzw. Entscheidung ist.",
    )

    scenario = Scenario(
        feature_count=feature_count,
        base_sensitivity=base_sensitivity,
        sensitive_share=sensitive_feature_share,
        granularity_level=granularity_level,
    )

with right:
    st.subheader("Berechnete Teilwerte")

    st.metric("Volume", f"{scenario.volume:.2f}")
    st.metric("Sensitivity", f"{scenario.sensitivity:.2f}")
    st.metric("Granularity", f"{scenario.granularity:.2f}")

    st.markdown("---")

    score = scenario.risk
    label = risk_label(score)
    color = risk_color(score)

    st.markdown(
        f"""
        <div style="
            padding: 1rem;
            border-radius: 12px;
            background-color: #f8f9fa;
            border-left: 8px solid {color};
        ">
            <h3 style="margin: 0; color: black;">Aktueller Risk Score: {score:.2f}</h3>
            <p style="margin: 0.5rem 0 0 0; color: black;">Risikobereich: <b>{label}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Schwellenlogik
# -----------------------------
st.subheader("Kritische Schwelle")

distance = CRITICAL_THRESHOLD - score
remaining_features = features_remaining_until_threshold(
    current_features=feature_count,
    base_sensitivity=base_sensitivity,
    sensitive_feature_share=sensitive_feature_share,
    granularity_level=granularity_level,
)

col1, col2, col3 = st.columns(3)

with col1:
    if distance > 0:
        st.metric("Abstand zur Schwelle 0,7", f"{distance:.2f}")
    else:
        st.metric("Überschreitung der Schwelle", f"{abs(distance):.2f}")

with col2:
    st.metric("Weitere Features bis 0,7", remaining_features)

with col3:
    if score >= CRITICAL_THRESHOLD:
        st.error("Kritische Schwelle erreicht oder überschritten.")
    else:
        st.success("Unterhalb der kritischen Schwelle.")

# -----------------------------
# Visualisierung
# -----------------------------
st.subheader("Visualisierung")

chart_df = pd.DataFrame(
    {
        "Komponente": ["Volume", "Sensitivity", "Granularity", "Risk Score", "Schwelle"],
        "Wert": [
            scenario.volume,
            scenario.sensitivity,
            scenario.granularity,
            scenario.risk,
            CRITICAL_THRESHOLD,
        ],
    }
)

st.bar_chart(chart_df.set_index("Komponente"))

# -----------------------------
# Vergleichsszenario
# -----------------------------
st.subheader("Was passiert bei einer anderen Konfiguration?")

compare_col1, compare_col2 = st.columns(2)

with compare_col1:
    st.markdown("**Aktuelles Szenario**")
    st.write(
        {
            "Features": scenario.feature_count,
            "Volume": round(scenario.volume, 2),
            "Sensitivity": round(scenario.sensitivity, 2),
            "Granularity": round(scenario.granularity, 2),
            "Risk Score": round(scenario.risk, 2),
        }
    )

with compare_col2:
    st.markdown("**Alternativszenario**")
    alt_feature_count = st.slider(
        "Alternative Anzahl Features",
        min_value=1,
        max_value=30,
        value=min(feature_count + 3, 30),
        step=1,
        key="alt_feature_count",
    )
    alt_base_sensitivity = st.slider(
        "Alternative Basis-Sensitivität",
        min_value=0.0,
        max_value=1.0,
        value=base_sensitivity,
        step=0.05,
        key="alt_base_sensitivity",
    )
    alt_sensitive_share = st.slider(
        "Alternative sensible Features (%)",
        min_value=0,
        max_value=100,
        value=sensitive_feature_share,
        step=5,
        key="alt_sensitive_share",
    )
    alt_granularity = st.selectbox(
        "Alternative Granularität",
        options=["Generisch", "Segmentbasiert", "Individuell"],
        index=["Generisch", "Segmentbasiert", "Individuell"].index(granularity_level),
        key="alt_granularity",
    )

    alt_scenario = Scenario(
        feature_count=alt_feature_count,
        base_sensitivity=alt_base_sensitivity,
        sensitive_share=alt_sensitive_share,
        granularity_level=alt_granularity,
    )

    st.write(
        {
            "Features": alt_scenario.feature_count,
            "Volume": round(alt_scenario.volume, 2),
            "Sensitivity": round(alt_scenario.sensitivity, 2),
            "Granularity": round(alt_scenario.granularity, 2),
            "Risk Score": round(alt_scenario.risk, 2),
        }
    )

compare_df = pd.DataFrame(
    {
        "Szenario": ["Aktuell", "Alternative"],
        "Risk Score": [scenario.risk, alt_scenario.risk],
    }
)

st.bar_chart(compare_df.set_index("Szenario"))

# -----------------------------
# Methodische Einordnung
# -----------------------------
with st.expander("Methodische Einordnung"):
    st.markdown(
        """
Dieser Simulator ist **kein wissenschaftlich validiertes Entscheidungssystem**,
sondern ein **konzeptionelles Governance-Tool** auf Basis des im Projekt entwickelten Risk Scores.

Verwendete Logik:
- **Volume** wird aus der Anzahl der Features abgeleitet.
- **Sensitivity** wird über einen Basiswert und den Anteil sensibler Features modelliert.
- **Granularity** wird über drei Personalisierungsstufen abgebildet.
- Die kritische Schwelle liegt bei **0,7**.
"""
    )