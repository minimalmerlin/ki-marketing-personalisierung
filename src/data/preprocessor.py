"""
Preprocessing-Logik für alle Datensätze.
EVA: Verarbeitungs-Schicht — Cleaning, Feature Engineering, RFM-Berechnung.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
from datetime import datetime


class BankMarketingPreprocessor:
    """Bereinigt und feature-engineert den UCI Bank Marketing Datensatz."""

    # duration sollte für realistische Tests ausgeschlossen werden
    # (Post-Contact-Information, siehe Data Dictionary)
    LEAKAGE_COLS = ["duration"]

    def fit_transform(self, df: pd.DataFrame, drop_leakage: bool = True) -> pd.DataFrame:
        """Vollständige Preprocessing-Pipeline.

        Args:
            df: Rohdaten aus loader.load_bank_marketing()
            drop_leakage: Wenn True, wird 'duration' entfernt

        Returns:
            Bereinigter DataFrame mit kodierten Kategorien
        """
        df = df.copy()

        # pdays: 999 = "nie kontaktiert" → separate Flag
        df["was_contacted_before"] = (df["pdays"] != 999).astype(int)
        df["pdays"] = df["pdays"].replace(999, np.nan)

        # Zielvariable binär kodieren
        df["y_binary"] = (df["y"] == "yes").astype(int)

        if drop_leakage:
            df = df.drop(columns=self.LEAKAGE_COLS, errors="ignore")

        return df


class GA4RFMPreprocessor:
    """Berechnet RFM-Scores aus GA4-Event-Daten."""

    def compute_rfm(
        self,
        df: pd.DataFrame,
        reference_date: datetime | None = None,
        user_col: str = "user_pseudo_id",
        date_col: str = "event_date",
        revenue_col: str = "purchase_revenue",
    ) -> pd.DataFrame:
        """Berechnet Recency, Frequency, Monetary je User.

        Args:
            df: GA4 Purchase-Events (bereits auf event_name='purchase' gefiltert)
            reference_date: Referenzdatum für Recency (default: max(event_date))
            user_col: Spaltenname der User-ID
            date_col: Spaltenname des Event-Datums (YYYYMMDD als String oder datetime)
            revenue_col: Spaltenname des Umsatzes

        Returns:
            DataFrame mit Spalten: user_id, recency_days, frequency, monetary, rfm_score
        """
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], format="%Y%m%d", errors="coerce")

        if reference_date is None:
            reference_date = df[date_col].max()

        rfm = (
            df.groupby(user_col)
            .agg(
                recency_days=(date_col, lambda x: (reference_date - x.max()).days),
                frequency=(date_col, "count"),
                monetary=(revenue_col, "sum"),
            )
            .reset_index()
        )

        # Quintil-Scores 1–5 (5 = bester Wert)
        # Recency: niedrigerer Wert = besser → invertieren
        rfm["r_score"] = pd.qcut(rfm["recency_days"], q=5, labels=[5, 4, 3, 2, 1])
        rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])
        rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])

        rfm["rfm_score"] = (
            rfm["r_score"].astype(int)
            + rfm["f_score"].astype(int)
            + rfm["m_score"].astype(int)
        )

        return rfm
