# Berichtsgliederung — KI-gestützte Personalisierung im Marketing

> Version: 1.0 | Stand: März 2026
> Zielformat: ~25–35 Seiten + Anhang | Sprache: Deutsch
> Verantwortlichkeiten: A = Person A, B = Person B, C = Person C

---

## Kapitel 1 — Einleitung *(~3 Seiten | Person C)*

### 1.1 Problemstellung & Relevanz
- Marketing-Shift: Von Massenkommunikation zu KI-gestützter Personalisierung
- Spannungsfeld: Conversion-Optimierung vs. DSGVO-Konformität
- Praxisrelevanz für Unternehmen im DACH-Raum

### 1.2 Zielsetzung & Forschungsfrage
> "Inwieweit kann KI-gestützte Personalisierung im Marketing die Relevanz und Conversion von Kundenansprache erhöhen, ohne datenschutzrechtliche und ethische Grenzen zu überschreiten?"

### 1.3 Aufbau der Arbeit
- Kurze Übersicht der Kapitelstruktur (Roadmap für Leser)

**Deliverable:** Problemraum klar umrissen, Frage präzise formuliert, Leser weiß wohin die Arbeit führt.

---

## Kapitel 2 — Theoretischer Rahmen *(~5 Seiten | Person C)*

### 2.1 KI-gestützte Personalisierung: Definitionen & Formen
- Personalisierungsgrade: regelbasiert → segmentbasiert → individuell
- Technologien: Collaborative Filtering, Content-Based, Hybrid Recommender
- Abgrenzung: Personalisierung vs. Profiling (DSGVO Art. 4 Nr. 4)

### 2.2 Customer Segmentation als Grundlage
- RFM-Modell (Recency, Frequency, Monetary)
- Verhaltensbasierte vs. demografische Segmentierung
- Clustering-Verfahren (KMeans, DBSCAN) — konzeptionelle Einführung

### 2.3 Rechtlicher Rahmen: DSGVO & Leitlinien
- Art. 5 (Grundsätze), Art. 6 (Rechtsgrundlagen), Art. 22 (Automatisierte Entscheidungen)
- EDPB Guidelines on Profiling (WP 251 rev.01)
- ICO Guidance: Profiling & Automated Decision Making
- Abwägung: berechtigtes Interesse vs. datenschutzrechtliche Risiken

### 2.4 Ethischer Rahmen
- Fairness & Diskriminierungsvermeidung in Empfehlungssystemen
- Transparenz & Explainability
- Privacy by Design als Designprinzip

**Verknüpfung zu Hypothesen:** H3 wird hier theoretisch fundiert.

---

## Kapitel 3 — Stand der Forschung *(~3 Seiten | Person C)*

### 3.1 Empirische Befunde zur Wirksamkeit von Personalisierung
- Conversion-Lift durch Personalisierung (Literatur-Review)
- Grenzen der Personalisierung: Creepiness-Faktor, Reaktanz

### 3.2 DSGVO-Compliance in der Praxis
- Aktuelle Bußgeldfälle (DPA-Entscheidungen)
- Herausforderungen für E-Commerce-Unternehmen

### 3.3 Forschungslücke & Positionierung dieser Arbeit

---

## Kapitel 4 — Daten & Methodik *(~4 Seiten | Person A + B)*

### 4.1 Datensätze & Auswahl
- GA4 BigQuery Sample: Beschreibung, Struktur, Relevanz
- UCI Bank Marketing: Beschreibung, Struktur, Zielvariable
- Begründung der Datenwahl (Datenfit-Checkliste → Verweis auf `data_dictionary`)

### 4.2 Datenaufbereitung
- Cleaning-Schritte (fehlende Werte, Duplikate, Encoding)
- Feature Engineering: RFM-Score, Session-Aggregation
- Verweis auf `src/data/preprocessor.py`

### 4.3 Analysemethoden

| Hypothese | Methode | Metrik |
|-----------|---------|--------|
| H1 | Chi²-Test, t-Test | p-Wert, Cramér's V / Cohen's d |
| H2 | KMeans + Silhouette | Silhouette-Score, Precision@K |
| H3 | Qualitative Analyse + Stufenmodell | Risiko-Score-Matrix |

### 4.4 Limitationen
- Sample-Bias bei GA4-Daten
- Bank Marketing: zeitlich limitiert, nicht EU-Markt
- H3: keine empirische Erhebung, konzeptionell

---

## Kapitel 5 — Explorative Datenanalyse (EDA) *(~4 Seiten | Person A)*

### 5.1 GA4 Ecommerce — Verhaltensdaten
- Session-Muster, Conversion Funnel, Top-Produktkategorien
- User-Segmentierung nach Aktivität
- Key Findings mit Visualisierungen

