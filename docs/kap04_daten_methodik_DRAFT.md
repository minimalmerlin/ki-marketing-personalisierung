# Kapitel 4 — Daten & Methodik
> Status: IN BEARBEITUNG | Verantwortlich: Person A (4.1, 4.3, 4.4) + Person B (4.2)
> Stand: 2026-04-07

---

## 4.1 Datensätze & Auswahl

**GA4 BigQuery Sample — Verhaltensdaten**

Der GA4-Datensatz stammt aus dem öffentlich verfügbaren BigQuery Sample des Google Merchandise Stores. Er enthält Event-Level-Daten aus dem Zeitraum November–Dezember 2020 mit 67.819 Nutzern nach Preprocessing (Rohexport: 50.000 Events / 3.420 Nutzer im EDA-Sample). Erfasst werden Nutzerinteraktionen wie `page_view`, `view_item`, `begin_checkout` und `purchase` sowie Gerätekategorie, Geografie und Traffic-Quelle.

Relevanz für das Projekt: Der Datensatz ermöglicht verhaltensbasierte Segmentierung (RFM-Logik auf Session-Basis), Conversion-Funnel-Analyse und die Simulation einer Empfehlungslogik auf Basis von Produktinteraktion.

**UCI Bank Marketing Dataset — Kampagnendaten**

Der UCI Bank Marketing Datensatz dokumentiert 45.211 Kundenkontakte einer portugiesischen Direktmarketing-Kampagne (Telefon-Outbound) zur Bewerbung von Termineinlagen. Er enthält 17 Merkmale — darunter demografische Angaben (Alter, Beruf, Familienstand), finanzielle Kennzahlen (Kontostand, Kredite) und kampagnenbezogene Variablen (Anzahl Kontakte, Vorhistorie, Gesprächsdauer).

Relevanz für das Projekt: Die binäre Zielvariable (`y`: Abschluss ja/nein) ermöglicht direkte Response-Modellierung und den Vergleich segment-spezifischer vs. generischer Ansprache.

**Begründung der Datenwahl (Datenfit-Checkliste):**

| Kriterium | GA4 | Bank Marketing |
|---|---|---|
| Klare Zielvariable vorhanden | Ja (purchase / has_purchased) | Ja (y / y_binary) |
| Merkmale zur Personalisierung | Ja (Verhalten, Session, Produkt) | Ja (Demografik, Historie, Balance) |
| Vergleich personalisiert vs. generisch | Ja (Segment vs. Baseline) | Ja (Experienced vs. Mass Market) |
| Datenschutz-Dimension diskutierbar | Ja (Verhaltens-Tracking) | Ja (Profiling auf Basis Finanzdaten) |

---

## 4.2 Datenaufbereitung
> ⚠️ PLATZHALTER — wird von Person B ergänzt (Preprocessing-Details, Feature Engineering, src/data/preprocessor.py)

---

## 4.3 Analysemethoden

| Hypothese | Methode | Kennzahl |
|---|---|---|
| H1 — Conversion | Chi²-Test + Z-Test (Proportionen) | p-Wert, Cramér's V, Cohen's h, Lift |
| H2 — Relevanz | K-Means + Permutationstest (Silhouette) | Silhouette-Score, Conversion-Rate je Segment, Lift |
| H3 — Grenze | Qualitative Analyse + Profiling-Stufenmodell | Risiko-Score-Matrix (Stufe 1–4) |

---

## 4.4 Limitationen

- **GA4-Sample-Bias:** Der Datensatz umfasst nur einen begrenzten Zeitraum (Nov–Dez 2020) eines einzelnen Shops (Google Merchandise Store). Saisonale Effekte und Shop-spezifisches Nutzerverhalten limitieren die Generalisierbarkeit.
- **Bank Marketing — Kontext:** Der Datensatz stammt aus dem portugiesischen Markt (2008–2010) und ist nicht direkt auf den aktuellen EU-E-Commerce-Kontext übertragbar. Zeitlich veraltete Kampagnenstrukturen können die Ergebnisse verzerren.
- **H3 — Konzeptionelle Analyse:** Die DSGVO-Bewertung basiert auf einer qualitativen Analyse der Methoden, nicht auf einer empirischen Erhebung. Die Risikobewertung ist normativ, nicht gemessen.
- **Kein A/B-Test:** Der Conversion-Lift ist simuliert auf Basis von Segmentunterschieden — kein echter randomisierter Experiment-Aufbau. Kausalität kann nicht direkt nachgewiesen werden.
