# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B
> **Status:** TEMPLATE — Ausfüllen bis M1 (KW 13)
> **Zweck:** Vollständige Dokumentation aller genutzten Datensätze als SSOT für das Team

---

## Datensatz 1: GA4 BigQuery Sample Ecommerce

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|-------------|-------|-----------|
| `event_date` | Datum des Events (YYYYMMDD) | STRING | `20210101` | Nein | H2 |
| `event_timestamp` | Unix-Timestamp in Mikrosekunden | INT64 | `1609459200000000` | Nein | — |
| `event_name` | Name des Events | STRING | `purchase`, `page_view` | Nein | H2 |
| `user_pseudo_id` | Anonymisierte User-ID (kein PII) | STRING | `abc123...` | Nein | H2 |
| `user_id` | App/Web User-ID (falls vorhanden) | STRING | — | Ja | — |
| `ga_session_id` | Session-ID | INT64 | `123456789` | Ja | H2 |
| `ecommerce.transaction_id` | Transaktions-ID | STRING | `T_12345` | Ja | H2 |
| `ecommerce.purchase_revenue` | Umsatz der Transaktion (USD) | FLOAT64 | `49.99` | Ja | H2 |
| `ecommerce.items` | Array mit Produktdetails | ARRAY | `[{item_id, item_name, ...}]` | Ja | H2 |
| *(weitere Felder ergänzen)* | | | | | |

**Quelle:** Google BigQuery Public Datasets — `bigquery-public-data.ga4_obfuscated_sample_ecommerce`
**Lizenz:** Google Public Data License
**Zeitraum:** [hier eintragen nach Download]
**Zeilen:** [hier eintragen]
**Besonderheiten / bekannte Probleme:**
- [ ] Obfuskierte User-IDs — kein Cross-Device-Tracking möglich
- [ ] Keine demografischen Daten enthalten

---

## Datensatz 2: UCI Bank Marketing

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|-------------|-------|-----------|
| `age` | Alter des Kunden | INT | `35` | Nein | H1, H2 |
| `job` | Berufsfeld | STRING | `admin.`, `blue-collar` | Nein | H1 |
| `marital` | Familienstand | STRING | `married`, `single` | Nein | H1 |
| `education` | Bildungsniveau | STRING | `secondary`, `tertiary` | Nein | H1 |
| `default` | Kreditausfall-Historie | STRING | `yes`, `no` | Nein | H1 |
| `balance` | Kontostand (EUR) | INT | `2000` | Nein | H1, H2 |
| `housing` | Wohnkredit | STRING | `yes`, `no` | Nein | H1 |
| `loan` | Privatkredit | STRING | `yes`, `no` | Nein | H1 |
| `contact` | Kontaktkanal | STRING | `cellular`, `telephone` | Ja | H1 |
| `day` | Letzter Kontakttag | INT | `15` | Nein | — |
| `month` | Letzter Kontaktmonat | STRING | `may`, `jun` | Nein | — |
| `duration` | Gesprächsdauer (Sekunden) | INT | `261` | Nein | H1 |
| `campaign` | Anzahl Kontakte diese Kampagne | INT | `3` | Nein | H1 |
| `pdays` | Tage seit letzter Kampagne | INT | `999` = nie kontaktiert | Nein | H1 |
| `previous` | Anzahl Kontakte vorherige Kampagnen | INT | `0` | Nein | H1 |
| `poutcome` | Ergebnis vorheriger Kampagne | STRING | `success`, `failure`, `unknown` | Ja | H1 |
| **`y`** | **Zielvariable: Hat Kunde Termin gebucht?** | STRING | `yes`, `no` | Nein | **H1** |

**Quelle:** UCI Machine Learning Repository — Bank Marketing Dataset
**URL:** https://archive.ics.uci.edu/dataset/222/bank+marketing
**Lizenz:** CC BY 4.0
**Datei:** `bank-full.csv` (vollständiger Datensatz, `;`-separiert)
**Zeilen:** 45.211 | **Spalten:** 17
**Besonderheiten / bekannte Probleme:**
- [ ] `duration` sollte für realistische Vorhersagen ausgeschlossen werden (Post-Contact-Information)
- [ ] `pdays = 999` kodiert "nie kontaktiert" — nicht als numerischer Wert interpretieren
- [ ] Klassen-Imbalance: ~88% `no`, ~12% `yes`

---

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
