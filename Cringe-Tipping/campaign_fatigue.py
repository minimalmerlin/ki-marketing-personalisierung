"""
Campaign Fatigue & Personalization Tipping Point Analysis
=========================================================
Analysiert den Punkt, ab dem steigende Kontaktintensität (Proxy für
Hyper-Personalisierung) die Conversion-Performance kippt.

Methodik:
    1. Response Rate je campaign-Kontaktanzahl berechnen
    2. Quadratische Regression fitten (β₂ < 0 → konkave Kurve)
    3. Tipping Point analytisch bestimmen: x* = -β₁ / (2·β₂)
    4. Statistischen Beweis via F-Test (linear vs. quadratisch)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from dataclasses import dataclass


@dataclass
class TippingPointResult:
    """Ergebnis der Tipping-Point-Analyse."""
    tipping_point: float          # Kontakt-Anzahl wo Performance peak ist
    beta_0: float                 # Intercept
    beta_1: float                 # Linearer Koeffizient
    beta_2: float                 # Quadratischer Koeffizient (negativ = konkav)
    r2_quadratic: float           # R² des quadratischen Modells
    r2_linear: float              # R² des linearen Modells (Vergleich)
    f_statistic: float            # F-Test: quadratisch vs. linear
    f_p_value: float              # p-Wert des F-Tests
    is_concave: bool              # True wenn β₂ < 0 (echter Tipping Point)
    campaign_stats: pd.DataFrame  # Aggregierte Statistiken je Gruppe


class CampaignFatigueAnalyzer:
    """
    Analysiert Campaign-Fatigue als Proxy für Personalisierungs-Overload.

    Die Anzahl der Marketing-Kontakte (campaign-Feature) wird als Intensitäts-
    Skala verwendet: mehr Kontakte = mehr Personalisierungsdruck auf das Individuum.
    """

    def __init__(self, max_campaigns: int = 10) -> None:
        """
        Args:
            max_campaigns: Obere Grenze für campaign-Gruppen (Ausreißer zusammenfassen).
        """
        self.max_campaigns = max_campaigns
        self._result: TippingPointResult | None = None

    def load_data(self, filepath: str, sep: str = ";") -> pd.DataFrame:
        """Lädt und bereinigt Bank-Marketing-Daten."""
        df = pd.read_csv(filepath, sep=sep)
        df["converted"] = (df["y"] == "yes").astype(int)

        # Ausreißer-Gruppen zusammenfassen (z.B. 11+ Kontakte → "10+")
        df["campaign_capped"] = df["campaign"].clip(upper=self.max_campaigns)

        return df

    def compute_group_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Berechnet Response Rate und Konfidenzintervalle je Kontaktgruppe.

        Konfidenzintervall: Wilson-Score-Methode (robust bei kleinen n).
        """
        groups = []

        for c_val, group in df.groupby("campaign_capped"):
            n = len(group)
            k = group["converted"].sum()
            rate = k / n if n > 0 else 0.0

            # Wilson-Score 95%-KI
            z = 1.96
            denom = 1 + z**2 / n
            center = (rate + z**2 / (2 * n)) / denom
            margin = (z * np.sqrt(rate * (1 - rate) / n + z**2 / (4 * n**2))) / denom
            ci_low = max(0.0, center - margin)
            ci_high = min(1.0, center + margin)

            groups.append({
                "campaign_contacts": int(c_val),
                "n_observations": n,
                "n_converted": int(k),
                "response_rate": round(rate, 4),
                "ci_low": round(ci_low, 4),
                "ci_high": round(ci_high, 4),
            })

        return pd.DataFrame(groups).sort_values("campaign_contacts").reset_index(drop=True)

    def fit_quadratic(self, stats_df: pd.DataFrame) -> TippingPointResult:
        """
        Fittet quadratische Regression auf die Gruppen-Response-Rates.

        Gewichtet nach Stichprobengröße (größere Gruppen → mehr Gewicht).
        """
        x = stats_df["campaign_contacts"].values.reshape(-1, 1)
        y = stats_df["response_rate"].values
        w = stats_df["n_observations"].values

        # Lineares Modell (Baseline)
        lin_reg = LinearRegression()
        lin_reg.fit(x, y, sample_weight=w)
        y_pred_lin = lin_reg.predict(x)
        r2_lin = r2_score(y, y_pred_lin, sample_weight=w)

        # Quadratisches Modell
        poly = PolynomialFeatures(degree=2, include_bias=True)
        x_poly = poly.fit_transform(x)
        quad_reg = LinearRegression(fit_intercept=False)
        quad_reg.fit(x_poly, y, sample_weight=w)
        y_pred_quad = quad_reg.predict(x_poly)
        r2_quad = r2_score(y, y_pred_quad, sample_weight=w)

        beta_0, beta_1, beta_2 = quad_reg.coef_

        # Tipping Point: Scheitel der Parabel x* = -β₁ / (2·β₂)
        if abs(beta_2) > 1e-10:
            tipping_point = -beta_1 / (2 * beta_2)
        else:
            tipping_point = float("nan")

        # F-Test: Bringt der quadratische Term signifikanten Mehrwert?
        n = len(y)
        rss_lin = np.sum(w * (y - y_pred_lin) ** 2)
        rss_quad = np.sum(w * (y - y_pred_quad) ** 2)
        f_stat = ((rss_lin - rss_quad) / 1) / (rss_quad / (n - 3)) if rss_quad > 0 else 0.0
        f_p_value = 1 - stats.f.cdf(f_stat, dfn=1, dfd=n - 3)

        self._result = TippingPointResult(
            tipping_point=round(tipping_point, 2),
            beta_0=round(beta_0, 6),
            beta_1=round(beta_1, 6),
            beta_2=round(beta_2, 6),
            r2_quadratic=round(r2_quad, 4),
            r2_linear=round(r2_lin, 4),
            f_statistic=round(f_stat, 4),
            f_p_value=round(f_p_value, 6),
            is_concave=bool(beta_2 < 0),
            campaign_stats=stats_df,
        )

        return self._result

    def run(self, filepath: str) -> TippingPointResult:
        """Vollständige Analyse-Pipeline."""
        df = self.load_data(filepath)
        stats_df = self.compute_group_stats(df)
        return self.fit_quadratic(stats_df)

    def summary(self) -> str:
        """Gibt einen lesbaren Bericht aus."""
        if self._result is None:
            return "Noch keine Analyse durchgeführt. run() zuerst aufrufen."

        r = self._result
        concave_str = "JA (β₂ < 0) → Echter Tipping Point nachgewiesen" if r.is_concave else "NEIN (β₂ ≥ 0) → Kein Tipping Point"

        return f"""
════════════════════════════════════════════════
  Campaign Fatigue — Tipping Point Analyse
════════════════════════════════════════════════

Modell:        y = {r.beta_0:.4f} + {r.beta_1:.4f}·x + {r.beta_2:.4f}·x²
Tipping Point: x* = {r.tipping_point} Kontakte

Konkave Kurve: {concave_str}

Modellgüte:
  R² (quadratisch): {r.r2_quadratic:.4f}
  R² (linear):      {r.r2_linear:.4f}
  Δ R²:             {r.r2_quadratic - r.r2_linear:+.4f}

F-Test (quad. vs. linear):
  F = {r.f_statistic:.4f}, p = {r.f_p_value:.6f}
  {"→ Quadratischer Term signifikant (p < 0.05)" if r.f_p_value < 0.05 else "→ Kein signifikanter Unterschied"}

Gruppen-Übersicht:
{r.campaign_stats[["campaign_contacts", "n_observations", "response_rate", "ci_low", "ci_high"]].to_string(index=False)}
════════════════════════════════════════════════
"""
