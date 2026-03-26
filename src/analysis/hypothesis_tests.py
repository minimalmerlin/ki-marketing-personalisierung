"""
Hypothesentests für H1 und H2.
EVA: Verarbeitung → p-Werte, Effektstärken als Ausgabe.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
from scipy import stats
from dataclasses import dataclass


@dataclass
class TestResult:
    """Strukturiertes Ergebnis eines statistischen Tests."""
    hypothesis: str
    test_name: str
    statistic: float
    p_value: float
    effect_size: float
    effect_size_name: str
    significant: bool  # alpha = 0.05
    interpretation: str


def test_h1_conversion(
    df: pd.DataFrame,
    segment_col: str,
    target_col: str = "y_binary",
    alpha: float = 0.05,
) -> TestResult:
    """H1: Personalisierte (segment-spezifische) Ansprache → höhere Response-Rate?

    Methode: Chi²-Test auf Kontingenztabelle Segment × Response

    Args:
        df: DataFrame mit Segment-Labels und binärer Zielvariable
        segment_col: Spalte mit Segment-Labels
        target_col: Binäre Zielvariable (0/1)
        alpha: Signifikanzniveau

    Returns:
        TestResult mit Chi²-Statistik, p-Wert und Cramér's V
    """
    contingency = pd.crosstab(df[segment_col], df[target_col])
    chi2, p_value, dof, _ = stats.chi2_contingency(contingency)

    # Cramér's V (Effektstärke für kategoriale Variablen)
    n = contingency.values.sum()
    cramers_v = float(np.sqrt(chi2 / (n * (min(contingency.shape) - 1))))

    return TestResult(
        hypothesis="H1",
        test_name="Chi²-Test",
        statistic=float(chi2),
        p_value=float(p_value),
        effect_size=cramers_v,
        effect_size_name="Cramér's V",
        significant=p_value < alpha,
        interpretation=(
            f"Response-Raten unterscheiden sich signifikant zwischen Segmenten "
            f"(Chi²={chi2:.2f}, p={p_value:.4f}, V={cramers_v:.3f})"
            if p_value < alpha
            else f"Kein signifikanter Unterschied zwischen Segmenten (p={p_value:.4f})"
        ),
    )


def test_h2_precision(
    baseline_precision: float,
    segmented_precision: float,
    n_users: int,
    alpha: float = 0.05,
) -> TestResult:
    """H2: Segmentierte Empfehlung → bessere Precision@K als naive Baseline?

    Methode: Binomial-Proportionstest (segmentiert vs. Baseline)

    Args:
        baseline_precision: Precision@K ohne Segmentierung
        segmented_precision: Precision@K mit Segmentierung
        n_users: Anzahl evaluierter User
        alpha: Signifikanzniveau

    Returns:
        TestResult mit z-Statistik und p-Wert
    """
    # Einseitiger z-Test: segmentiert > baseline
    se = float(np.sqrt(
        (baseline_precision * (1 - baseline_precision) / n_users)
        + (segmented_precision * (1 - segmented_precision) / n_users)
    ))
    z = (segmented_precision - baseline_precision) / se if se > 0 else 0.0
    p_value = float(1 - stats.norm.cdf(z))  # einseitig

    lift = (
        (segmented_precision - baseline_precision) / baseline_precision
        if baseline_precision > 0
        else 0.0
    )

    return TestResult(
        hypothesis="H2",
        test_name="Proportionstest (einseitig)",
        statistic=z,
        p_value=p_value,
        effect_size=lift,
        effect_size_name="Relativer Lift",
        significant=p_value < alpha,
        interpretation=(
            f"Segmentierte Empfehlung signifikant besser: Lift={lift:.1%} (p={p_value:.4f})"
            if p_value < alpha
            else f"Kein signifikanter Precision-Vorteil durch Segmentierung (p={p_value:.4f})"
        ),
    )
