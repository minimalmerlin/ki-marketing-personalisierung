"""
Konzeptionelle Recommender-Logik (kollaborative Filterung, segmentbasiert).
EVA: Verarbeitung → Top-N-Empfehlungen als Ausgabe.
Kein Produktionssystem — Proof-of-Concept für H2.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SegmentBasedRecommender:
    """Empfiehlt Produkte basierend auf Segment-Profilen (item popularity per segment).

    Ansatz: Für jedes Cluster wird ein Produkt-Popularitätsprofil berechnet.
    Empfehlung = Top-N Produkte im Cluster des Users, die er noch nicht gesehen hat.
    """

    def __init__(self, top_n: int = 5) -> None:
        self.top_n = top_n
        self._segment_profiles: dict[int, pd.Series] = {}

    def fit(
        self,
        interactions: pd.DataFrame,
        user_col: str = "user_id",
        item_col: str = "item_id",
        segment_col: str = "cluster_label",
    ) -> "SegmentBasedRecommender":
        """Berechnet Popularitätsprofil je Segment.

        Args:
            interactions: User-Item-Interaktionen mit Segment-Label
        """
        for segment, group in interactions.groupby(segment_col):
            # Anzahl Käufe je Produkt im Segment normiert
            profile = group[item_col].value_counts(normalize=True)
            self._segment_profiles[int(segment)] = profile
        return self

    def predict(
        self,
        user_id: str,
        user_segment: int,
        already_seen: list[str] | None = None,
    ) -> list[str]:
        """Gibt Top-N Empfehlungen für einen User zurück.

        Args:
            user_id: User-Identifier (für Logging)
            user_segment: Cluster-Label des Users
            already_seen: Items, die ausgeschlossen werden sollen

        Returns:
            Liste mit bis zu top_n Item-IDs
        """
        if user_segment not in self._segment_profiles:
            return []

        profile = self._segment_profiles[user_segment]
        if already_seen:
            profile = profile.drop(labels=already_seen, errors="ignore")

        return profile.head(self.top_n).index.tolist()

    def precision_at_k(
        self,
        recommendations: list[str],
        relevant_items: list[str],
    ) -> float:
        """Berechnet Precision@K für eine einzelne Empfehlung.

        Args:
            recommendations: Liste der empfohlenen Items (len = K)
            relevant_items: Liste der tatsächlich interagierten Items

        Returns:
            Precision@K als Float zwischen 0 und 1
        """
        if not recommendations:
            return 0.0
        hits = len(set(recommendations) & set(relevant_items))
        return hits / len(recommendations)
