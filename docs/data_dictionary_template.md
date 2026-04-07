# Data Dictionary — KI-gestützte Personalisierung im Marketing

> **Verantwortlich:** Person B  
> **Status:** Fertig für M1 (KW 13)  
> **Zweck:** Vollständige Dokumentation aller genutzten Datensätze als SSOT für das Team  

---

## Metadaten

| Feld | Wert |
|------|------|
| **Version** | 1.1.0 |
| **Letzte Aktualisierung** | 2026-04-07 |
| **Erstellt von** | Person B |
| **Änderungshistorie** | v1.0.0 — Initiale Version (KW 13); v1.1.0 — GA4-Felder vervollständigt, Encoding-Referenz ergänzt, Sprache vereinheitlicht |

---

## Datensatz 1: GA4 BigQuery Sample Ecommerce (Processed CSV)

| Feld | Beschreibung | Typ | Beispielwert | Null? | Hypothese |
|------|-------------|-----|-------------|-------|-----------|
| `event_date` | Datum des Events (YYYYMMDD) | INT64 | `20210131` | Nein | H2 — Nutzeraktivität variiert nach Datum |
| `event_timestamp` | Unix-Timestamp in Mikrosekunden | FLOAT64 | `1612069510766593.0` | Nein | — |
| `event_name` | Name des Events (siehe Werteliste unten) | STRING | `page_view`, `scroll`, `purchase` | Nein | H2 — Bestimmte Events korrelieren mit Engagement |
| `user_pseudo_id` | Anonymisierte User-ID (kein PII) | FLOAT64 (ursprünglich STRING) | `1026454.427` | Nein | H2 — Nutzerverhalten über Sessions analysierbar |
| `platform` | Plattform des Users | STRING | `WEB` | Nein | H2 — Verhalten unterscheidet sich zwischen Plattformen |
| `device_category` | Gerätetyp des Users | STRING | `mobile`, `desktop`, `tablet` | Nein | H2 — Mobile Nutzer zeigen anderes Verhalten |
| `country` | Land des Users | STRING | `United States`, `Germany` | Nein | H2 — Geografische Unterschiede im Verhalten |

### Vollständige Werteliste: `event_name`

| Event-Name | Kategorie | Beschreibung |
|------------|-----------|-------------|
| `page_view` | Navigation | Seitenaufruf |
| `scroll` | Engagement | Nutzer scrollt auf der Seite |
| `user_engagement` | Engagement | Mindest-Engagement-Schwelle erreicht |
| `session_start` | Session | Beginn einer neuen Session |
| `first_visit` | Akquisition | Erster Besuch des Nutzers |
| `click` | Interaktion | Klick auf ein Element |
| `view_item` | E-Commerce | Produktdetailseite aufgerufen |
| `select_item` | E-Commerce | Produkt aus Liste ausgewählt |
| `add_to_cart` | E-Commerce | Produkt in Warenkorb gelegt |
| `begin_checkout` | E-Commerce | Checkout-Prozess gestartet |
| `add_shipping_info` | E-Commerce | Versandinformationen eingegeben |
| `add_payment_info` | E-Commerce | Zahlungsinformationen eingegeben |
| `purchase` | E-Commerce | Kauf abgeschlossen |
| `view_promotion` | Marketing | Promotion-Banner angezeigt |
| `select_promotion` | Marketing | Promotion-Banner angeklickt |
| `view_search_results` | Suche | Suchergebnisse angezeigt |

### Vollständige Werteliste: `device_category`

| Wert | Beschreibung |
|------|-------------|
| `mobile` | Smartphone |
| `desktop` | Desktop / Laptop |
| `tablet` | Tablet-Gerät |

---

**Quelle:** GA4 Export (Processed CSV)  
**Lizenz:** Google Public Data License  
**Zeitraum:** 2021‑01‑31  
**Zeilen:** 26.489  

---

## Besonderheiten / bekannte Probleme (GA4)

