# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B  
> **Status:** Fertig für M1 (KW 13)  
> **Zweck:** Vollständige Dokumentation aller genutzten Datensätze als SSOT für das Team  

---

## Datensatz 1: GA4 BigQuery Sample Ecommerce (Processed CSV)

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|-------------|-------|-----------|
| `event_date` | Datum des Events (YYYYMMDD) | INT64 | `20210131` | Nein | H2 — Nutzeraktivität variiert nach Datum |
| `event_timestamp` | Unix-Timestamp in Mikrosekunden | FLOAT64 | `1612069510766593.0` | Nein | — |
| `event_name` | Name des Events | STRING | `page_view`, `scroll`, `user_engagement` | Nein | H2 — Bestimmte Events korrelieren mit Engagement |
| `user_pseudo_id` | Anonymisierte User-ID (kein PII) | FLOAT64 (ursprünglich STRING) | `1026454.427` | Nein | H2 — Nutzerverhalten über Sessions analysierbar |
| `platform` | Plattform des Users | STRING | `WEB` | Nein | H2 — Verhalten unterscheidet sich zwischen Plattformen |
| `device_category` | Gerätetyp | STRING | `mobile` | Nein | H2 — Mobile Nutzer zeigen anderes Verhalten |
| `country` | Land des Users | STRING | `United States` | Nein | H2 — Geografische Unterschiede im Verhalten |
| *(weitere Felder ergänzen)* | | | | | |

---

**Quelle:** GA4 Export (Processed CSV)  
**Lizenz:** Google Public Data License  
**Zeitraum:** 2021‑01‑31  
**Zeilen:** 26.489  

---

## Besonderheiten / bekannte Probleme

- [x] Obfuskierte User-IDs — kein Cross-Device-Tracking möglich  
- [x] Keine demografischen Daten enthalten (GA4-typisch)  
- [x] `user_pseudo_id` wurde beim CSV‑Export zu FLOAT64 konvertiert  
  → Empfehlung: später in STRING casten  
- [x] Dieses Subset enthält nur Engagement-Events  
  → Keine Felder wie `transaction_id`, `purchase_revenue`, `items`  
- [x] Daten stammen nur aus einem einzigen Tag  
  → Für Zeitreihenanalysen ungeeignet  

---

## Hinweis für das Team

Dieser Datensatz eignet sich besonders für:

- Analyse von Nutzerverhalten  
- Event-basierte Segmentierung  
- Modellierung von Engagement  
- Vorbereitung für KI‑gestützte Personalisierungsmodelle  

Für Kauf- oder Revenue-Modelle wird ein zusätzlicher Datensatz benötigt.


---
# UCI Bank Marketing Dataset (Numeric-Encoded Version)

This repository contains the numeric-encoded version of the UCI Bank Marketing dataset with 41,188 rows and 21 columns.

## 📘 Data Dictionary

| Column | Description | Type | Notes |
|--------|-------------|------|--------|
| age | Customer age | int | — |
| job | Job category (encoded) | int | Original categories mapped to integers |
| marital | Marital status (encoded) | int | — |
| education | Education level (encoded) | int | — |
| default | Credit default history (encoded) | int | Values include -1, 0, 1 |
| housing | Housing loan (encoded) | int | — |
| loan | Personal loan (encoded) | int | — |
| contact | Contact communication type (encoded) | int | — |
| month | Last contact month (encoded) | int | — |
| day_of_week | Last contact weekday (encoded) | int | — |
| duration | Call duration (seconds) | int | ⚠️ Should be excluded from predictive modeling |
| campaign | Number of contacts during this campaign | int | — |
| pdays | Days since last contact | int | -1 = never contacted |
| previous | Number of previous contacts | int | — |
| poutcome | Outcome of previous campaign (encoded) | int | — |
| emp.var.rate | Employment variation rate | float | Macro-economic |
| cons.price.idx | Consumer price index | float | Macro-economic |
| cons.conf.idx | Consumer confidence index | float | Macro-economic |
| euribor3m | Euribor 3-month rate | float | Macro-economic |
| nr.employed | Number of employees | float | Macro-economic |
| y | Target variable (0 = no, 1 = yes) | int | — |

## Dataset Info
- Rows: 41,188  
- Columns: 21  
- Missing Values: 0% in all columns  
- Target: `y` (0 = no, 1 = yes)