### 5.2 Bank Marketing — Kampagnendaten
- Verteilung demografischer Merkmale
- Response-Rate gesamt vs. nach Segmenten
- Korrelationsanalyse relevanter Features

### 5.3 Synthese: Was sagen die Daten über Personalisierungspotenzial?

**Abbildungen (aus `outputs/figures/`):**
- `fig_01_session_funnel.png`
- `fig_02_rfm_distribution.png`
- `fig_03_bank_response_by_segment.png`

---

## Kapitel 6 — Analyse & Ergebnisse *(~6 Seiten | Person A + B)*

### 6.1 H1: Conversion — Testergebnisse
- Segmentierung nach Response-Merkmalen
- Ergebnis Chi²-Test / t-Test
- Interpretation: H1 bestätigt/widerlegt/teilweise bestätigt + Begründung

### 6.2 H2: Relevanz — Segmentierung & Empfehlungen
- RFM-Segmente: Beschreibung der identifizierten Cluster
- Silhouette-Score-Auswertung
- Precision@K: segmentiert vs. naiv
- Interpretation: H2 bestätigt/widerlegt + Begründung

### 6.3 H3: Grenze — DSGVO-Risiko-Analyse
- Profiling-Stufenmodell (Stufe 1–4)
- Rechtsgrundlagen-Matrix: Personalisierungsgrad vs. Rechtsrisiko
- Ab wann wird aus berechtigtem Interesse ein DSGVO-Problem?
- Interpretation: H3 bestätigt/widerlegt + Schwellenwert-Diskussion

**Abbildungen (aus `outputs/figures/`):**
- `fig_04_cluster_visualization.png`
- `fig_05_hypothesis_results_summary.png`
- `fig_06_profiling_risk_matrix.png`

---

## Kapitel 7 — Diskussion *(~3 Seiten | Person C)*

### 7.1 Zusammenführung der Hypothesen
- H1 + H2 gemeinsam gelesen: Wo liegt der Conversion-Lift tatsächlich?
- H3 als Korrektiv: Was limitiert die Anwendung in der Praxis?

### 7.2 Implikationen für die Praxis
- Empfehlung: Segment-level statt Individual-level Personalisierung als DSGVO-konformer Mittelweg
- Privacy-Enhancing Technologies (PETs) als Enabler

### 7.3 Kritische Reflexion
- Limitationen der Datensätze
- Generalisierbarkeit der Ergebnisse
- Was hätte mit echten Produktionsdaten anders ausgesehen?

---

## Kapitel 8 — Handlungsempfehlungen *(~2 Seiten | Person C)*

### 8.1 Für Marketing-Teams
- Segment-basierte Personalisierung als Einstieg
- Consent-Management als Wettbewerbsvorteil

### 8.2 Für Data/ML-Teams
- Privacy by Design in der Feature-Selektion
- Dokumentationspflichten (DSGVO Art. 30)

### 8.3 Für Compliance/Legal
- Profiling-Schwellenwert-Modell als internes Governance-Tool
- DPIA-Trigger-Kriterien

---

## Kapitel 9 — Fazit & Ausblick *(~2 Seiten | Person C)*

### 9.1 Beantwortung der Forschungsfrage
- Synthetische Antwort auf Basis H1+H2+H3
- "Ja, aber mit klaren Grenzen..."

### 9.2 Ausblick
- Federated Learning als datenschutzfreundliche Alternative
- EU AI Act und seine Implikationen für Marketing-KI
- Real-Time Personalisierung vs. Batch-Segmentierung

---

## Anhang

| Anhang | Inhalt | Erstellt von |
|--------|--------|--------------|
| A | Data Dictionary (vollständig) | Person B |
| B | Vollständige Hypothesentest-Outputs | Person A |
| C | DSGVO-Rechtsgrundlagen-Tabelle | Person C |
| D | Notebook-Ausführungsprotokoll | Person A/B |
| E | Literaturverzeichnis | Alle |

---

## Verknüpfungsmatrix (Hypothesen ↔ Kapitel)

| Element | Kap. 1 | Kap. 2 | Kap. 3 | Kap. 4 | Kap. 5 | Kap. 6 | Kap. 7 | Kap. 8 |
|---------|--------|--------|--------|--------|--------|--------|--------|--------|
| H1 Conversion | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** | ✓ | ✓ |
| H2 Relevanz | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** | ✓ | ✓ |
| H3 Grenze | ✓ | **✓** | ✓ | ✓ | — | **✓** | ✓ | ✓ |
| DSGVO | — | **✓** | ✓ | — | — | ✓ | ✓ | **✓** |
