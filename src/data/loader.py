"""
Datei-Loader für alle Datensätze des Projekts.
EVA: Eingabe-Schicht — rohe Daten laden, nichts transformieren.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# Repo-Root relativ zu dieser Datei bestimmen
REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"


def load_bank_marketing(filename: str = "bank-additional-full.csv") -> pd.DataFrame:
    """Lädt den UCI Bank Marketing Datensatz (;-separiert).

    Args:
        filename: Dateiname im Verzeichnis data/raw/bank_marketing/

    Returns:
        DataFrame mit 17 Spalten (inkl. Zielvariable 'y')
    """
    path = RAW_DIR / "bank_marketing" / filename
    df = pd.read_csv(path, sep=";")
    return df


def load_ga4_events(filename: str = "ga4_events.csv") -> pd.DataFrame:
    """Lädt GA4-Event-Daten (CSV-Export aus BigQuery).

    Args:
        filename: Dateiname im Verzeichnis data/raw/ga4_ecommerce/

    Returns:
        DataFrame mit GA4 Event-Rohdaten
    """
    path = RAW_DIR / "ga4_ecommerce" / filename
    df = pd.read_csv(path)
    return df


def load_mind_behaviors(split: str = "train") -> pd.DataFrame:
    """Lädt MIND User-Behavior-Daten (optional).

    Args:
        split: 'train' oder 'dev'

    Returns:
        DataFrame mit user_id, time, history, impressions
    """
    path = RAW_DIR / "mind" / split / "behaviors.tsv"
    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["impression_id", "user_id", "time", "history", "impressions"],
    )
    return df
