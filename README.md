# KI-gestützte Personalisierung im Marketing

> Abschlussprojekt · März 2026 · 3 Personen · 3 Wochen

---

## Forschungsfrage

> **"Inwieweit kann KI-gestützte Personalisierung im Marketing die Relevanz und Conversion von Kundenansprache erhöhen, ohne datenschutzrechtliche und ethische Grenzen zu überschreiten?"**

---

## Hypothesen

| ID | Hypothese | Notebook | Status |
|----|-----------|----------|--------|
| **H1** | Personalisierte Ansprache (segment-spezifisch) erzielt signifikant höhere Response-Raten als generische Massenkommunikation | `04_hypothesis_testing` | offen |
| **H2** | Verhaltensbasierte Segmentierung verbessert die Treffsicherheit von Produktempfehlungen messbar | `03_segmentation_analysis`, `04_hypothesis_testing` | offen |
| **H3** | Ab einem bestimmten Grad der Individualisierung entstehen DSGVO-konforme Risiken, die den Mehrwert überwiegen | `06_ethics_dsgvo_analysis` | offen |

---

## Repo-Struktur (EVA-Logik)

```
data/raw/        → E: Roheingabe (gitignored, lokal ablegen)
data/processed/  → V: Bereinigte Features (gitignored)
notebooks/       → V: Analyse & Modellierung
outputs/         → A: Plots, Tabellen für Bericht
docs/            → Projektdokumentation (SSOT)
src/             → Wiederverwendbare Python-Module
```

---

## Quick Start

### 1. Environment einrichten