- [x] Obfuskierte User-IDs — kein Cross-Device-Tracking möglich  
- [x] Keine demografischen Daten enthalten (GA4-typisch)  
- [x] `user_pseudo_id` wurde beim CSV‑Export zu FLOAT64 konvertiert  
  → Empfehlung: später in STRING casten  
- [x] Dieses Subset enthält Engagement- und E-Commerce-Events  
- [x] Daten stammen nur aus einem einzigen Tag (2021-01-31)  
  → Für Zeitreihenanalysen ungeeignet  

---

## Hinweis für das Team (GA4)

Dieser Datensatz eignet sich besonders für:

- Analyse von Nutzerverhalten  
- Event-basierte Segmentierung  
- Modellierung von Engagement  
- Vorbereitung für KI‑gestützte Personalisierungsmodelle  

Für Kauf- oder Revenue-Modelle wird ein zusätzlicher Datensatz benötigt.

---

## Datensatz 2: UCI Bank Marketing Dataset (Numerisch kodierte Version)

Dieser Datensatz enthält die numerisch kodierte Version des UCI Bank Marketing Datensatzes mit 41.188 Zeilen und 21 Spalten.

### Datenwörterbuch

| Spalte | Beschreibung | Typ | Hinweise |
|--------|-------------|------|---------|
| `age` | Alter des Kunden | int | — |
| `job` | Berufsgruppe (kodiert) | int | Encoding-Referenz siehe unten |
| `marital` | Familienstand (kodiert) | int | Encoding-Referenz siehe unten |
| `education` | Bildungsstand (kodiert) | int | Encoding-Referenz siehe unten |
| `default` | Kreditausfall-Vorgeschichte (kodiert) | int | Encoding-Referenz siehe unten |
| `housing` | Wohnungsdarlehen (kodiert) | int | Encoding-Referenz siehe unten |
| `loan` | Privatdarlehen (kodiert) | int | Encoding-Referenz siehe unten |
| `contact` | Kontaktkommunikationstyp (kodiert) | int | Encoding-Referenz siehe unten |
| `month` | Letzter Kontaktmonat (kodiert) | int | Encoding-Referenz siehe unten |
| `day_of_week` | Letzter Kontaktwochentag (kodiert) | int | Encoding-Referenz siehe unten |
| `duration` | Gesprächsdauer in Sekunden | int | ⚠️ Soll aus prädiktiven Modellen ausgeschlossen werden |
| `campaign` | Anzahl Kontakte während dieser Kampagne | int | — |
| `pdays` | Tage seit letztem Kontakt | int | -1 = noch nie kontaktiert |
| `previous` | Anzahl vorheriger Kontakte | int | — |
| `poutcome` | Ergebnis der vorherigen Kampagne (kodiert) | int | Encoding-Referenz siehe unten |
| `emp.var.rate` | Beschäftigungsveränderungsrate | float | Makroökonomisch |
| `cons.price.idx` | Verbraucherpreisindex | float | Makroökonomisch |
| `cons.conf.idx` | Verbrauchervertrauensindex | float | Makroökonomisch |
| `euribor3m` | Euribor 3-Monats-Satz | float | Makroökonomisch |
| `nr.employed` | Anzahl der Beschäftigten | float | Makroökonomisch |
| `y` | Zielvariable (0 = nein, 1 = ja) | int | — |

### Encoding-Referenz

#### `job` — Berufsgruppe

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| -1 | `unknown` | Unbekannt |
| 0 | `admin.` | Verwaltung |
| 1 | `blue-collar` | Handwerk / Arbeiter |
| 2 | `entrepreneur` | Unternehmer |
| 3 | `housemaid` | Haushaltshilfe |
| 4 | `management` | Management |
| 5 | `retired` | Rentner |
| 6 | `self-employed` | Selbstständig |
| 7 | `services` | Dienstleistungen |
| 8 | `student` | Student |
| 9 | `technician` | Techniker |
| 10 | `unemployed` | Arbeitslos |

