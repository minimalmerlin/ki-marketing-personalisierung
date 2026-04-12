# Data Dictionary — KI-Marketing-Personalisierung
**Version:** 3.0  
**Datum:** 2026-04-12  
**Status:** Vollständig — synchron mit Codestand

---

## Inhaltsverzeichnis

1. [Datensatz 1 — GA4 Raw Events](#1-datensatz-1--ga4-raw-events)
2. [Datensatz 2 — GA4 User-Level](#2-datensatz-2--ga4-user-level)
3. [Datensatz 3 — GA4 Segmentation](#3-datensatz-3--ga4-segmentation)
4. [Datensatz 4 — GA4 Recommender Dataset](#4-datensatz-4--ga4-recommender-dataset)
5. [Datensatz 5 — Bank Marketing (bank-full.csv)](#5-datensatz-5--bank-marketing-bank-fullcsv)
6. [Datensatz 6 — Bank Marketing Additional (bank-additional-full.csv)](#6-datensatz-6--bank-marketing-additional-bank-additional-fullcsv)
7. [Datensatz 7 — Bank Segments](#7-datensatz-7--bank-segments)
8. [Data Lineage Diagram](#8-data-lineage-diagram)
9. [Data Quality Rules](#9-data-quality-rules)
10. [Update Frequency](#10-update-frequency)
11. [Processing Scripts Mapping](#11-processing-scripts-mapping)
12. [Notebook-to-Dataset Mapping](#12-notebook-to-dataset-mapping)
13. [Feature Engineering Log](#13-feature-engineering-log)
14. [Change Log](#14-change-log)

---

## 1. Datensatz 1 — GA4 Raw Events

**Datei:** `data/raw/ga4_ecommerce/GA4_Ecommerce.csv`  
**Quelle:** BigQuery GA4 Export (Google Analytics 4)  
**Zeilenanzahl:** ~variabel (Event-Level)  
**Format:** CSV, Komma-separiert  
**Verwendung:** H1 (Engagement-Analyse), H3 (Empfehlungssystem)

> ⚠️ **Hinweis:** `user_pseudo_id` wird von GA4 als FLOAT64 exportiert. Dies kann die String-Präzision beeinträchtigen (z. B. `1026454.427` statt der originalen ID). Für exakte Nutzeridentifikation empfiehlt sich die Verwendung von `user_id`, falls verfügbar.

> 📦 **JSON-Felder:** `event_params`, `user_properties`, `device`, `geo`, `ecommerce`, `items` sind als JSON-Strings gespeichert und müssen vor der Verarbeitung geparst werden.

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `event_date` | STRING | Nein | Datum des Events (Format: YYYYMMDD) | `20210101` |
| `event_timestamp` | INT64 | Nein | Unix-Mikrosekunden seit Epoch | `1609459200000000` |
| `event_name` | STRING | Nein | Name des GA4-Events | `page_view`, `purchase` |
| `event_params` | JSON | Ja | Key-Value-Parameter des Events | `[{"key":"page_title",...}]` |
| `event_previous_timestamp` | INT64 | Ja | Timestamp des vorherigen Events | `1609459100000000` |
| `event_value_in_usd` | FLOAT64 | Ja | Monetärer Wert des Events in USD | `19.99` |
| `event_bundle_sequence_id` | INT64 | Ja | Bündel-Sequenz-ID | `123456` |
| `event_server_timestamp_offset` | INT64 | Ja | Offset zwischen Client und Server (Mikrosek.) | `-5000` |
| `user_id` | STRING | Ja | Authentifizierte User-ID (falls angemeldet) | `user_abc123` |
| `user_pseudo_id` | FLOAT64 | Nein | Anonyme GA4-Gerätekennzeichnung ⚠️ FLOAT64-Präzision | `1026454.427` |
| `privacy_info` | JSON | Ja | DSGVO-relevante Datenschutz-Flags | `{"ads_storage":"Yes"}` |
| `user_properties` | JSON | Ja | Benutzerdefinierte User-Eigenschaften | `[{"key":"tier",...}]` |
| `user_first_touch_timestamp` | INT64 | Ja | Erster Kontakt des Users (Unix-Mikrosek.) | `1609000000000000` |
| `user_ltv` | JSON | Ja | Lifetime Value des Users | `{"revenue": 49.99}` |
| `device` | JSON | Ja | Geräte-Informationen | `{"category":"mobile",...}` |
| `geo` | JSON | Ja | Geo-Informationen | `{"country":"Germany",...}` |
| `app_info` | JSON | Ja | App-spezifische Infos (für App-Tracking) | `null` |
| `traffic_source` | JSON | Ja | Kanal und Quelle | `{"source":"google",...}` |
| `stream_id` | STRING | Ja | GA4-Stream-ID | `1234567890` |
| `platform` | STRING | Ja | Plattform | `WEB` |
| `event_dimensions` | JSON | Ja | Zusätzliche Dimensionen | `null` |
| `ecommerce` | JSON | Ja | E-Commerce-Transaktionsdaten | `{"purchase_revenue":19.99}` |
| `items` | JSON | Ja | Liste der gekauften/angesehenen Artikel | `[{"item_id":"SKU123",...}]` |

---

## 2. Datensatz 2 — GA4 User-Level

**Datei:** `data/processed/GA4_user_level.csv`  
**Quelle:** Aggregiert aus Datensatz 1 via `src/data/preprocessor.py`  
**Granularität:** 1 Zeile pro User  
**Verwendung:** H1 (Engagement-Segmentierung), H2 (RFM-Basis)

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `user_pseudo_id` | FLOAT64 | Nein | Anonyme GA4-Gerätekennzeichnung ⚠️ | `1026454.427` |
| `total_events` | INT64 | Nein | Gesamtanzahl aller Events | `7` |
| `page_views` | INT64 | Nein | Anzahl `page_view`-Events | `2` |
| `scrolls` | INT64 | Nein | Anzahl `scroll`-Events | `1` |
| `engagements` | INT64 | Nein | Anzahl Engagement-Events (engaged_session_start) | `1` |
| `sessions` | INT64 | Nein | Anzahl Sessions | `1` |
| `device` | STRING | Ja | Gerätetyp | `mobile` |
| `country` | STRING | Ja | Land des Users | `United States` |
| `active_days` | INT64 | Nein | Anzahl aktiver Tage | `1` |
| `engagement_rate` | FLOAT64 | Nein | Anteil Engagements an Gesamt-Events (`engagements / total_events`) | `0.1429` |
| `scroll_rate` | FLOAT64 | Nein | Anteil Scroll-Events an Gesamt-Events (`scrolls / total_events`) | `0.5` |
| `session_rate` | FLOAT64 | Nein | Anteil Sessions an Gesamt-Events (`sessions / total_events`) | `0.1429` |

---

## 3. Datensatz 3 — GA4 Segmentation

**Datei:** `data/processed/ga4_segments.csv`  
**Quelle:** Aggregiert aus Datensatz 1; Segmentierung via `src/analysis/segmentation.py`  
**Granularität:** 1 Zeile pro User  
**Verwendung:** H2 (Cluster-Validierung), H3 (Personalisierung)

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `user_pseudo_id` | FLOAT64 | Nein | Anonyme GA4-Gerätekennzeichnung ⚠️ | `1000300.322` |
| `n_sessions` | INT64 | Nein | Anzahl Sessions | `1` |
| `n_events` | INT64 | Nein | Gesamtanzahl Events | `1` |
| `n_view_item` | INT64 | Nein | Anzahl `view_item`-Events | `0` |
| `n_purchase` | INT64 | Nein | Anzahl Käufe | `0` |
| `total_revenue` | FLOAT64 | Nein | Gesamtumsatz in USD | `0.0` |
| `device_category` | STRING | Ja | Gerätekategorie | `desktop` |
| `country` | STRING | Ja | Land | `France` |
| `traffic_source` | STRING | Ja | Traffic-Quelle | `<Other>` |
| `first_seen` | DATE | Nein | Erster Event-Tag | `2020-11-04` |
| `last_seen` | DATE | Nein | Letzter Event-Tag | `2020-11-04` |
| `recency_days` | INT64 | Nein | Tage seit letztem Event (RFM-Recency) | `58` |
| `tenure_days` | INT64 | Nein | Tage zwischen erstem und letztem Event | `0` |
| `has_purchased` | INT8 | Nein | Binär: Hat mindestens einmal gekauft (0/1) | `0` |
| `tier1` | INT64 | Nein | Tier-Klassifikation (numerisch) | `1` |
| `tier1_label` | STRING | Nein | Tier-Bezeichnung (aus Regel-basierter Segmentierung) | `Passive` |
| `cluster` | STRING | Ja | Cluster-Bezeichnung (Rule-based, identisch mit cluster_label) | `Passive` |
| `cluster_label` | STRING | Nein | KMeans-Cluster-Label (Output von `RFMSegmentation.fit_predict()`) | `Passive` |
| `cluster_db` | INT64 | Nein | DBSCAN-Cluster-ID (0 = kein Cluster, -1 = Rauschen) | `0` |

### 3.1 RFM Scores (Feature-engineered)

Die folgenden Spalten entstehen durch `GA4RFMPreprocessor.compute_rfm()` aus `src/data/preprocessor.py` und werden dem Datensatz vor der Segmentierung hinzugefügt:

| Spalte | Typ | Nullable | Beschreibung | Wertebereich |
|--------|-----|----------|--------------|-------------|
| `r_score` | INT8 | Nein | Recency-Quintil-Score (5 = zuletzt aktiv) | 1–5 |
| `f_score` | INT8 | Nein | Frequency-Quintil-Score (5 = häufigste Käufe) | 1–5 |
| `m_score` | INT8 | Nein | Monetary-Quintil-Score (5 = höchster Umsatz) | 1–5 |
| `rfm_score` | INT8 | Nein | Summe r_score + f_score + m_score | 3–15 |

> **Recency-Inversion:** Niedrigerer `recency_days`-Wert = besser → Score wird invertiert: Quintil 1 (niedrigste Tage) erhält Score 5.

---

## 4. Datensatz 4 — GA4 Recommender Dataset

**Datei:** `data/processed/ga4_recommender_dataset.csv`  
**Quelle:** Abgeleitet aus Datensatz 1; Gewichtung via `notebooks/05_recommendation_logic.ipynb`  
**Granularität:** 1 Zeile pro (User, Item)-Kombination  
**Verwendung:** H3 (Empfehlungssystem)

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `user_pseudo_id` | FLOAT64 | Nein | Anonyme GA4-Gerätekennzeichnung ⚠️ | `56513851.433` |
| `item_id` | STRING | Nein | Produkt-ID (aus GA4 `items`-Array) | `9195712` |
| `interaction` | INT8 | Nein | Gewichteter Interaktions-Score | `4` |
| `event_timestamp` | DATETIME | Nein | Zeitstempel des Events | `2021-01-31 02:14:23` |

**Interaktions-Gewichtung:**

| Event-Typ | Gewicht |
|-----------|---------|
| `view_item` | 1 |
| `add_to_cart` | 2 |
| `purchase` | 4 |

---

## 5. Datensatz 5 — Bank Marketing (bank-full.csv)

**Datei:** `data/raw/bank_marketing/bank-full.csv`  
**Quelle:** UCI Machine Learning Repository (ältere Version)  
**Zeilenanzahl:** 45.211  
**Format:** CSV, Komma-separiert  
**Verwendung:** H1 (Basis-EDA), Vergleich mit Datensatz 6

> ⚠️ **Data Leakage:** `duration` (Anrufdauer in Sekunden) ist eine Post-Contact-Variable. Sie ist erst nach dem Anruf bekannt und darf **nicht** für realistische Modelle verwendet werden. Wird in `BankMarketingPreprocessor` via `LEAKAGE_COLS` entfernt.

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `age` | INT64 | Nein | Alter des Kunden | `58` |
| `job` | STRING | Nein | Beruf | `management` |
| `marital` | STRING | Nein | Familienstand | `married` |
| `education` | STRING | Nein | Bildungsniveau | `tertiary` |
| `default` | STRING | Nein | Hat Kreditausfall? (`yes`/`no`) | `no` |
| `balance` | INT64 | Nein | Durchschnittlicher Jahreskontostand (EUR) | `2143` |
| `housing` | STRING | Nein | Hat Immobilienkredit? (`yes`/`no`) | `yes` |
| `loan` | STRING | Nein | Hat Privatkredit? (`yes`/`no`) | `no` |
| `contact` | STRING | Ja | Kontaktart | `unknown` |
| `day` | INT64 | Nein | Tag des letzten Kontakts (1–31) | `5` |
| `month` | STRING | Nein | Monat des letzten Kontakts | `may` |
| `duration` | INT64 | Nein | ⚠️ Anrufdauer in Sekunden — **Data Leakage!** | `261` |
| `campaign` | INT64 | Nein | Anzahl Kontakte in dieser Kampagne | `1` |
| `pdays` | INT64 | Ja | Tage seit letztem Kontakt (**-1 = nie kontaktiert**) | `-1` |
| `previous` | INT64 | Nein | Anzahl früherer Kontakte | `0` |
| `poutcome` | STRING | Ja | Ergebnis der letzten Kampagne | `unknown` |
| `Target` | STRING | Nein | Zielvariable: Termineinlage abgeschlossen? | `no` |

---

## 6. Datensatz 6 — Bank Marketing Additional (bank-additional-full.csv)

**Datei:** `data/raw/bank_marketing/bank-additional-full.csv`  
**Quelle:** UCI Machine Learning Repository (neuere, erweiterte Version)  
**Zeilenanzahl:** 41.188  
**Format:** CSV, Semikolon-separiert  
**Verwendung:** H1 (Haupt-Datenbasis), H2 (Makroökonomische Features)

> 📌 **Warum zwei Bank-Datensätze?**  
> `bank-full.csv` ist die ältere Version (2008–2010) mit weniger Features.  
> `bank-additional-full.csv` ist die neuere, vollständige Version mit zusätzlichen Makroökonomischen Indikatoren. Letztere wird für alle Analysen bevorzugt (`loader.load_bank_marketing()` lädt standardmäßig diese Datei).

### Vergleichstabelle: Datensatz 5 vs. Datensatz 6

| Merkmal | Datensatz 5 (bank-full) | Datensatz 6 (bank-additional-full) |
|---------|------------------------|-------------------------------------|
| Trennzeichen | `,` | `;` |
| Zeilen | 45.211 | 41.188 |
| Spalten | 17 | 21 |
| `pdays` kodierung | **-1** = nie kontaktiert | **999** = nie kontaktiert |
| `day` | Numerisch (1–31) | Fehlend (ersetzt durch `day_of_week`) |
| `balance` | Vorhanden | **Fehlend** |
| Makro-Features | **Fehlend** | `emp.var.rate`, `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed` |
| Zielvariable | `Target` | `y` |

> ⚠️ **`pdays`-Kodierung:** In Datensatz 5 bedeutet `-1` „nie kontaktiert". In Datensatz 6 bedeutet `999` dasselbe. `BankMarketingPreprocessor.fit_transform()` normalisiert den 999-Wert: `999 → NaN` + neue Spalte `was_contacted_before`.

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `age` | INT64 | Nein | Alter des Kunden | `56` |
| `job` | STRING | Nein | Beruf | `housemaid` |
| `marital` | STRING | Nein | Familienstand | `married` |
| `education` | STRING | Nein | Bildungsniveau | `basic.4y` |
| `default` | STRING | Nein | Hat Kreditausfall? | `no` |
| `housing` | STRING | Nein | Hat Immobilienkredit? | `no` |
| `loan` | STRING | Nein | Hat Privatkredit? | `no` |
| `contact` | STRING | Nein | Kontaktart | `telephone` |
| `month` | STRING | Nein | Monat des letzten Kontakts | `may` |
| `day_of_week` | STRING | Nein | Wochentag des letzten Kontakts | `mon` |
| `duration` | INT64 | Nein | ⚠️ Anrufdauer in Sekunden — **Data Leakage!** | `261` |
| `campaign` | INT64 | Nein | Anzahl Kontakte in dieser Kampagne | `1` |
| `pdays` | INT64 | Ja | Tage seit letztem Kontakt (**999 = nie kontaktiert**) | `999` |
| `previous` | INT64 | Nein | Anzahl früherer Kontakte | `0` |
| `poutcome` | STRING | Nein | Ergebnis der letzten Kampagne | `nonexistent` |
| `emp.var.rate` | FLOAT64 | Nein | Beschäftigungs-Variationsrate (quartalsweise) | `1.1` |
| `cons.price.idx` | FLOAT64 | Nein | Verbraucherpreisindex (monatlich) | `93.994` |
| `cons.conf.idx` | FLOAT64 | Nein | Konsumklimaindex (monatlich) | `-36.4` |
| `euribor3m` | FLOAT64 | Nein | EURIBOR 3-Monats-Zinssatz (täglich) | `4.857` |
| `nr.employed` | FLOAT64 | Nein | Anzahl Beschäftigter (quartalsweise, in Tausend) | `5191.0` |
| `y` | STRING | Nein | Zielvariable: Termineinlage? (`yes`/`no`) | `no` |

---

## 7. Datensatz 7 — Bank Segments

**Datei:** `data/processed/bank_segments.csv`  
**Quelle:** Verarbeitet aus Datensatz 5 via `notebooks/02_eda_bank_marketing.ipynb`  
**Granularität:** 1 Zeile pro Kunden-Kontakt  
**Verwendung:** H1 (Segmentvergleich), H2 (Cluster-Validierung)

> **Hinweis:** Datensatz 5 (`bank-full.csv`) ist die Basis. `pdays = -1` kennzeichnet Erstkontakte. Makroökonomische Features fehlen (aus Datensatz 6 ergänzbar).

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `age` | INT64 | Nein | Alter des Kunden | `58` |
| `job` | STRING | Nein | Beruf | `management` |
| `marital` | STRING | Nein | Familienstand | `married` |
| `education` | STRING | Nein | Bildungsniveau | `tertiary` |
| `balance` | INT64 | Nein | Durchschnittlicher Jahreskontostand | `2143` |
| `housing` | STRING | Nein | Hat Immobilienkredit? | `yes` |
| `loan` | STRING | Nein | Hat Privatkredit? | `no` |
| `contact` | STRING | Ja | Kontaktart | `unknown` |
| `month` | STRING | Nein | Kampagnenmonat | `may` |
| `duration` | INT64 | Nein | ⚠️ Anrufdauer — **Data Leakage!** | `261` |
| `campaign` | INT64 | Nein | Anzahl Kontakte dieser Kampagne | `1` |
| `pdays` | INT64 | Ja | Tage seit letztem Kontakt (-1 = nie) | `-1` |
| `previous` | INT64 | Nein | Frühere Kontakte | `0` |
| `poutcome` | STRING | Ja | Ergebnis der letzten Kampagne | `unknown` |
| `y` | STRING | Nein | Zielvariable: Termineinlage? | `no` |
| `y_binary` | INT8 | Nein | Binärkodierung von `y` (`1`=yes, `0`=no) | `0` |
| `cluster` | INT64 | Nein | Numerischer Cluster-Index (KMeans) | `1` |
| `cluster_label` | STRING | Nein | Lesbare Cluster-Bezeichnung | `Mass Market` |

### 7.1 Bank User-Level (Aggregiert)

**Datei:** `data/processed/bank_user_level.csv`  
**Granularität:** 1 Zeile pro Kontakttyp (aggregierte Metriken)

| Spalte | Typ | Nullable | Beschreibung | Beispiel |
|--------|-----|----------|--------------|---------|
| `contact` | STRING | Nein | Kontaktart (Aggregierungsschlüssel) | `cellular` |
| `total_contacts` | INT64 | Nein | Gesamtanzahl Kontakte | `24005` |
| `avg_duration` | FLOAT64 | Nein | Durchschnittliche Anrufdauer (Sek.) | `250.18` |
| `max_duration` | INT64 | Nein | Maximale Anrufdauer | `1271` |
| `min_duration` | INT64 | Nein | Minimale Anrufdauer | `11` |
| `successful_contacts` | INT64 | Nein | Anzahl erfolgreicher Termineinlagen | `2942` |
| `has_success` | INT8 | Nein | Binär: Hat mindestens eine Einlage erzielt | `1` |
| `last_month` | STRING | Nein | Häufigster Kampagnenmonat | `aug` |
| `last_day` | STRING | Nein | Häufigster Wochentag | `tue` |
| `age` | FLOAT64 | Nein | Durchschnittliches Kundenalter | `39.83` |
| `job` | STRING | Nein | Häufigster Beruf | `admin.` |
| `marital` | STRING | Nein | Häufigster Familienstand | `married` |
| `education` | STRING | Nein | Häufigstes Bildungsniveau | `university.degree` |
| `default` | STRING | Nein | Häufigste Kreditausfall-Angabe | `no` |
| `housing` | STRING | Nein | Häufigste Immobilienkreditangabe | `yes` |
| `loan` | STRING | Nein | Häufigste Privatkreditangabe | `no` |
| `emp_var_rate` | FLOAT64 | Nein | Mittlere Beschäftigungs-Variationsrate | `-0.341` |
| `cons_price_idx` | FLOAT64 | Nein | Mittlerer Verbraucherpreisindex | `93.289` |
| `cons_conf_idx` | FLOAT64 | Nein | Mittlerer Konsumklimaindex | `-41.366` |
| `euribor3m` | FLOAT64 | Nein | Mittlerer EURIBOR 3M | `3.193` |
| `nr_employed` | FLOAT64 | Nein | Mittlere Beschäftigtenzahl | `5159.29` |

---

## 8. Data Lineage Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         RAW DATA                                │
│                                                                 │
│  [D1] GA4_Ecommerce.csv        [D5] bank-full.csv              │
│       (data/raw/ga4_ecommerce)      (data/raw/bank_marketing)  │
│                                [D6] bank-additional-full.csv   │
│                                     (data/raw/bank_marketing)  │
└──────────────────┬──────────────────────────┬───────────────────┘
                   │                          │
         src/data/loader.py          src/data/loader.py
         load_ga4_events()           load_bank_marketing()
                   │                          │
                   ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PREPROCESSED                               │
│                                                                 │
│  [D2] GA4_user_level.csv       [D7] bank_segments.csv          │
│       (data/processed)              (data/processed)           │
│                                     bank_user_level.csv        │
│                                                                 │
│  Pipeline: src/data/preprocessor.py                            │
│  • GA4RFMPreprocessor.compute_rfm()  → r_score, f_score,       │
│    m_score, rfm_score                                           │
│  • BankMarketingPreprocessor.fit_transform()                    │
│    → was_contacted_before, y_binary                             │
└──────────────────┬──────────────────────────┬───────────────────┘
                   │                          │
         EDA Notebooks (01, 02)     EDA Notebooks (02)
                   │                          │
                   ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FEATURE-ENGINEERED                            │
│                                                                 │
│  RFM Features: recency_days, frequency, monetary                │
│  Cluster Features: StandardScaler → KMeans Input               │
│  Recommender Features: interaction weights (1/2/4)             │
│                                                                 │
│  Pipeline: src/analysis/segmentation.py                        │
│  notebooks/03_segmentation_analysis.ipynb                      │
│  notebooks/05_recommendation_logic.ipynb                       │
└──────────────────┬──────────────────────────┬───────────────────┘
                   │                          │
                   ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SEGMENTED & CLUSTERED                        │
│                                                                 │
│  [D3] ga4_segments.csv         [D4] ga4_recommender_dataset.csv│
│       (data/processed)              (data/processed)           │
│       + cluster_label               + interaction weights      │
│       + cluster_db                                             │
│       + tier1_label                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Data Quality Rules

| Datensatz | Regel | Validierung | Aktion bei Verletzung |
|-----------|-------|-------------|----------------------|
| GA4 User-Level (D2) | `total_events` > 0 | `MIN(total_events) >= 1` | Zeile ablehnen |
| GA4 User-Level (D2) | `engagement_rate` in [0, 1] | `0 <= engagement_rate <= 1` | Warnung |
| GA4 User-Level (D2) | `scroll_rate` in [0, 1] | `0 <= scroll_rate <= 1` | Warnung |
| GA4 Segments (D3) | `recency_days` ≥ 0 | `MIN(recency_days) >= 0` | Ablehnen |
| GA4 Segments (D3) | `rfm_score` in [3, 15] | `3 <= rfm_score <= 15` | Alert bei Ausreißer |
| GA4 Segments (D3) | `r_score`, `f_score`, `m_score` in [1, 5] | Quintil-Check | Neuberechnung |
| GA4 Recommender (D4) | `interaction` in {1, 2, 4} | Set-Mitgliedschaft | Ablehnen |
| Bank Full (D5) | `age` in [18, 98] | `18 <= age <= 98` | Ablehnen |
| Bank Full (D5) | `pdays` = -1 oder ≥ 0 | Keine anderen negativen Werte | Warnung |
| Bank Additional (D6) | `pdays` = 999 oder ≥ 0 | Keine -1-Werte | Warnung |
| Bank Additional (D6) | `emp.var.rate` in [-3.5, 1.5] | Historischer Wertebereich | Alert |
| Bank Segments (D7) | `y_binary` in {0, 1} | Binär-Check | Ablehnen |
| Bank Segments (D7) | `cluster_label` nicht leer | `NOT NULL` | Warnung |

---

## 10. Update Frequency

| Datensatz | Datei | Quelle | Frequenz | Letztes Update | Nächstes Update |
|-----------|-------|--------|----------|----------------|-----------------|
| D1 — GA4 Raw | `GA4_Ecommerce.csv` | BigQuery Export | Manueller Import | 2026-04-12 | Nach Bedarf |
| D2 — GA4 User-Level | `GA4_user_level.csv` | Preprocessing | Bei D1-Update | 2026-04-12 | Bei D1-Update |
| D3 — GA4 Segments | `ga4_segments.csv` | Segmentierung | Bei D2-Update | 2026-04-12 | Bei D2-Update |
| D4 — GA4 Recommender | `ga4_recommender_dataset.csv` | Feature Eng. | Bei D1-Update | 2026-04-12 | Bei D1-Update |
| D5 — Bank Full | `bank-full.csv` | UCI Repository | Statisch | 2026-04-01 | N/A |
| D6 — Bank Additional | `bank-additional-full.csv` | UCI Repository | Statisch | 2026-04-01 | N/A |
| D7 — Bank Segments | `bank_segments.csv` | Preprocessing | Statisch | 2026-04-01 | N/A |

---

## 11. Processing Scripts Mapping

| Script / Notebook | Eingabe | Ausgabe | Beschreibung |
|-------------------|---------|---------|--------------|
| `src/data/loader.py` | Raw CSV-Dateien | DataFrame | Laden der Rohdaten ohne Transformation |
| `src/data/preprocessor.py` → `BankMarketingPreprocessor` | D5 oder D6 (Raw) | D7 (bank_segments) | pdays-Normalisierung, was_contacted_before, y_binary, duration-Entfernung |
| `src/data/preprocessor.py` → `GA4RFMPreprocessor` | D1 (Raw) | RFM-Tabelle (D3-Basis) | recency_days, frequency, monetary, r/f/m_score, rfm_score |
| `src/analysis/segmentation.py` → `RFMSegmentation` | RFM-Tabelle | D3 (ga4_segments) + cluster_label | StandardScaler + KMeans-Clustering + Silhouette-Score |
| `notebooks/01_eda_ga4_ecommerce.ipynb` | D1 | D2 (GA4_user_level) | User-Level-Aggregation, engagement/scroll/session_rate |
| `notebooks/02_eda_bank_marketing.ipynb` | D5, D6 | D7 (bank_segments) | EDA, Segmentierung, Visualisierungen |
| `notebooks/03_segmentation_analysis.ipynb` | D2, D3 | D3 (aktualisiert) | Cluster-Optimierung, Silhouette-Analyse |
| `notebooks/04_hypothesis_testing.ipynb` | D3, D7 | Statistik-Outputs | H1, H2, H3 Hypothesentests |
| `notebooks/05_recommendation_logic.ipynb` | D1 | D4 (ga4_recommender) | Interaction-Gewichtung, Recommender-Matrix |

---

## 12. Notebook-to-Dataset Mapping

| Notebook | Liest Datensatz | Schreibt Datensatz |
|----------|-----------------|--------------------|
| `01_eda_ga4_ecommerce.ipynb` | D1 | D2 |
| `02_eda_bank_marketing.ipynb` | D5, D6 | D7 |
| `03_segmentation_analysis.ipynb` | D2 → D3 | D3 (cluster_label) |
| `04_hypothesis_testing.ipynb` | D3, D7 | — (nur Analyse) |
| `05_recommendation_logic.ipynb` | D1 | D4 |
| `06_ethics_dsgvo_analysis.ipynb` | D3, D7 | — (nur Analyse) |

---

## 13. Feature Engineering Log

### 13.1 RFM Scores (GA4)

**Script:** `src/data/preprocessor.py` → `GA4RFMPreprocessor.compute_rfm()`  
**Eingabe:** Datensatz 1 (gefiltert auf `event_name='purchase'`)  
**Ausgabe:** Spalten in Datensatz 3

| Feature | Formel | Beschreibung |
|---------|--------|--------------|
| `recency_days` | `(reference_date - max(event_date)).days` | Tage seit letztem Kauf |
| `frequency` | `COUNT(event_date) per user` | Anzahl Käufe gesamt |
| `monetary` | `SUM(purchase_revenue) per user` | Gesamtumsatz |
| `r_score` | `pd.qcut(recency_days, q=5, labels=[5,4,3,2,1])` | Quintil 1–5, **invertiert** (weniger Tage = höherer Score) |
| `f_score` | `pd.qcut(frequency.rank(), q=5, labels=[1,2,3,4,5])` | Quintil 1–5 (mehr Käufe = höherer Score) |
| `m_score` | `pd.qcut(monetary.rank(), q=5, labels=[1,2,3,4,5])` | Quintil 1–5 (mehr Umsatz = höherer Score) |
| `rfm_score` | `r_score + f_score + m_score` | Gesamt-Score, Wertebereich 3–15 |

**Recency-Inversion Erklärung:**  
Da ein niedriger `recency_days`-Wert (kürzlich aktiv) gut ist, werden die Quintil-Labels invertiert:  
- Quintil 1 (niedrigste recency_days) → Label **5** (bester Score)  
- Quintil 5 (höchste recency_days) → Label **1** (schlechtester Score)

### 13.2 Engagement Rates (GA4 User-Level)

**Script:** `notebooks/01_eda_ga4_ecommerce.ipynb`  
**Ausgabe:** Spalten in Datensatz 2

| Feature | Formel | Beschreibung |
|---------|--------|--------------|
| `engagement_rate` | `engagements / total_events` | Anteil engagierter Sessions |
| `scroll_rate` | `scrolls / total_events` | Anteil Scroll-Events |
| `session_rate` | `sessions / total_events` | Anteil Sessions an Gesamt-Events |

### 13.3 Bank-spezifische Features

**Script:** `src/data/preprocessor.py` → `BankMarketingPreprocessor.fit_transform()`  
**Ausgabe:** Spalten in Datensatz 7

| Feature | Formel | Beschreibung |
|---------|--------|--------------|
| `was_contacted_before` | `(pdays != 999).astype(int)` | 1 = wurde bereits kontaktiert, 0 = Erstkontakt |
| `y_binary` | `(y == 'yes').astype(int)` | Binärkodierung der Zielvariable |
| ~~`duration`~~ | Entfernt via `LEAKAGE_COLS` | ⚠️ Data Leakage: Post-Contact-Variable |

### 13.4 Clustering Features

**Script:** `src/analysis/segmentation.py` → `RFMSegmentation.fit_predict()`  
**Eingabe:** `recency_days`, `frequency`, `monetary` aus Datensatz 3  
**Ausgabe:** `cluster_label` in Datensatz 3

| Schritt | Methode | Beschreibung |
|---------|---------|--------------|
| Skalierung | `StandardScaler().fit_transform(X)` | Z-Score-Normalisierung der RFM-Features |
| Clustering | `KMeans(n_clusters=4, n_init='auto')` | 4 Cluster (optimiert via Silhouette-Score) |
| `cluster_label` | `model.fit_predict(X_scaled)` | Integer-Label 0–3 (KMeans-Output) |
| Qualitätsmetrik | `silhouette_score(X_scaled, labels)` | Gespeichert als `RFMSegmentation.silhouette_score_` |

**Optimale k-Bestimmung:** `RFMSegmentation.find_optimal_k()` testet `k=2..7` und gibt Silhouette-Scores zurück.

### 13.5 Recommender Features

**Script:** `notebooks/05_recommendation_logic.ipynb`  
**Ausgabe:** Datensatz 4

| Feature | Gewichtung | Beschreibung |
|---------|-----------|--------------|
| `view_item` → `interaction=1` | ×1 | Schwache Präferenz |
| `add_to_cart` → `interaction=2` | ×2 | Mittlere Präferenz |
| `purchase` → `interaction=4` | ×4 | Starke Präferenz |

---

## 14. Change Log

| Datum | Version | Änderung | Autor |
|-------|---------|----------|-------|
| 2026-04-01 | 1.0 | Initiale Erstellung: Datensätze 1–6 | Person A |
| 2026-04-10 | 2.0 | Feature Engineering Log ergänzt, pdays-Hinweis | Person A |
| 2026-04-12 | 3.0 | Vollständige Überarbeitung: Data Lineage, Quality Rules, Processing Mapping, RFM Scores (D3), engagement_rate/scroll_rate (D2), Bank Segments (D7), Makrofeatures, pdays-Kodierung dokumentiert, user_pseudo_id FLOAT64 Warnung, Data Leakage Hinweis duration, Notebook-Mapping, Cross-References | Person B |

---

*Dieses Dokument ist synchron mit dem Codestand in `src/data/preprocessor.py` und `src/analysis/segmentation.py`. Bei Code-Änderungen muss das Dictionary entsprechend aktualisiert werden.*
