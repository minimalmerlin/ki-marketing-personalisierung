# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B
> **Status:** Status: FINAL — Version 1.0 (Stand: 02.04.2026)
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
| `age` | Alter des Kunden | INT64 | `56` | Nein | H1 |
| `job` | Berufsfeld des Kunden | STRING | `services`, `admin.`, `technician` | Nein | H1 |
| `marital` | Familienstand | STRING | `married`, `single`, `divorced` | Nein | H1 |
| `education` | Bildungsniveau | STRING | `high.school`, `university.degree` | Nein | H1 |
| `default` | Kreditausfall-Historie | STRING | `yes`, `no` | Nein | H1 |
| `housing` | Wohnkredit | STRING | `yes`, `no` | Nein | H1 |
| `loan` | Privatkredit | STRING | `yes`, `no` | Nein | H1 |
| `contact` | Kontaktkanal | STRING | `cellular`, `telephone` | Nein | H1 |
| `month` | Monat des letzten Kontakts | STRING | `may`, `jun` | Nein | — |
| `day_of_week` | Wochentag des letzten Kontakts | STRING | `mon`, `tue` | Nein | — |
| `duration` | Dauer des letzten Kontakts (Sekunden) | INT64 | `180` | Nein | **Leakage → entfernt** |
| `campaign` | Anzahl Kontakte in dieser Kampagne | INT64 | `2` | Nein | H1 |
| `pdays` | Tage seit letzter Kampagne (`999` = nie kontaktiert) | INT64 | `999` | Nein | H1 |
| `previous` | Anzahl früherer Kontakte | INT64 | `0` | Nein | H1 |
| `poutcome` | Ergebnis früherer Kampagne | STRING | `nonexistent`, `success`, `failure` | Nein | H1 |
| `emp.var.rate` | Beschäftigungsänderungsrate | FLOAT64 | `1.1` | Nein | H2 |
| `cons.price.idx` | Verbraucherpreisindex | FLOAT64 | `93.994` | Nein | H2 |
| `cons.conf.idx` | Konsumentenvertrauensindex | FLOAT64 | `-36.4` | Nein | H2 |
| `euribor3m` | 3‑Monats Euribor | FLOAT64 | `4.857` | Nein | H2 |
| `nr.employed` | Anzahl Beschäftigte | FLOAT64 | `5191.0` | Nein | H2 |
| `y` | Zielvariable: Hat Kunde zugesagt? | STRING | `yes`, `no` | Nein | H1 |

---

## 📦 **Metadaten**

- **Zeilen:** 41.176  
- **Spalten (Original):** 21  
- **Spalten (nach Cleaning):** 20 (da `duration` entfernt wurde)  
- **Spalten (nach One‑Hot Encoding):** abhängig vom Encoding (typisch 50–60+)  

### **Target Imbalance**
- `no`: **88.74%**  
- `yes`: **11.26%**

---

## ⚠️ **Besonderheiten / bekannte Probleme**

- `duration` wurde entfernt → **post-event leakage**  
- `pdays = 999` bedeutet **nie kontaktiert** (logisches Missing)  
- starke Klassen-Imbalance → wichtig für Modellierung  
- kategorische Variablen haben hohe Cardinality (`job`, `education`)  
- numerische Variablen weisen unterschiedliche Skalen auf → StandardScaler empfohlen  
- `poutcome` enthält viele `nonexistent` → wichtig für Feature Engineering  

---

## 🧩 **Finale Outputs**

- **df_cleaned** → 20 Spalten (ohne `duration`)  
- **df_encoded** → One‑Hot encodiert, skaliert, modellbereit  
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
