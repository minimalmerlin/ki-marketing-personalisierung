# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B
> **Status:** In Bearbeitung (KW 15)
> **Zweck:** Vollständige Dokumentation aller genutzten Datensätze als SSOT für das Team

---

## Inhaltsverzeichnis

1. [GA4 Rohdaten](#datensatz-1-ga4-bigquery-sample-ecommerce-rohdaten)
2. [GA4 User-Level (aggregiert)](#datensatz-2-ga4-user-level-aggregiert)
3. [GA4 Segmentierungs-Dataset](#datensatz-3-ga4-segmentierungs-dataset)
4. [GA4 Recommender-Dataset](#datensatz-4-ga4-recommender-dataset)
5. [Bank Marketing Rohdaten (bank-full)](#datensatz-5-bank-marketing-rohdaten-bank-full)
6. [Bank Marketing Rohdaten (bank-additional-full)](#datensatz-6-bank-marketing-rohdaten-bank-additional-full)
7. [Bank User-Level (aggregiert)](#datensatz-7-bank-user-level-aggregiert)
8. [Bank Segmente](#datensatz-8-bank-segmente)
9. [Externe Regulatorische Dokumente](#datensatz-9-externe-regulatorische-dokumente)
10. [Feature Engineering Log](#feature-engineering-log)

---

## Datensatz 1: GA4 BigQuery Sample Ecommerce (Rohdaten)

**Datei:** `data/raw/ga4_ecommerce/GA4_Ecommerce.csv`
**Quelle:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce`
**Lizenz:** Google Public Data License
**Zeilen:** 2.376 | **Spalten:** 23
**Zeitraum:** Nov 2020 – Jan 2021

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hinweis |
|------|-------------|-----|-------------|-------|---------|
| `event_date` | Datum des Events (YYYYMMDD) | INT64 | `20201227` | Nein | Format: YYYYMMDD als Ganzzahl |
| `event_timestamp` | Unix-Timestamp des Events in Mikrosekunden | INT64 | `1609083756933271` | Nein | — |
| `event_name` | Name des Events | STRING | `view_promotion`, `page_view`, `purchase` | Nein | Conversion-Funnel: session_start → view_item → add_to_cart → begin_checkout → purchase |
| `event_params` | JSON-Objekt mit event-spezifischen Parametern | STRING (JSON) | `{"key": "page_location", ...}` | Ja | Nested JSON; je nach event_name unterschiedliche Keys |
| `event_previous_timestamp` | Timestamp des vorherigen Events desselben Nutzers | FLOAT64 | `1609081234000000.0` | Ja | Null bei erstem Event |
| `event_value_in_usd` | Monetärer Wert des Events in USD | FLOAT64 | `12.99` | Ja | Nur bei Kauf-Events befüllt |
| `event_bundle_sequence_id` | Sequenz-ID für Event-Batches | INT64 | `1` | Nein | — |
| `event_server_timestamp_offset` | Zeitversatz zwischen Client und Server in Mikrosekunden | FLOAT64 | `3000000.0` | Ja | — |
| `user_id` | Optionale Login-User-ID (PII) | FLOAT64 | `null` | Ja | In diesem Sample meist leer (obfuskiert) |
| `user_pseudo_id` | Anonymisierte Client-ID (kein PII) | FLOAT64 | `1026454.427` | Nein | Ursprünglich STRING in BigQuery; beim CSV-Export zu FLOAT64 konvertiert → kann für Cross-Device kein Tracking |
| `privacy_info` | Datenschutz-Flags des Nutzers | STRING (JSON) | `{"analytics_storage": "Yes", ...}` | Ja | Nested JSON |
| `user_properties` | Nutzerspezifische Properties | STRING (JSON) | `{"first_open_time": {...}}` | Ja | Nested JSON; selten befüllt |
| `user_first_touch_timestamp` | Timestamp des ersten Kontakts mit der App | INT64 | `1609000000000000` | Nein | Mikrosekunden |
| `user_ltv` | Lifetime Value des Nutzers | STRING (JSON) | `{"revenue": 0.0, "currency": "USD"}` | Ja | Nested JSON |
| `device` | Geräteinformationen | STRING (JSON) | `{"category": "mobile", "operating_system": "Web", ...}` | Nein | Nested JSON — enthält: category, mobile_brand_name, operating_system, browser |
| `geo` | Geografische Informationen | STRING (JSON) | `{"country": "United States", "city": "Houston", ...}` | Nein | Nested JSON — enthält: continent, country, region, city |
| `app_info` | App-Metadaten | STRING (JSON) | `null` | Ja | In Web-Events meist leer |
| `traffic_source` | Herkunft des Traffics | STRING (JSON) | `{"medium": "(none)", "source": "(direct)", ...}` | Nein | Nested JSON — enthält: medium, name, source |
| `stream_id` | GA4 Data Stream ID | INT64 | `7461943820` | Nein | Identifiziert den GA4-Property-Stream |
| `platform` | Plattform des Events | STRING | `WEB` | Nein | Werte: `WEB`, `APP` |
| `event_dimensions` | Weitere Event-Dimensionen | STRING (JSON) | `null` | Ja | Selten befüllt |
| `ecommerce` | E-Commerce-Daten des Events | STRING (JSON) | `{"purchase_revenue": 12.99, ...}` | Ja | Nur bei Kauf-Events; enthält purchase_revenue, transaction_id |
| `items` | Liste der betroffenen Produkte | STRING (JSON) | `[{"item_id": "9195712", ...}]` | Ja | Array of items; enthält item_id, item_name, price, quantity |

### Besonderheiten / bekannte Probleme

- `user_pseudo_id` wurde beim CSV-Export zu FLOAT64 konvertiert → Empfehlung: als STRING behandeln
- Nested JSON-Felder (`event_params`, `device`, `geo`, etc.) müssen vor Analyse geparst werden
- Keine demografischen Daten enthalten (GA4-typisch)
- Obfuskierte Daten — kein reales Cross-Device-Tracking möglich

---

## Datensatz 2: GA4 User-Level (aggregiert)

**Datei:** `data/processed/GA4_user_level.csv`
**Erstellt durch:** `data/processed/GA4_Ecommer_cleaner.py`
**Zeilen:** 2.546 | **Spalten:** 12
**Granularität:** Ein Eintrag pro `user_pseudo_id`

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|-------------|-------|-----------|
| `user_pseudo_id` | Anonymisierte User-ID | FLOAT64 | `1026454.427` | Nein | — |
| `total_events` | Gesamtanzahl aller Events des Nutzers | INT64 | `7` | Nein | H2 — Aktivitätsniveau |
| `page_views` | Anzahl der `page_view`-Events | INT64 | `2` | Nein | H2 — Content-Interesse |
| `scrolls` | Anzahl der `scroll`-Events | INT64 | `1` | Nein | H2 — Engagement-Tiefe |
| `engagements` | Anzahl der `user_engagement`-Events | INT64 | `1` | Nein | H2 — Aktives Engagement |
| `sessions` | Anzahl der `session_start`-Events | INT64 | `1` | Nein | H2 — Besuchshäufigkeit |
| `device` | Hauptgerät des Nutzers | STRING | `mobile` | Ja | H2 — Plattformverhalten |
| `country` | Hauptland des Nutzers | STRING | `United States` | Ja | H2 — Geografische Segmentierung |
| `active_days` | Anzahl aktiver Tage | INT64 | `1` | Nein | H2 — Loyalität / Wiederkehr |
| `engagement_rate` | Anteil Engagement-Events an total_events | FLOAT64 | `0.143` | Nein | H2 — Qualität der Interaktion |
| `scroll_rate` | Anteil Scroll-Events an total_events | FLOAT64 | `0.5` | Nein | H2 — Content-Konsum |
| `session_rate` | Anteil Session-Events an total_events | FLOAT64 | `0.143` | Nein | H2 — Besuchsfrequenz |

---

## Datensatz 3: GA4 Segmentierungs-Dataset

**Datei:** `data/processed/ga4_segments.csv`
**Erstellt durch:** `notebooks/03_segmentation_analysis.ipynb`
**Zeilen:** 67.819 | **Spalten:** 19
**Granularität:** Ein Eintrag pro User (mit Segment-Labels)

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hinweis |
|------|-------------|-----|-------------|-------|---------|
| `user_pseudo_id` | Anonymisierte User-ID | FLOAT64 | `1000300.3223` | Nein | — |
| `n_sessions` | Anzahl Sessions | INT64 | `1` | Nein | — |
| `n_events` | Gesamtanzahl Events | INT64 | `1` | Nein | — |
| `n_view_item` | Anzahl `view_item`-Events | INT64 | `0` | Nein | Produkt-Interesse |
| `n_purchase` | Anzahl Käufe | INT64 | `0` | Nein | Conversion-Indikator |
| `total_revenue` | Gesamtumsatz des Nutzers in USD | FLOAT64 | `0.0` | Nein | — |
| `device_category` | Gerätetyp | STRING | `desktop` | Ja | `mobile`, `desktop`, `tablet` |
| `country` | Land des Nutzers | STRING | `France` | Ja | — |
| `traffic_source` | Traffic-Herkunft | STRING | `<Other>` | Ja | Organisch, Paid, Direct, etc. |
| `first_seen` | Datum des ersten Events | STRING (DATE) | `2020-11-04` | Nein | Format: YYYY-MM-DD |
| `last_seen` | Datum des letzten Events | STRING (DATE) | `2020-11-04` | Nein | Format: YYYY-MM-DD |
| `recency_days` | Tage seit letztem Event (Recency für RFM) | INT64 | `58` | Nein | Niedrigerer Wert = aktiver |
| `tenure_days` | Tage zwischen first_seen und last_seen | INT64 | `0` | Nein | Kunde seit X Tagen aktiv |
| `has_purchased` | Hat Nutzer mindestens einmal gekauft? | INT64 (Bool) | `0` | Nein | `0` = nein, `1` = ja |
| `tier1` | Erster Segmentierungs-Tier (numerisch) | INT64 | `1` | Nein | `1` = Passive, `2` = Engaged |
| `tier1_label` | Bezeichnung des Tier-1-Segments | STRING | `Passive` | Nein | Werte: `Passive`, `Engaged` |
| `cluster` | KMeans-Cluster (Bezeichnung) | STRING | `Passive` | Nein | Werte: `Passive`, `Loyal Buyers`, `Champions` |
| `cluster_label` | Lesbarer Cluster-Name | STRING | `Passive` | Nein | Identisch mit `cluster` |
| `cluster_db` | DBSCAN-Cluster-ID | INT64 | `0` | Nein | `-1` = Ausreißer |

---

## Datensatz 4: GA4 Recommender-Dataset

**Datei:** `data/processed/ga4_recommender_dataset.csv`
**Erstellt durch:** `notebooks/05_recommendation_logic.ipynb`
**Zeilen:** 1.758 | **Spalten:** 4
**Granularität:** Eine Zeile pro User-Item-Interaktion

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hinweis |
|------|-------------|-----|-------------|-------|---------|
| `user_pseudo_id` | Anonymisierte User-ID | FLOAT64 | `56513851.43` | Nein | — |
| `item_id` | Produkt-ID aus GA4 `items`-Feld | INT64 | `9195712` | Nein | Numerisch kodiert aus ursprünglichem STRING |
| `interaction` | Interaktionsstärke (implizites Feedback) | INT64 | `4` | Nein | Gewichteter Score: z. B. view_item=1, add_to_cart=2, purchase=4 |
| `event_timestamp` | Zeitstempel der Interaktion | STRING (DATETIME) | `2021-01-31 02:14:23` | Nein | Format: YYYY-MM-DD HH:MM:SS |

---

## Datensatz 5: Bank Marketing Rohdaten (bank-full)

**Datei:** `data/raw/bank_marketing/bank-full.csv`
**Quelle:** UCI Machine Learning Repository — Bank Marketing Dataset (ältere Version)
**Lizenz:** CC BY 4.0
**Zeilen:** 45.211 | **Spalten:** 17
**Zielvariable:** `Target` (Termineinlage abgeschlossen?)

| Feld | Beschreibung | Typ | Beispielwert | Wertebereich | Hypothese |
|------|-------------|-----|-------------|--------------|-----------|
| `age` | Alter des Kunden in Jahren | INT64 | `56` | 18–95 | H1, H2 |
| `job` | Berufsgruppe | STRING | `management` | admin., blue-collar, entrepreneur, housemaid, management, retired, self-employed, services, student, technician, unemployed, unknown | H1, H2 |
| `marital` | Familienstand | STRING | `married` | divorced, married, single | H2 |
| `education` | Bildungsabschluss | STRING | `tertiary` | primary, secondary, tertiary, unknown | H2 |
| `default` | Kreditausfall in der Vergangenheit | STRING | `no` | no, yes | H1 |
| `balance` | Jahressaldo auf dem Konto in Euro | INT64 | `2143` | Negativ möglich | H1, H2 |
| `housing` | Hypothekarkredit vorhanden? | STRING | `yes` | no, yes | H1 |
| `loan` | Persönlicher Kredit vorhanden? | STRING | `no` | no, yes | H1 |
| `contact` | Art der Kontaktaufnahme | STRING | `unknown` | cellular, telephone, unknown | H1 |
| `day` | Tag des letzten Kontakts im Monat | INT64 | `5` | 1–31 | — |
| `month` | Monat des letzten Kontakts | STRING | `may` | jan–dec | H1 |
| `duration` | Dauer des letzten Anrufs in Sekunden | INT64 | `261` | ≥ 0 | ⚠️ Leakage — erst nach Kontakt bekannt; für prädiktive Modelle ausschließen |
| `campaign` | Anzahl der Kontakte in dieser Kampagne | INT64 | `1` | ≥ 1 | H1 |
| `pdays` | Tage seit letztem Kontakt einer vorherigen Kampagne | INT64 | `-1` | -1 = nie kontaktiert | H1 |
| `previous` | Anzahl Kontakte vor dieser Kampagne | INT64 | `0` | ≥ 0 | H1 |
| `poutcome` | Ergebnis der vorherigen Kampagne | STRING | `unknown` | failure, other, success, unknown | H1 |
| `Target` | Zielvariable: Termineinlage abgeschlossen? | STRING | `no` | no, yes | H1 |

---

## Datensatz 6: Bank Marketing Rohdaten (bank-additional-full)

**Datei:** `data/raw/bank_marketing/bank-additional-full.csv`
**Quelle:** UCI Machine Learning Repository — Bank Marketing Dataset (neuere Version mit Makrovariablen)
**Lizenz:** CC BY 4.0
**Trennzeichen:** Semikolon (`;`)
**Zeilen:** 41.188 | **Spalten:** 21
**Zielvariable:** `y` (Termineinlage abgeschlossen?)

| Feld | Beschreibung | Typ | Beispielwert | Wertebereich | Hypothese |
|------|-------------|-----|-------------|--------------|-----------|
| `age` | Alter des Kunden in Jahren | INT64 | `56` | 18–98 | H1, H2 |
| `job` | Berufsgruppe | STRING | `housemaid` | admin., blue-collar, entrepreneur, housemaid, management, retired, self-employed, services, student, technician, unemployed, unknown | H1, H2 |
| `marital` | Familienstand | STRING | `married` | divorced, married, single, unknown | H2 |
| `education` | Bildungsabschluss | STRING | `basic.4y` | basic.4y, basic.6y, basic.9y, high.school, illiterate, professional.course, university.degree, unknown | H2 |
| `default` | Kreditausfall in der Vergangenheit | STRING | `no` | no, unknown, yes | H1 |
| `housing` | Hypothekarkredit vorhanden? | STRING | `no` | no, unknown, yes | H1 |
| `loan` | Persönlicher Kredit vorhanden? | STRING | `no` | no, unknown, yes | H1 |
| `contact` | Art der Kontaktaufnahme | STRING | `telephone` | cellular, telephone | H1 |
| `month` | Monat des letzten Kontakts | STRING | `may` | jan–dec | H1 |
| `day_of_week` | Wochentag des letzten Kontakts | STRING | `mon` | mon, tue, wed, thu, fri | H1 |
| `duration` | Dauer des letzten Anrufs in Sekunden | INT64 | `261` | ≥ 0 | ⚠️ Leakage — für realistische Modelle ausschließen (siehe `LEAKAGE_COLS` in `preprocessor.py`) |
| `campaign` | Anzahl der Kontakte in dieser Kampagne | INT64 | `1` | ≥ 1 | H1 |
| `pdays` | Tage seit letztem Kontakt einer vorherigen Kampagne | INT64 | `999` | 999 = nie kontaktiert | H1 — Im Preprocessing: 999 → NaN + `was_contacted_before`-Flag |
| `previous` | Anzahl Kontakte vor dieser Kampagne | INT64 | `0` | ≥ 0 | H1 |
| `poutcome` | Ergebnis der vorherigen Kampagne | STRING | `nonexistent` | failure, nonexistent, success | H1 |
| `emp.var.rate` | Beschäftigungsveränderungsrate (Quartal) | FLOAT64 | `1.1` | — | Makroökonomisch |
| `cons.price.idx` | Konsumgüterpreisindex (monatlich) | FLOAT64 | `93.994` | — | Makroökonomisch |
| `cons.conf.idx` | Verbraucherstimmungsindex (monatlich) | FLOAT64 | `-36.4` | — | Makroökonomisch |
| `euribor3m` | Euribor 3-Monats-Zinssatz | FLOAT64 | `4.857` | — | Makroökonomisch |
| `nr.employed` | Anzahl Beschäftigter (Quartal, in Tausend) | FLOAT64 | `5191.0` | — | Makroökonomisch |
| `y` | Zielvariable: Termineinlage abgeschlossen? | STRING | `no` | no, yes | H1 |

---

## Datensatz 7: Bank User-Level (aggregiert)

**Datei:** `data/processed/bank_user_level.csv`
**Erstellt durch:** `data/processed/bank_marketing_data_cleaner.py`
**Zeilen:** 2 (aggregiert nach Kontaktkanal) | **Spalten:** 21
**Granularität:** Ein Eintrag pro `contact`-Typ

| Feld | Beschreibung | Typ | Beispielwert | Hinweis |
|------|-------------|-----|-------------|---------|
| `contact` | Kontaktkanal (Schlüssel) | STRING | `cellular` | Gruppierspalte |
| `total_contacts` | Gesamtzahl Kontakte dieses Typs | INT64 | `24005` | — |
| `avg_duration` | Durchschnittliche Anrufdauer in Sekunden | FLOAT64 | `250.18` | — |
| `max_duration` | Maximale Anrufdauer in Sekunden | INT64 | `1271` | — |
| `min_duration` | Minimale Anrufdauer in Sekunden | INT64 | `11` | — |
| `successful_contacts` | Anzahl Kontakte mit `y = yes` | INT64 | `2942` | — |
| `has_success` | Hat dieser Kontaktkanal Erfolge? | INT64 (Bool) | `1` | `0` = nein, `1` = ja |
| `last_month` | Häufigster Monat für diesen Kanal | STRING | `aug` | — |
| `last_day` | Häufigster Wochentag für diesen Kanal | STRING | `tue` | — |
| `age` | Durchschnittsalter der kontaktierten Kunden | FLOAT64 | `39.83` | — |
| `job` | Häufigste Berufsgruppe | STRING | `admin.` | — |
| `marital` | Häufigster Familienstand | STRING | `married` | — |
| `education` | Häufigster Bildungsabschluss | STRING | `university.degree` | — |
| `default` | Häufigster Kreditausfall-Status | STRING | `no` | — |
| `housing` | Häufigster Hypothekenstatus | STRING | `yes` | — |
| `loan` | Häufigster Kreditstatus | STRING | `no` | — |
| `emp_var_rate` | Durchschnittliche Beschäftigungsveränderungsrate | FLOAT64 | `-0.341` | — |
| `cons_price_idx` | Durchschnittlicher Konsumgüterpreisindex | FLOAT64 | `93.289` | — |
| `cons_conf_idx` | Durchschnittlicher Verbraucherstimmungsindex | FLOAT64 | `-41.366` | — |
| `euribor3m` | Durchschnittlicher Euribor 3-Monats-Zinssatz | FLOAT64 | `3.193` | — |
| `nr_employed` | Durchschnittliche Anzahl Beschäftigter | FLOAT64 | `5159.29` | — |

---

## Datensatz 8: Bank Segmente

**Datei:** `data/processed/bank_segments.csv`
**Erstellt durch:** `notebooks/03_segmentation_analysis.ipynb`
**Basis:** `data/raw/bank_marketing/bank-full.csv`
**Zeilen:** 45.211 | **Spalten:** 18

| Feld | Beschreibung | Typ | Beispielwert | Hinweis |
|------|-------------|-----|-------------|---------|
| `age` | Alter des Kunden | INT64 | `58` | — |
| `job` | Berufsgruppe | STRING | `management` | Kategorisch |
| `marital` | Familienstand | STRING | `married` | Kategorisch |
| `education` | Bildungsabschluss | STRING | `tertiary` | Kategorisch |
| `balance` | Jahressaldo in Euro | INT64 | `2143` | Aus bank-full (nicht in bank-additional-full) |
| `housing` | Hypothekarkredit | STRING | `yes` | Kategorisch |
| `loan` | Persönlicher Kredit | STRING | `no` | Kategorisch |
| `contact` | Kontaktkanal | STRING | `unknown` | Kategorisch |
| `month` | Monat des letzten Kontakts | STRING | `may` | Kategorisch |
| `duration` | Anrufdauer in Sekunden | INT64 | `261` | ⚠️ Leakage — vor Verwendung in Modellen ausschließen |
| `campaign` | Anzahl Kontakte dieser Kampagne | INT64 | `1` | — |
| `pdays` | Tage seit letztem Kontakt (-1 = nie) | INT64 | `-1` | Kodierung: -1 = nie kontaktiert (bank-full Konvention) |
| `previous` | Anzahl Kontakte vor dieser Kampagne | INT64 | `0` | — |
| `poutcome` | Ergebnis der Vorkampagne | STRING | `unknown` | Kategorisch |
| `y` | Zielvariable: Termineinlage? | STRING | `no` | no, yes |
| `y_binary` | Binär kodierte Zielvariable | INT64 | `0` | `0` = no, `1` = yes |
| `cluster` | KMeans-Cluster-ID | INT64 | `1` | Numerisch |
| `cluster_label` | Lesbarer Cluster-Name | STRING | `Mass Market` | Werte: `Mass Market`, `Experienced` |

---

## Datensatz 9: Externe Regulatorische Dokumente

### 9a. EDPB Profiling Guidelines (WP 251 rev.01)

| Feld | Inhalt |
|------|--------|
| **Dokument-Typ** | Regulatorisches Leitlinienpapier |
| **Herausgeber** | European Data Protection Board (EDPB) |
| **Datei** | `data/external/edpb_guidelines_profiling_wp251.pdf` |
| **Relevanz** | Definition Profiling, Art. 22 DSGVO, Rechtsgrundlagen |
| **Kapitel für H3** | Kap. 3 (Definition), Kap. 5 (Rechtsgrundlagen), Kap. 7 (Spezifische Situationen) |

### 9b. ICO Guidance on Profiling

| Feld | Inhalt |
|------|--------|
| **Dokument-Typ** | Regulatorisches Leitlinienpapier |
| **Herausgeber** | Information Commissioner's Office (UK) |
| **Datei** | `data/external/ico_guidance_profiling.pdf` |
| **Relevanz** | UK GDPR-Auslegung, Profiling-Risiken, DPIA-Anforderungen |
| **Kapitel für H3** | Abschnitt "What is profiling?", "When can we profile?" |

---

## Feature Engineering Log

> Hier dokumentieren wir alle aus den Rohdaten abgeleiteten Features.

### RFM-Features (GA4)

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `recency_days` | GA4 | Tage zwischen letztem `purchase`-Event und Referenzdatum | `src/data/preprocessor.py` |
| `frequency` | GA4 | Anzahl `purchase`-Events je `user_pseudo_id` | `src/data/preprocessor.py` |
| `monetary` | GA4 | Summe von `ecommerce.purchase_revenue` je User | `src/data/preprocessor.py` |
| `r_score` | GA4 | Quintil-Score 1–5 für Recency (5 = am aktivsten) | `src/data/preprocessor.py` |
| `f_score` | GA4 | Quintil-Score 1–5 für Frequency | `src/data/preprocessor.py` |
| `m_score` | GA4 | Quintil-Score 1–5 für Monetary | `src/data/preprocessor.py` |
| `rfm_score` | GA4 | Summe r_score + f_score + m_score (3–15) | `src/data/preprocessor.py` |

### Segmentierungs-Features (GA4)

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `engagement_rate` | GA4 | `engagements / total_events` | `data/processed/GA4_Ecommer_cleaner.py` |
| `scroll_rate` | GA4 | `scrolls / total_events` | `data/processed/GA4_Ecommer_cleaner.py` |
| `session_rate` | GA4 | `sessions / total_events` | `data/processed/GA4_Ecommer_cleaner.py` |
| `has_purchased` | GA4 | 1 wenn `n_purchase > 0` | `notebooks/03_segmentation_analysis.ipynb` |
| `tenure_days` | GA4 | `last_seen - first_seen` in Tagen | `notebooks/03_segmentation_analysis.ipynb` |
| `tier1_label` | GA4 | Regel-basiert: `Engaged` wenn Käufe oder hohe Interaktion | `notebooks/03_segmentation_analysis.ipynb` |
| `cluster_label` | GA4 | KMeans (k=3): `Passive`, `Loyal Buyers`, `Champions` | `src/analysis/segmentation.py` |
| `cluster_db` | GA4 | DBSCAN-Cluster (-1 = Ausreißer) | `src/analysis/segmentation.py` |

### Preprocessing-Features (Bank Marketing)

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `was_contacted_before` | Bank | 1 wenn `pdays ≠ 999` (bank-additional) | `src/data/preprocessor.py` |
| `y_binary` | Bank | `1` wenn `y = "yes"`, sonst `0` | `src/data/preprocessor.py` |
| `cluster_label` | Bank | KMeans (k=2): `Mass Market`, `Experienced` | `src/analysis/segmentation.py` |

### Recommender-Features (GA4)

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `interaction` | GA4 | Gewichteter Score: view_item=1, add_to_cart=2, purchase=4 | `notebooks/05_recommendation_logic.ipynb` |

---

## Change Log

| Datum | Version | Änderung | Person |
|-------|---------|----------|--------|
| 2026-04-07 | 1.0 | Erstversion mit GA4 (Basis) und Bank Marketing (numerisch kodiert) | Person B |
| 2026-04-07 | 2.0 | Vollständige Neuerstellung: alle Datensätze, alle Felder, Feature Engineering Log | Person B |