## Datensatz 3: EDPB Profiling Guidelines (WP 251 rev.01)

| Feld | Inhalt |
|------|--------|
| **Dokument-Typ** | Regulatorisches Leitlinienpapier |
| **Herausgeber** | European Data Protection Board (EDPB) |
| **Datei** | `data/external/edpb_guidelines_profiling_wp251.pdf` |
| **Relevanz** | Definition Profiling, Art. 22 DSGVO, Rechtsgrundlagen |
| **Kapitel für H3** | Kap. 3 (Definition), Kap. 5 (Rechtsgrundlagen), Kap. 7 (Spezifische Situationen) |

---

## Datensatz 4: ICO Guidance on Profiling

| Feld | Inhalt |
|------|--------|
| **Dokument-Typ** | Regulatorisches Leitlinienpapier |
| **Herausgeber** | Information Commissioner's Office (UK) |
| **Datei** | `data/external/ico_guidance_profiling.pdf` |
| **Relevanz** | UK GDPR-Auslegung, Profiling-Risiken, DPIA-Anforderungen |
| **Kapitel für H3** | Abschnitt "What is profiling?", "When can we profile?" |

---

## Datensatz 5: MIND — Microsoft News Dataset *(optional)*

| Feld | Beschreibung | Typ | Hypothese |
|------|-------------|-----|-----------|
| `user_id` | Anonymisierte User-ID | STRING | H2 |
| `history` | Klick-Historie (Artikel-IDs) | ARRAY | H2 |
| `impressions` | Gezeigte Artikel + Klick-Label | ARRAY | H2 |

**Quelle:** Microsoft Research — MIND Dataset
**Status:** Optional — nur wenn GA4 für Recommender nicht ausreicht
**Datei:** `data/raw/mind/` (nach Download entpacken)

---

## Feature Engineering Log

> Hier dokumentieren wir, welche neuen Features aus den Rohdaten abgeleitet wurden.

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `rfm_recency` | GA4 | Tage seit letztem `purchase`-Event | `src/data/preprocessor.py` |
| `rfm_frequency` | GA4 | Anzahl `purchase`-Events je `user_pseudo_id` | `src/data/preprocessor.py` |
| `rfm_monetary` | GA4 | Summe `ecommerce.purchase_revenue` je User | `src/data/preprocessor.py` |
| `rfm_score` | GA4 | Quintil-Score 1–5 für R, F, M kombiniert | `src/analysis/segmentation.py` |
| `cluster_label` | GA4 | KMeans-Cluster-ID | `src/analysis/segmentation.py` |

### Zusätzliche GA4 Features
| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `event_count` | GA4 | Gesamtanzahl aller Events pro User | `src/data/preprocessor.py` |
| `unique_event_types` | GA4 | Anzahl unterschiedlicher Event-Namen | `src/data/preprocessor.py` |
| `avg_session_events` | GA4 | Durchschnittliche Events pro Session | `src/data/preprocessor.py` |
| `is_mobile` | GA4 | 1 wenn `device_category = mobile` | `src/data/preprocessor.py` |
| `country_group` | GA4 | EU / Non‑EU / Other basierend auf `country` | `src/data/preprocessor.py` |
| `user_activity_score` | GA4 | Normierte Kombination aus `event_count` + Engagement | `src/analysis/recommender.py` |
| `engagement_level` | GA4 | Low / Medium / High basierend auf Event-Intensität | `src/analysis/recommender.py` |

### Bank Marketing Features
| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `contact_intensity` | Bank | `campaign + previous` | `src/data/preprocessor.py` |
| `is_first_contact` | Bank | 1 wenn `pdays = -1` | `src/data/preprocessor.py` |
| `call_success_rate` | Bank | `previous_success / previous` | `src/data/preprocessor.py` |
| `age_bucket` | Bank | Altersgruppen (18–30, 31–45, 46–60, 60+) | `src/data/preprocessor.py` |
| `economic_stress_index` | Bank | Normierte Kombination der Makro-Variablen | `src/data/preprocessor.py` |

### Recommender-spezifische Features
| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `similarity_vector` | GA4 / Content | TF‑IDF oder Embedding-Vektor für Content-Ähnlichkeit | `src/analysis/recommender.py` |
| `precision_at_k_input` | GA4 | Nutzer- und Item-Matrix für Präzisionsberechnung | `src/analysis/recommender.py` |

