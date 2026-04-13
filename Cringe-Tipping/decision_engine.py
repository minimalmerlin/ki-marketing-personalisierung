"""
Decision Engine — Personalisierungs-NBV-Kalkulator
====================================================
Berechnet den Netto-Business-Value (NBV) eines Personalisierungs-Use-Cases
unter Berücksichtigung von Performance-Lift und DSGVO-Compliance-Risiken.

Architektur:
    UseCase (Input DTO)
    → RiskScorer      → risk_score, risk_drivers, legal_basis
    → LiftEstimator   → performance_lift, lift_confidence
    → NBVCalculator   → net_business_value, optimal_level
    → DecisionEngine  → signal (GREEN/YELLOW/RED), guardrails, experiment_plan
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Enums ────────────────────────────────────────────────────────────────────

class Channel(str, Enum):
    EMAIL   = "E-Mail"
    ONSITE  = "Onsite"
    ADS     = "Paid Ads"
    PUSH    = "Push"
    CRM     = "CRM / Direct"


class UseCase(str, Enum):
    REACTIVATION    = "Re-Activation"
    CROSS_SELL      = "Cross-Sell"
    NEXT_BEST_OFFER = "Next Best Offer"
    ONBOARDING      = "Onboarding"
    RETENTION       = "Retention / Churn-Prevention"
    UPSELL          = "Upsell"


class AutomationDegree(str, Enum):
    SEGMENT     = "Segment-basiert (manuell kuratiert)"
    SCORING     = "Scoring-Modell (ML, human review)"
    AUTOMATED   = "Vollautomatisiert (kein human review)"


class ImpactType(str, Enum):
    CONTENT     = "Nur Content/Offer-Variation"
    FINANCIAL   = "Finanziell (Preis, Kredit, Rabatt)"
    ACCESS      = "Zugangsbeschränkend (Feature, Dienst)"


class PersonalizationLevel(str, Enum):
    GENERIC     = "Generic"
    SEGMENT     = "Segment-basiert"
    SCORE       = "Score-basiert (1:1 Scoring)"
    INDIVIDUAL  = "Vollindividuell (1:1 Automated)"


class Signal(str, Enum):
    GREEN   = "GREEN"
    YELLOW  = "YELLOW"
    RED     = "RED"


# ── Input DTO ─────────────────────────────────────────────────────────────────

@dataclass
class PersonalizationRequest:
    """Alle Eingabefelder des Decision-Support-Tools."""
    use_case:            UseCase
    channel:             Channel
    automation_degree:   AutomationDegree
    impact_type:         ImpactType
    personalization_level: PersonalizationLevel

    # Datenarten (Mehrfachauswahl)
    uses_behavioral_data:    bool = False   # GA4 / Clickstream
    uses_crm_data:           bool = False   # Transaktions-/Beziehungshistorie
    uses_geo_device:         bool = False   # Standort / Device
    uses_special_categories: bool = False   # DSGVO Art. 9 (Gesundheit, Religion …)

    # Ziel-KPI
    kpi: str = "Conversion Rate"

    # Risiko-Toleranz (0.0 = risk-averse, 1.0 = risk-tolerant)
    risk_tolerance: float = 0.5


# ── Ergebnis DTO ──────────────────────────────────────────────────────────────

@dataclass
class LevelProfile:
    """Performance + Risiko für einen Personalisierungsgrad."""
    level:             PersonalizationLevel
    performance_lift:  float   # relativer Lift vs. Generic (0.0 = baseline)
    risk_score:        float   # 0.0–1.0
    net_value:         float   # normierter NBV
    article22_trigger: bool
    dpia_required:     bool


@dataclass
class DecisionResult:
    """Vollständiger Output des Decision-Engines."""
    signal:             Signal
    recommended_level:  PersonalizationLevel
    net_business_value: float          # für gewählten Level
    performance_lift:   float          # für gewählten Level
    risk_score:         float          # für gewählten Level
    article22_triggered: bool
    dpia_required:      bool
    legal_basis:        str
    top_risk_drivers:   list[str]      = field(default_factory=list)
    guardrails:         list[str]      = field(default_factory=list)
    experiment_plan:    dict           = field(default_factory=dict)
    level_profiles:     list[LevelProfile] = field(default_factory=list)
    one_pager_md:       str            = ""


# ── Scoring-Logik ─────────────────────────────────────────────────────────────

class RiskScorer:
    """
    Berechnet den Risk-Score basierend auf Max' Framework
    (Risk = 0.3·Volume + 0.3·Sensitivity + 0.4·Granularity)
    plus kontextuelle Modifier aus den Formulareingaben.
    """

    # Basis-Scores je Personalisierungsgrad (aus Max' Analyse)
    _BASE_RISK: dict[PersonalizationLevel, float] = {
        PersonalizationLevel.GENERIC:    0.20,
        PersonalizationLevel.SEGMENT:    0.60,
        PersonalizationLevel.SCORE:      0.72,
        PersonalizationLevel.INDIVIDUAL: 0.90,
    }

    def score(self, req: PersonalizationRequest, level: PersonalizationLevel) -> tuple[float, list[str]]:
        """
        Returns (risk_score, risk_drivers).
        risk_score ist auf [0, 1] begrenzt.
        """
        base = self._BASE_RISK[level]
        drivers: list[str] = []
        delta = 0.0

        if req.uses_special_categories:
            delta += 0.20
            drivers.append("Besondere Datenkategorien (Art. 9 DSGVO) erhöhen Risiko erheblich")

        if req.impact_type == ImpactType.FINANCIAL:
            delta += 0.12
            drivers.append("Finanzieller Impact kann Art. 22 DSGVO auslösen")
        elif req.impact_type == ImpactType.ACCESS:
            delta += 0.15
            drivers.append("Zugangsbeschränkender Impact: Art. 22 DSGVO-Risiko hoch")

        if req.automation_degree == AutomationDegree.AUTOMATED and level in (
            PersonalizationLevel.SCORE, PersonalizationLevel.INDIVIDUAL
        ):
            delta += 0.10
            drivers.append("Vollautomatisierung ohne Human Review: Art. 22 wahrscheinlich anwendbar")

        if req.channel == Channel.PUSH:
            delta += 0.05
            drivers.append("Push-Kanal: erhöhte Wahrnehmung als aufdringlich (Reputationsrisiko)")
        elif req.channel == Channel.ADS:
            delta += 0.05
            drivers.append("Paid Ads: Targeting-Transparenz schwer kommunizierbar")

        if req.uses_geo_device and level == PersonalizationLevel.INDIVIDUAL:
            delta += 0.08
            drivers.append("Geo/Device + Individualmodell: Profiling-Tiefe nahe Tracking-Grenze")

        score = min(1.0, base + delta)

        # Nur die Top-3 Treiber ausgeben
        return round(score, 3), drivers[:3]


class LiftEstimator:
    """
    Schätzt Performance-Lift je Personalisierungsgrad.
    Basiert auf empirischen Werten aus dem Projekt + Kanal-/UseCase-Modifier.
    """

    # Empirische Basis-Lifts (aus Hypothesentests H1/H2, normiert auf Generic=0)
    _BASE_LIFT: dict[PersonalizationLevel, float] = {
        PersonalizationLevel.GENERIC:    0.00,   # Baseline
        PersonalizationLevel.SEGMENT:    1.22,   # +122% (11.7% → 26%)
        PersonalizationLevel.SCORE:      1.80,   # geschätzt zwischen Segment & Individual
        PersonalizationLevel.INDIVIDUAL: 2.60,   # AUC 94.3% → hohe Precision
    }

    # Kanal-Multiplikatoren (relative Wirksamkeit der Personalisierung)
    _CHANNEL_MULT: dict[Channel, float] = {
        Channel.EMAIL:  1.0,
        Channel.ONSITE: 1.15,
        Channel.ADS:    0.85,
        Channel.PUSH:   0.75,
        Channel.CRM:    1.10,
    }

    # UseCase-Multiplikatoren
    _USECASE_MULT: dict[UseCase, float] = {
        UseCase.REACTIVATION:    1.20,
        UseCase.CROSS_SELL:      1.00,
        UseCase.NEXT_BEST_OFFER: 1.10,
        UseCase.ONBOARDING:      0.90,
        UseCase.RETENTION:       1.05,
        UseCase.UPSELL:          0.95,
    }

    def estimate(self, req: PersonalizationRequest, level: PersonalizationLevel) -> float:
        """Returns relativer Performance-Lift (0.0 = kein Lift)."""
        base = self._BASE_LIFT[level]
        lift = base * self._CHANNEL_MULT[req.channel] * self._USECASE_MULT[req.use_case]
        return round(lift, 3)


# ── NBV-Berechnung ────────────────────────────────────────────────────────────

class NBVCalculator:
    """
    Netto-Business-Value = w_lift · lift_norm − w_risk · risk_score

    lift_norm: Lift auf [0,1] skaliert (max möglicher Lift = 1.0)
    risk_score: bereits auf [0,1]
    Gewichtung durch risk_tolerance des Users.
    """

    MAX_LIFT = 3.0  # Normierungsbasis

    def calculate(
        self,
        lift: float,
        risk: float,
        risk_tolerance: float,
    ) -> float:
        lift_norm = min(1.0, lift / self.MAX_LIFT)
        w_lift = 0.5 + risk_tolerance * 0.3    # höhere Toleranz → mehr Gewicht auf Lift
        w_risk = 1.0 - w_lift
        nbv = w_lift * lift_norm - w_risk * risk
        return round(nbv, 4)


# ── Signal-Logik ──────────────────────────────────────────────────────────────

def _derive_signal(risk: float, nbv: float, article22: bool, dpia_required: bool) -> Signal:
    if risk >= 0.80 or nbv < 0.0 or (article22 and not dpia_required):
        return Signal.RED
    if risk >= 0.60 or nbv < 0.15:
        return Signal.YELLOW
    return Signal.GREEN


def _article22_triggered(
    req: PersonalizationRequest,
    level: PersonalizationLevel,
) -> bool:
    """Art. 22 greift wenn: automatisiert + individuell + erheblicher Impact."""
    return (
        req.automation_degree == AutomationDegree.AUTOMATED
        and level in (PersonalizationLevel.SCORE, PersonalizationLevel.INDIVIDUAL)
        and req.impact_type in (ImpactType.FINANCIAL, ImpactType.ACCESS)
    )


def _dpia_required(risk: float, article22: bool) -> bool:
    return risk >= 0.75 or article22


def _legal_basis(risk: float, article22: bool, req: PersonalizationRequest) -> str:
    if req.uses_special_categories:
        return "Explizite Einwilligung (Art. 9 Abs. 2a DSGVO) — Pflicht"
    if article22:
        return "Explizite Einwilligung (Art. 22 Abs. 2c DSGVO) — Pflicht"
    if risk < 0.65:
        return "Berechtigtes Interesse (Art. 6 Abs. 1f) — LIA empfohlen"
    return "Einwilligung (Art. 6 Abs. 1a) — dringend empfohlen"


def _build_guardrails(
    signal: Signal,
    risk: float,
    article22: bool,
    req: PersonalizationRequest,
) -> list[str]:
    guardrails: list[str] = []

    if signal in (Signal.YELLOW, Signal.RED):
        guardrails.append("Frequency Cap: max. 3 Kontakte/Nutzer/Kampagne (Campaign-Fatigue-Tipping-Point)")
        guardrails.append("Transparenz-Notice im ersten Kontakt: Profiling-Hinweis + Opt-Out-Link")
        guardrails.append("Feature-Whitelist: nur datenschutzkonforme Features (keine besonderen Kategorien)")

    if risk >= 0.70:
        guardrails.append("Retention Limit: personalisierte Daten nach 90 Tagen inaktiver Nutzer löschen")
        guardrails.append("Explainability: Top-3-Treiber je Empfehlung dokumentieren (intern)")

    if article22:
        guardrails.append("PFLICHT: Human-Review-Gate vor jeder automatisierten Entscheidung")
        guardrails.append("PFLICHT: Recht auf Widerspruch aktiv kommunizieren (Art. 21 DSGVO)")
        guardrails.append("PFLICHT: Datenschutz-Folgenabschätzung (DPIA) vor Go-Live")

    if req.uses_special_categories:
        guardrails.append("PFLICHT: Separate Einwilligungserklärung für besondere Datenkategorien")

    if req.channel == Channel.PUSH:
        guardrails.append("Push-spezifisch: Opt-In-Rate als Guardrail-Metrik tracken (Ziel: >60%)")

    if not guardrails:
        guardrails.append("Keine kritischen Guardrails erforderlich — Standard-DSGVO-Compliance ausreichend")

    return guardrails


def _build_experiment_plan(
    req: PersonalizationRequest,
    level: PersonalizationLevel,
    lift: float,
) -> dict:
    holdout = 20 if lift > 1.0 else 30
    return {
        "design":          "A/B-Test mit Holdout-Gruppe",
        "holdout_pct":     holdout,
        "primary_kpi":     req.kpi,
        "guardrail_kpis": [
            "Opt-Out-Rate (Ziel: < 2% je Kontakt)",
            "Frequency-Cap-Violations (Ziel: 0)",
            "Complaint-Rate / Spam-Markierungen (Ziel: < 0.1%)",
        ],
        "min_runtime_days": 14,
        "significance_level": 0.05,
        "note": (
            "Tipping-Point-Monitoring: Response Rate je Kontaktanzahl wöchentlich prüfen. "
            f"Ab {3 if level == PersonalizationLevel.SEGMENT else 2} Kontakten ohne Response → Kontakt stoppen."
        ),
    }


def _build_one_pager(result: "DecisionResult", req: PersonalizationRequest) -> str:
    signal_emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}[result.signal.value]
    guardrails_md = "\n".join(f"- {g}" for g in result.guardrails)
    kpis_md = "\n".join(f"- {k}" for k in result.experiment_plan.get("guardrail_kpis", []))

    return f"""# Personalisierungs-Entscheid: {req.use_case.value}
