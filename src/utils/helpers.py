"""
Gemeinsame Hilfsfunktionen: Plotting, Pfade, Logging.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.figure
import seaborn as sns

# Repo-Root und Output-Verzeichnisse
REPO_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = REPO_ROOT / "outputs" / "figures"
TABLES_DIR = REPO_ROOT / "outputs" / "tables"

# Einheitliches Plot-Styling
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)


def save_figure(fig: matplotlib.figure.Figure, filename: str) -> Path:
    """Speichert eine Matplotlib-Figure nach outputs/figures/.

    Args:
        fig: Matplotlib Figure-Objekt
        filename: Dateiname (ohne Pfad), z.B. 'fig_01_rfm_distribution.png'

    Returns:
        Absoluter Pfad zur gespeicherten Datei
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Figure gespeichert: {path.relative_to(REPO_ROOT)}")
    return path


def save_table(df, filename: str) -> Path:
    """Speichert einen DataFrame als CSV nach outputs/tables/.

    Args:
        df: pandas DataFrame
        filename: Dateiname (ohne Pfad), z.B. 'table_01_rfm_scores.csv'

    Returns:
        Absoluter Pfad zur gespeicherten Datei
    """
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLES_DIR / filename
    df.to_csv(path, index=False)
    print(f"Tabelle gespeichert: {path.relative_to(REPO_ROOT)}")
    return path


def print_hypothesis_result(result) -> None:
    """Gibt ein TestResult-Objekt formatiert in der Konsole aus."""
    separator = "─" * 60
    print(separator)
    print(f"  {result.hypothesis} | {result.test_name}")
    print(separator)
    print(f"  Statistik:    {result.statistic:.4f}")
    print(f"  p-Wert:       {result.p_value:.4f}")
    print(f"  Effektstärke: {result.effect_size:.4f} ({result.effect_size_name})")
    print(f"  Signifikant:  {'✓ JA' if result.significant else '✗ NEIN'} (α = 0.05)")
    print(f"  → {result.interpretation}")
    print(separator)
