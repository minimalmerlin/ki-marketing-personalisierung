# Kapitel 5 — Explorative Datenanalyse (EDA)
> Status: IN BEARBEITUNG | Verantwortlich: Person A
> Stand: 2026-04-07

---

## 5.1 GA4 Ecommerce — Verhaltensdaten

Der GA4-Datensatz umfasst **50.000 Events von 3.420 einzigartigen Nutzern** in **3.860 Sessions** im Zeitraum 08.–27. November 2020 (Google Merchandise Store). Der Datensatz enthält 15 Event-Typen ohne fehlende Werte.

**Event-Verteilung:** Dominiert wird das Verhalten durch passive Interaktionen — `page_view` (16.509), `user_engagement` (14.676) und `scroll` (5.651) machen den Großteil aus. Aktive Kaufinteresse-Signale wie `view_item` (3.999) und `begin_checkout` (133) sind deutlich seltener.

**Conversion Funnel:**

| Schritt | Anzahl | Anteil (absolut) | Schritt-zu-Schritt |
|---|---|---|---|
| Session Start | 3.834 | 100% | — |
| View Item | 3.999 | 104% | 104% |
| Begin Checkout | 133 | 3,5% | 3,3% |
| Purchase | 32 | 0,8% | 24,1% |

Der starke Drop zwischen `view_item` und `begin_checkout` (3,3%) zeigt, dass der größte Personalisierungshebel im oberen Funnel liegt — Produktrelevanz entscheidet, ob ein Nutzer überhaupt in Richtung Kauf bewegt wird. Immerhin 24,1% der Checkout-Starter schließen den Kauf ab.

**Gesamte Conversion Rate: 0,9%** (31 von 3.420 Nutzern tätigten mindestens einen Kauf). Unter Käufern betrug der mittlere Umsatz **121,28 USD** (Median: 69 USD, Max: 717,60 USD).

**Geräte & Traffic:** Desktop dominiert mit 57,8% (2.231 Sessions), gefolgt von Mobile (39,9%, 1.540 Sessions) und Tablet (2,3%). Der primäre Traffic-Kanal ist organische Google-Suche (34,2%), gefolgt von sonstigen Quellen (27,8%) und Direct (22,7%).

**Geografie:** Die USA stellen mit 50% die größte Nutzergruppe, gefolgt von Indien (10,5%) und Kanada (8,2%). Dies spiegelt die internationale Reichweite des Google Merchandise Stores wider.

> Abbildungen: `outputs/ga4_conversion_funnel.png`, `outputs/ga4_traffic_device.png`, `outputs/ga4_user_features_distribution.png`

**Key Finding:** Der GA4-Datensatz belegt ein stark segmentiertes Nutzerverhalten — wenige hochaktive Nutzer (Kaufende, Checkout-Starter) stehen einer großen Masse passiver Browser gegenüber. Diese bimodale Struktur ist die analytische Grundlage für die Segmentierung in Kapitel 6.2.

---

## 5.2 Bank Marketing — Kampagnendaten

Der UCI Bank Marketing Datensatz umfasst **45.211 Kundenkontakte** einer portugiesischen Direktmarketingkampagne mit **17 Merkmalen** (demografisch, finanziell, kampagnenbezogen). Es liegen **keine fehlenden Werte oder Duplikate** vor.

**Zielvariable:** Die Response-Rate (Abschluss Termineinlage = „yes") beträgt **11,7%** — ein deutliches Class-Imbalance-Problem. Ein naives Modell, das immer „no" vorhersagt, erreicht 88,3% Accuracy und dient als Baseline für H1.

**Demografische Muster:**

| Merkmal | Höchste Response-Gruppe | Response-Rate |
|---|---|---|
| Berufsgruppe | Studenten | 28,7% |
| Berufsgruppe | Rentner | 22,8% |
| Bildung | Tertiär | 15,0% |
| Familienstand | Single | 14,9% |

Alter spielt eine untergeordnete Rolle (Median: 39 Jahre bei „no", 38 Jahre bei „yes"). Der **Kontostand** differenziert jedoch klar: Responder haben einen deutlich höheren Median-Kontostand (733 EUR vs. 417 EUR bei Non-Respondern).

**Saisonalität:** Die Response-Rate variiert stark nach Kontaktmonat. März (52,0%), Dezember (46,7%), September (46,5%) und Oktober (43,8%) zeigen deutlich überdurchschnittliche Raten — Mai hingegen nur 6,7%. Dies deutet auf starke kampagnenbezogene Timing-Effekte hin.

**Methodische Anmerkung:** Das Feature `duration` (Gesprächsdauer in Sekunden) korreliert stark mit der Zielvariable (Median: 426s bei „yes" vs. 164s bei „no"), ist jedoch **Data Leakage** — es ist erst nach dem Gespräch bekannt und wurde daher aus allen prädiktiven Analysen ausgeschlossen.

> Abbildungen: `outputs/bank_response_by_job.png`, `outputs/bank_response_by_month.png`, `outputs/bank_response_by_demographics.png`, `outputs/bank_correlation_matrix.png`

**Key Finding:** Die Bank-Daten zeigen, dass Personalisierung auf Basis von Vorhistorie (`previous`, `poutcome`) und Kontostand (`balance`) die stärksten Differenzierungsmerkmale liefert. Demographische Merkmale allein reichen nicht aus — die Kombination aus Kundenhistorie und Timing ist entscheidend.

---

## 5.3 Synthese: Personalisierungspotenzial der Daten

Beide Datensätze bestätigen das zentrale Grundmuster: **Kundenverhalten ist nicht homogen** — kleine Teilgruppen mit spezifischen Merkmalen reagieren signifikant anders als die Masse. Im GA4-Datensatz sind es kaufaktive Nutzer mit mehreren Sessions und Produktinteraktion; im Bank-Datensatz Kunden mit positiver Vorhistorie und höherem Kontostand.

Dies liefert die empirische Ausgangsbasis für die Hypothesentests: Wenn diese Gruppen identifizierbar und gezielt ansprechbar sind, sollte segment-spezifische Ansprache messbar besser performen als generische Massenkommunikation (→ H1 und H2).