**Datum:** _(automatisch generiert)_
**Kanal:** {req.channel.value} | **KPI:** {req.kpi}
**Empfohlener Level:** {result.recommended_level.value}

---

## Entscheid: {signal_emoji} {result.signal.value}

| Metrik | Wert |
|---|---|
| Performance-Lift (relativ) | +{result.performance_lift:.0%} |
| Risk Score | {result.risk_score:.2f} / 1.0 |
| Netto-Business-Value | {result.net_business_value:+.3f} |
| Art. 22 DSGVO | {'⚠️ Ausgelöst' if result.article22_triggered else '✓ Nicht ausgelöst'} |
| DPIA erforderlich | {'Ja — vor Go-Live' if result.dpia_required else 'Nein'} |

**Rechtsbasis:** {result.legal_basis}

---

## Top-Risiko-Treiber

{chr(10).join(f'- {d}' for d in result.top_risk_drivers) or '- Keine kritischen Treiber identifiziert'}

---

## Guardrails (Pflicht-To-dos)

{guardrails_md}

---

## Experiment-Plan

- **Design:** {result.experiment_plan.get('design', '')}
- **Holdout:** {result.experiment_plan.get('holdout_pct', '')}%
- **Laufzeit:** mind. {result.experiment_plan.get('min_runtime_days', '')} Tage
- **Primär-KPI:** {result.experiment_plan.get('primary_kpi', '')}

