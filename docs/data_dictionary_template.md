# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B
> **Status:** TEMPLATE — Ausfüllen bis M1 (KW 13)
> **Zweck:** Vollständige Dokumentation aller genutzten Datensätze als SSOT für das Team

---

## Datensatz 1: GA4 BigQuery Sample Ecommerce
| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|--------------|-------|-----------|
| `event_date` | Datum des Events (YYYYMMDD) | INT64 | `20210131` | Nein | H2 |
| `event_timestamp` | Unix-Timestamp in Mikrosekunden | FLOAT64 | `1612070000000000` | Nein | — |
| `event_name` | Name des Events | STRING | `page_view`, `scroll`, `session_start` | Nein | H2 |
| `user_pseudo_id` | Anonymisierte User-ID (kein PII) | FLOAT64 | `1026454.427` | Nein | H2 |
| `platform` | Plattform des Besuchers | STRING | `WEB` | Nein | H1 |
| `device_category` | Gerätetyp | STRING | `mobile` | Nein | H1 |
| `country` | Land des Nutzers | STRING | `United States` | Nein | H3 |


**Quelle:** Google BigQuery Public Datasets — `bigquery-public-data.ga4_obfuscated_sample_ecommerce`
**Lizenz:** Google Public Data License
**Zeitraum:31.01.2021
**Zeilen:26489
**Besonderheiten / bekannte Probleme:**
- [ ] Obfuskierte User-IDs — kein Cross-Device-Tracking möglich
- [ ] Keine demografischen Daten enthalten

---

## Datensatz 2: UCI Bank Marketing

## 📊 Datensatz 2: Bank Marketing (UCI)

### 🧾 Feldbeschreibung (Original + Feature Engineering)

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|--------------|-------|-----------|
| `age` | Alter des Kunden | INT64 | `58` | Nein | H1, H2 |
| `job` | Berufsfeld des Kunden | STRING | `management`, `technician` | Ja (288) | H1 |
| `marital` | Familienstand | STRING | `married`, `single` | Nein | H1 |
| `education` | Bildungsniveau | STRING | `secondary`, `tertiary` | Ja (1857) | H1 |
| `default` | Kreditausfall-Historie | STRING | `yes`, `no` | Nein | H1 |
| `balance` | Durchschnittlicher Kontostand (EUR) | INT64 | `2000` | Nein | H1, H2 |
| `housing` | Wohnkredit | STRING | `yes`, `no` | Nein | H1 |
| `loan` | Privatkredit | STRING | `yes`, `no` | Nein | H1 |
| `contact` | Kontaktkanal | STRING | `cellular`, `telephone` | Ja (13020) | H1 |
| `day` | Tag des letzten Kontakts | INT64 | `15` | Nein | — |
| `month` | Monat des letzten Kontakts | STRING | `may`, `jun` | Nein | — |
| `campaign` | Anzahl Kontakte in dieser Kampagne | INT64 | `1` | Nein | H1 |
| `pdays` | Tage seit letzter Kampagne (`-1` = nie kontaktiert → `NaN`) | FLOAT64 | `NaN` | Ja (36.954) | H1 |
| `previous` | Anzahl Kontakte früherer Kampagnen | INT64 | `0` | Nein | H1 |
| `poutcome` | Ergebnis früherer Kampagne | STRING | `success`, `failure`, `unknown` | Nein (nach Cleaning) | H1 |
| `Target` | Zielvariable: Hat Kunde Termin gebucht? | INT64 | `0` oder `1` | Nein | H1 |
| `balance_cat` | Kategorisierung des Kontostands | CATEGORY | `medium`, `high` | Ja (14) | H2 |
| `was_contacted_before` | Wurde Kunde früher kontaktiert? | INT64 | `0`, `1` | Nein | H1 |

---

## 📦 **Metadaten**

- **Zeilen:** 45.211  
- **Spalten (Original):** 16  
- **Spalten (nach Cleaning):** 18  
- **Spalten (nach One‑Hot Encoding):** 57  

### **Target Imbalance**
- `0` (no): **88.30%**  
- `1` (yes): **11.69%**

---

## ⚠️ **Besonderheiten / bekannte Probleme**

- `pdays = -1` wurde korrekt zu `NaN` konvertiert  
- `poutcome`, `contact`, `education`, `job` hatten viele fehlende Werte → ersetzt durch `unknown`  
- `balance_cat` hat 14 `NaN` wegen Grenzwerten beim Binning  
- starke Klassen-Imbalance → wichtig für Modellierung  
- `duration` wurde entfernt (post-event leakage)  
- numerische Variablen in `df_encoded` skaliert (StandardScaler)  
- kategorische Variablen vollständig One‑Hot encodiert (drop_first=False → keine Informationsverluste)

---

## 🧩 **Finale Outputs**

- **df** → 18 Spalten (cleaned dataset)  
- **df_encoded** → 57 Spalten (ready for ML)  
- **Keine Daten gelöscht**  
- **Alle Transformationen dokumentiert**  

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

> Hier dokumentieren welche neuen Features aus den Rohdaten abgeleitet wurden.

| Feature-Name | Herkunft | Formel / Logik | Datei |
|-------------|----------|----------------|-------|
| `rfm_recency` | GA4 | Tage seit letztem `purchase`-Event | `src/data/preprocessor.py` |
| `rfm_frequency` | GA4 | Anzahl `purchase`-Events je `user_pseudo_id` | `src/data/preprocessor.py` |
| `rfm_monetary` | GA4 | Summe `ecommerce.purchase_revenue` je User | `src/data/preprocessor.py` |
| `rfm_score` | GA4 | Quintil-Score 1–5 für R, F, M kombiniert | `src/analysis/segmentation.py` |
| `cluster_label` | GA4 | KMeans-Cluster-ID | `src/analysis/segmentation.py` |
| *(weitere ergänzen)* | | | |