```bash
make setup
# oder manuell:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Daten ablegen (keine Daten in Git!)

| Datensatz | Ziel-Pfad | Quelle |
|-----------|-----------|--------|
| GA4 BigQuery Sample | `data/raw/ga4_ecommerce/` | BigQuery public datasets |
| UCI Bank Marketing | `data/raw/bank_marketing/bank-full.csv` | UCI ML Repository |
| EDPB Profiling Guidelines | `data/external/edpb_profiling_guidelines.pdf` | edpb.europa.eu |
| ICO Guidance | `data/external/ico_guidance_profiling.pdf` | ico.org.uk |
| MIND (optional) | `data/raw/mind/` | Microsoft Research |

### 3. Notebooks in Reihenfolge ausführen

```
01_eda_ga4_ecommerce.ipynb       → EDA Verhaltensdaten (Person A)
02_eda_bank_marketing.ipynb      → EDA Kampagnendaten  (Person A/B)
03_segmentation_analysis.ipynb   → Segmentierung + H2  (Person A)
04_hypothesis_testing.ipynb      → H1 + H2 Tests       (Person A)
05_recommendation_logic.ipynb    → Empfehlungslogik     (Person B)
06_ethics_dsgvo_analysis.ipynb   → DSGVO-Analyse, H3   (Person C)
```

```bash
make notebook   # startet Jupyter Lab
```

---

## Team & Rollen

| Person | Lead-Verantwortung |
|--------|--------------------|
| **A** | EDA, Segmentierung, Hypothesentests (H1 + H2) |
| **B** | Recommender-Logik, Data Dictionary, Daten-Setup |
| **C** | DSGVO/Ethik-Analyse (H3), Berichtsschreiben, QA |

---

## Milestones

| Milestone | Woche | KW | Deliverable |
|-----------|-------|----|-------------|
| **M1** | Woche 1 | KW 13 | Daten geladen, EDA fertig (`01`, `02`), Charter final |
| **M2** | Woche 2 | KW 14 | Segmentierung + Tests (`03`, `04`, `05`), Zwischenpräsentation |
| **M3** | Woche 3 | KW 15 | DSGVO-Analyse (`06`), Bericht abgegeben, Abschlusspräsentation |

---

## Konventionen

- **Dateinamen:** `snake_case`, keine Leerzeichen
- **Commits:** `[scope] kurze Beschreibung`
  Beispiele: `[eda] add session funnel analysis`, `[docs] update charter hypotheses`
- **Scopes:** `eda`, `seg`, `hyp`, `rec`, `ethics`, `docs`, `fix`, `refactor`
- **Type Hints** in allen `.py`-Dateien
- **Kein echtes Datum** in Zellen-Outputs committen

---

## Scope

**In scope:** Digitales Marketing (E-Commerce, Display, Direct), Segmentierung, Empfehlungen,
CTR-Optimierung, DSGVO + EDPB + ICO, Explorative Analyse + konzeptionelle ML-Logik

**Out of scope:** Offline-Kanäle, RTB/Programmatic im Detail, CCPA/nicht-EU-Rechtsräume,
vollständige Produktions-ML-Implementierung

---

## Docs

| Dokument | Zweck |
|----------|-------|
| [`docs/project_charter.md`](docs/project_charter.md) | SSOT: Frage, Hypothesen, Rollen, Milestones, EVA-Architektur |
| [`docs/report_outline.md`](docs/report_outline.md) | Berichtsgliederung Kap. 1–9 + Anhang |
| [`docs/data_dictionary_template.md`](docs/data_dictionary_template.md) | Datensatz-Dokumentation (Person B ausfüllen) |
| [`docs/qa_checklist.md`](docs/qa_checklist.md) | QA-Gates vor Abgabe |

---

## Erweiterung: Cringe-Tipping — Der Personalisierungs-Tipping-Point

> **Fragestellung:** Ab welchem Punkt wird Personalisierung kontraproduktiv?

Max' ursprüngliche Analyse zeigt eine monoton steigende Kurve (mehr Personalisierung = mehr Performance). Diese Erweiterung prüft empirisch, ob es einen **Tipping Point** gibt — also einen Scheitel, ab dem weitere Personalisierung die Performance *senkt*.

### Methodik

Als Proxy für Personalisierungsintensität wird das Feature `campaign` (Anzahl der Kontaktversuche in der aktuellen Kampagne) verwendet:

| Kontakte | Interpretation |
|---|---|
| 1–2 | Erster Kontakt — neutrale, generische Ansprache |
| 3–4 | Gezieltes Follow-up — segment-basierte Personalisierung |
| 5+ | Wiederholter persönlicher Druck — Hyper-Personalisierung / „Cringe" |

Die **quadratische Regression** prüft, ob β₂ < 0 (konkave Kurve). Der Tipping Point ergibt sich analytisch als `x* = -β₁ / (2·β₂)`. Ein F-Test vergleicht das lineare gegen das quadratische Modell.

### Dateien

```
Cringe-Tipping/
├── cringe_tipping_analysis.ipynb   → Vollständige Analyse (Notebook)
├── campaign_fatigue.py             → CampaignFatigueAnalyzer (OOP-Modul)
└── outputs/
    ├── cringe_tipping_main.png     → Inverted-U-Kurve + Tipping Point Markierung
    ├── cringe_tipping_marginal.png → Marginale Effekte je Kontaktschritt
    ├── campaign_fatigue_stats.csv  → Response Rate je Gruppe mit 95%-KI
    └── model_parameters.csv        → Modell-Koeffizienten & Teststatistiken
```

### Verbindung zu H3

Diese Analyse ergänzt Max' theoretischen Risk-Score-Ansatz (`06_datenschutzanalyse_risk_score_h3.ipynb`) mit einem empirischen Befund:

- **Max zeigt:** Ab Risk Score > 0.7 überwiegen DSGVO-Risiken den Nutzen
- **Cringe-Tipping zeigt:** Ab ~x* Kontakten sinkt die tatsächliche Response Rate
- **Gemeinsame Aussage:** Hyper-Personalisierung ist weder compliance-konform noch wirksam — der optimale Punkt liegt dazwischen

### Ausführen

```bash
# Im Cringe-Tipping-Ordner
jupyter lab cringe_tipping_analysis.ipynb
```

Benötigt: `data/raw/bank_marketing/bank-additional-full.csv` (UCI ML Repository)