#### `marital` — Familienstand

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| -1 | `unknown` | Unbekannt |
| 0 | `divorced` | Geschieden / verwitwet |
| 1 | `married` | Verheiratet |
| 2 | `single` | Ledig |

#### `education` — Bildungsstand

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| -1 | `unknown` | Unbekannt |
| 0 | `basic.4y` | Grundschule (4 Jahre) |
| 1 | `basic.6y` | Grundschule (6 Jahre) |
| 2 | `basic.9y` | Grundschule (9 Jahre) |
| 3 | `high.school` | Gymnasium / Abitur |
| 4 | `illiterate` | Analphabet |
| 5 | `professional.course` | Berufsausbildung |
| 6 | `university.degree` | Hochschulabschluss |

#### `default` — Kreditausfall, `housing` — Wohnungsdarlehen, `loan` — Privatdarlehen

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| -1 | `unknown` | Unbekannt |
| 0 | `no` | Nein |
| 1 | `yes` | Ja |

#### `contact` — Kontakttyp

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| 0 | `cellular` | Mobiltelefon |
| 1 | `telephone` | Festnetz |

#### `month` — Letzter Kontaktmonat

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| 0 | `apr` | April |
| 1 | `aug` | August |
| 2 | `dec` | Dezember |
| 3 | `jul` | Juli |
| 4 | `jun` | Juni |
| 5 | `mar` | März |
| 6 | `may` | Mai |
| 7 | `nov` | November |
| 8 | `oct` | Oktober |
| 9 | `sep` | September |

#### `day_of_week` — Letzter Kontaktwochentag

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| 0 | `fri` | Freitag |
| 1 | `mon` | Montag |
| 2 | `thu` | Donnerstag |
| 3 | `tue` | Dienstag |
| 4 | `wed` | Mittwoch |

#### `poutcome` — Ergebnis der vorherigen Kampagne

| Code | Originalwert | Bedeutung |
|------|-------------|-----------|
| 0 | `failure` | Misserfolg |
| 1 | `nonexistent` | Kein vorheriger Kontakt |
| 2 | `success` | Erfolg |

### Datensatz-Informationen
- **Zeilen:** 41.188  
- **Spalten:** 21  
- **Fehlende Werte:** 0 % in allen Spalten  
- **Zielvariable:** `y` (0 = nein, 1 = ja)  
- **Quelle:** UCI Machine Learning Repository  
- **Lizenz:** CC BY 4.0  

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

## Datensatz 5: MIND — Microsoft News Dataset

> **Status:** Nicht verwendet — GA4-Datensatz ist für die Recommender-Analyse ausreichend.  
> Dieser Datensatz wurde initial als optionale Erweiterung vorgesehen, wird aber im aktuellen Projektumfang nicht eingesetzt.

| Feld | Beschreibung | Typ | Hypothese |
|------|-------------|-----|-----------|
| `user_id` | Anonymisierte User-ID | STRING | H2 |
| `history` | Klick-Historie (Artikel-IDs) | ARRAY[STRING] | H2 — Vergangenes Verhalten als Signal |
| `impressions` | Gezeigte Artikel + Klick-Label (Format: `news_id-label`) | ARRAY[STRING] | H2 — Implizites Feedback |
| `news_id` | Eindeutige Artikel-ID | STRING | H2 |
| `category` | Nachrichtenkategorie (z. B. Sports, Finance) | STRING | H2 — Thematische Präferenzen |
| `subcategory` | Unterkategorie des Artikels | STRING | H2 |
| `title` | Artikeltitel | STRING | H2 |
| `abstract` | Kurzzusammenfassung des Artikels | STRING | H2 |

**Quelle:** Microsoft Research — MIND Dataset  
**Datei:** `data/raw/mind/` (nach Download entpacken)  
**Entscheidung:** Nicht in Verwendung — wird durch GA4-Datensatz ersetzt

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

