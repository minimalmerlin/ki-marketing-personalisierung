# Kapitel 6 — Analyse & Ergebnisse
> Status: IN BEARBEITUNG | Verantwortlich: Person A (6.1, 6.2) + Person B (6.2 Empfehlungen) + Person C (6.3)
> Stand: 2026-04-07

---

## 6.1 H1: Conversion — Testergebnisse

### Fragestellung

**H1:** Personalisierte (segment-spezifische) Ansprache erzielt signifikant höhere Response-Raten als generische Massenkommunikation.

**H₀:** Die Response-Rate ist unabhängig von der Segmentzugehörigkeit — kein messbarer Unterschied.

---

### Test 1: Chi-Quadrat-Test (Segmentzugehörigkeit vs. Response)

Auf Basis der K-Means-Segmentierung (Notebook 03) wurden zwei Segmente gebildet: **Experienced** (7,5%, n=3.379) mit positiver Kontaktvorhistorie und hohem Kontostand sowie **Mass Market** (92,5%, n=41.832) ohne Vorhistorie.

**Kontingenzmatrix:**

| Segment | Response: No | Response: Yes | Response-Rate |
|---|---|---|---|
| Experienced | 2.513 | 866 | **25,63%** |
| Mass Market | 37.409 | 4.423 | **10,57%** |
| **Gesamt** | 39.922 | 5.289 | **11,70%** |

**Ergebnis:**

| Kennzahl | Wert |
|---|---|
| Chi² | 684,59 |
| Freiheitsgrade (df) | 1 |
| p-Wert | 6,71 × 10⁻¹⁵¹ |
| Cramér's V | 0,123 (mittlere Effektstärke) |

Der p-Wert liegt weit unterhalb des Signifikanzniveaus α = 0,05. **H₀ wird abgelehnt.**

---

### Test 2: Z-Test (Proportionenvergleich)

Ein einseitiger Z-Test vergleicht die Response-Rate des besten Segments direkt gegen die Gesamtbaseline:

| Kennzahl | Wert |
|---|---|
| Experienced | 25,63% |
| Mass Market | 10,57% |
| Z-Statistik | 26,19 |
| p-Wert (einseitig) | ≈ 0,000 |
| Cohen's h | 0,399 (mittlerer Effekt) |
| **Lift** | **2,42×** |

Das Experienced-Segment erzielt eine **2,42-fach höhere Response-Rate** als das Mass-Market-Segment.

---

### Robustheitsprüfung

Zur Absicherung wurden weitere natürliche Segmentierungsmerkmale auf denselben Effekt geprüft:

| Merkmal | Chi² | p-Wert | Cramér's V | Signifikant |
|---|---|---|---|---|
| Berufsgruppe (job) | 836,11 | < 0,001 | 0,136 | Ja |
| Bildung (education) | 238,92 | < 0,001 | 0,073 | Ja |
| Familienstand (marital) | 196,50 | < 0,001 | 0,066 | Ja |

Alle geprüften Segmentierungsvariablen zeigen signifikante Effekte. Das Ergebnis ist **robust** — der H1-Befund ist nicht auf eine spezifische Clustering-Entscheidung zurückzuführen, sondern spiegelt eine generelle Heterogenität im Kundenverhalten wider.

---

### Interpretation

**H1 ist bestätigt.** Segment-spezifische Ansprache erzielt messbar höhere Response-Raten als generische Massenkommunikation. Der Lift von 2,42× zeigt, dass die Identifikation des richtigen Segments — statt alle Kunden gleich zu behandeln — den Kampagnenerfolg mehr als verdoppeln kann.

Die Effektstärke (Cramér's V = 0,123) ist als mittel einzustufen: Die Segmentzugehörigkeit erklärt einen signifikanten, aber nicht dominanten Anteil der Varianz. Das bedeutet in der Praxis: Segmentierung ist ein starker Hebel, aber kein Alleinstellungsmerkmal — weitere Faktoren (Timing, Kanal, Botschaft) bleiben relevant.

> Abbildungen: `outputs/hyp_h1_response_ci.png`, `outputs/hyp_summary.png`

---

## 6.2 H2: Relevanz — Segmentierung & Empfehlungen
> ⚠️ PLATZHALTER (Empfehlungslogik) — wird nach Fertigstellung von Notebook 05 durch Person B ergänzt

### Silhouette & Conversion-Lift (Person A)

**Silhouette-Score GA4 (Tier-1, k=2):** 0,7175

Permutationstest (N=100 Zufalls-Zuordnungen):
- Random-Baseline: Ø −0,0113 (SD = 0,053)
- p-Wert: 0,000 → H₀ abgelehnt

Die Segmentierung ist statistisch valide und weit besser als zufällige Cluster-Zuordnung.

**Conversion-Rate je GA4-Segment:**

| Segment | n | Conversion-Rate | Lift vs. Baseline |
|---|---|---|---|
| Champions | 491 | 10,59% | 26,3× |
| Loyal Buyers | 3.463 | 3,78% | 9,4× |
| Passive | 63.865 | 0,14% | 0,35× |
| **Baseline (gesamt)** | 67.819 | **0,40%** | — |

Der Champions-Lift von **75,2×** gegenüber Passive-Nutzern belegt, dass verhaltensbasierte Segmentierung die Treffsicherheit der Ansprache massiv verbessert.

> Abbildungen: `outputs/hyp_h2_silhouette_permtest.png`, `outputs/hyp_h2_conversion_lift.png`

### Empfehlungslogik (Platzhalter Person B)
> ⚠️ Precision@K-Auswertung und Item-basierte Co-Occurrence folgen nach Notebook 05

---

## 6.3 H3: Grenze — DSGVO-Risiko-Analyse
> ⚠️ PLATZHALTER — wird von Person C nach Fertigstellung von Notebook 06 ergänzt