**Guardrail-KPIs:**
{kpis_md}

_{result.experiment_plan.get('note', '')}_

---
_Erstellt mit dem Personalisierungs-Decision-Tool (Cringe-Tipping MVP)_
"""


# ── Haupt-Engine ──────────────────────────────────────────────────────────────

class PersonalizationDecisionEngine:
    """
    Haupt-Orchestrator: nimmt einen PersonalizationRequest entgegen
    und gibt einen vollständigen DecisionResult zurück.
    """

    def __init__(self) -> None:
        self._risk_scorer   = RiskScorer()
        self._lift_estimator = LiftEstimator()
        self._nbv_calc      = NBVCalculator()

    def evaluate(self, req: PersonalizationRequest) -> DecisionResult:
        """Vollständige Evaluation für den gewählten Personalisierungsgrad."""
        all_levels = list(PersonalizationLevel)
        profiles: list[LevelProfile] = []

        for level in all_levels:
            risk, _ = self._risk_scorer.score(req, level)
            lift     = self._lift_estimator.estimate(req, level)
            nbv      = self._nbv_calc.calculate(lift, risk, req.risk_tolerance)
            art22    = _article22_triggered(req, level)
            dpia     = _dpia_required(risk, art22)
            profiles.append(LevelProfile(level, lift, risk, nbv, art22, dpia))

        # Gewählter Level
        chosen = next(p for p in profiles if p.level == req.personalization_level)
        risk, drivers = self._risk_scorer.score(req, req.personalization_level)
        signal   = _derive_signal(chosen.risk_score, chosen.net_value, chosen.article22_trigger, chosen.dpia_required)
        legal    = _legal_basis(chosen.risk_score, chosen.article22_trigger, req)
        guards   = _build_guardrails(signal, chosen.risk_score, chosen.article22_trigger, req)
        exp_plan = _build_experiment_plan(req, req.personalization_level, chosen.performance_lift)

        # Empfohlener Level = höchster NBV ohne RED-Signal
        recommended = max(
            (p for p in profiles if _derive_signal(p.risk_score, p.net_value, p.article22_trigger, p.dpia_required) != Signal.RED),
            key=lambda p: p.net_value,
            default=profiles[0],
        )

        result = DecisionResult(
            signal=signal,
            recommended_level=recommended.level,
            net_business_value=chosen.net_value,
            performance_lift=chosen.performance_lift,
            risk_score=chosen.risk_score,
            article22_triggered=chosen.article22_trigger,
            dpia_required=chosen.dpia_required,
            legal_basis=legal,
            top_risk_drivers=drivers,
            guardrails=guards,
            experiment_plan=exp_plan,
            level_profiles=profiles,
        )
        result.one_pager_md = _build_one_pager(result, req)
        return result
