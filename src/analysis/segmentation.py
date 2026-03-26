"""
Segmentierungslogik: KMeans-Clustering auf RFM-Daten.
EVA: Verarbeitung → Cluster-Labels als Ausgabe.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class RFMSegmentation:
    """KMeans-Segmentierung auf RFM-Features."""

    def __init__(self, n_clusters: int = 4, random_state: int = 42) -> None:
        self.n_clusters = n_clusters
        self.random_state = random_state
        self._scaler = StandardScaler()
        self._model: KMeans | None = None
        self.silhouette_score_: float | None = None

    def fit_predict(
        self,
        rfm_df: pd.DataFrame,
        features: list[str] | None = None,
    ) -> pd.DataFrame:
        """Skaliert RFM-Features und clustert mit KMeans.

        Args:
            rfm_df: Output von GA4RFMPreprocessor.compute_rfm()
            features: Zu nutzende Spalten (default: recency_days, frequency, monetary)

        Returns:
            rfm_df mit zusätzlicher Spalte 'cluster_label'
        """
        if features is None:
            features = ["recency_days", "frequency", "monetary"]

        df = rfm_df.copy()
        X = self._scaler.fit_transform(df[features])

        self._model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init="auto",
        )
        df["cluster_label"] = self._model.fit_predict(X)

        # Silhouette-Score berechnen (Qualitätsmetrik für H2)
        self.silhouette_score_ = float(silhouette_score(X, df["cluster_label"]))

        return df

    def find_optimal_k(
        self,
        rfm_df: pd.DataFrame,
        k_range: range = range(2, 8),
        features: list[str] | None = None,
    ) -> pd.DataFrame:
        """Vergleicht Silhouette-Scores für verschiedene k-Werte.

        Returns:
            DataFrame mit Spalten: k, silhouette_score
        """
        if features is None:
            features = ["recency_days", "frequency", "monetary"]

        X = self._scaler.fit_transform(rfm_df[features])
        results = []

        for k in k_range:
            model = KMeans(n_clusters=k, random_state=self.random_state, n_init="auto")
            labels = model.fit_predict(X)
            score = silhouette_score(X, labels)
            results.append({"k": k, "silhouette_score": score})

        return pd.DataFrame(results)
