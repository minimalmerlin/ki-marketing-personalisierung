# QA-Checkliste — Abgabe-Gates

> **Verantwortlich:** Person C
> **Auszufüllen:** KW 15 vor finaler Abgabe
> **Regel:** Alle Gates müssen grün sein. Kein partielle Abgabe.

---

## Gate 1 — Reproduzierbarkeit

- [ ] `make setup` läuft fehlerfrei durch (frische venv)
- [ ] Alle 6 Notebooks laufen von oben nach unten ohne Fehler
- [ ] Notebooks laufen in korrekter Reihenfolge (01 → 02 → 03 → 04 → 05 → 06)
- [ ] Kein Hard-coded lokaler Pfad (kein `/Users/[name]/...`)
- [ ] Alle Pfade relativ zum Repo-Root oder via Konstante in `src/utils/helpers.py`
- [ ] `data/raw/` und `data/processed/` sind leer im Repo (nur `.gitkeep`)
- [ ] `requirements.txt` vollständig — alle Imports gedeckt

---

## Gate 2 — Daten-Qualität

- [ ] Kein PII in `data/processed/` oder Notebook-Outputs
- [ ] `docs/data_dictionary_template.md` vollständig ausgefüllt (Person B)
- [ ] Fehlende Werte dokumentiert und behandelt (im Notebook kommentiert)
- [ ] Train/Test-Split (falls angewandt) dokumentiert und reproduzierbar (fixed random seed)
- [ ] Keine Datenleckage zwischen Gruppen bei Hypothesentests

---

## Gate 3 — Hypothesen (inhaltlich)

### H1 — Conversion
- [ ] Test-Methode klar begründet (Chi² oder t-Test — warum?)
- [ ] p-Wert und Signifikanzniveau (α = 0.05) dokumentiert
- [ ] Effektstärke berichtet (Cramér's V oder Cohen's d)
- [ ] Klare Aussage: H1 bestätigt / widerlegt / teilweise bestätigt + Begründung

### H2 — Relevanz
- [ ] Silhouette-Score für gewählte Cluster-Anzahl dokumentiert
- [ ] Cluster inhaltlich interpretiert (Wer ist Segment X?)
- [ ] Precision@K oder equivalent dokumentiert
- [ ] Klare Aussage: H2 bestätigt / widerlegt / teilweise bestätigt + Begründung

### H3 — Grenze
- [ ] Profiling-Stufenmodell (mind. 3 Stufen) definiert
- [ ] Rechtsgrundlagen für jede Stufe zugeordnet (DSGVO-Artikel)
- [ ] EDPB und ICO Guidance direkt zitiert (mind. je 2 Zitate)
- [ ] Klare Schwellen-Empfehlung: Ab Stufe X ist DSGVO-Risiko > Mehrwert
- [ ] Klare Aussage: H3 bestätigt / widerlegt + Begründung

---

## Gate 4 — Code-Qualität

- [ ] Type Hints in allen `.py`-Dateien in `src/`
- [ ] Keine ungenutzen Imports
- [ ] Keine auskommentierten Code-Blöcke (außer bewusste Kommentare)
- [ ] Notebook-Zellen: Keine leeren Outputs aus Debug-Läufen
- [ ] `ruff check src/` — 0 Fehler (oder alle bekannten Ausnahmen dokumentiert)
- [ ] Funktionen haben Docstrings (min. 1-Zeiler)

---

## Gate 5 — Bericht

- [ ] Alle 9 Kapitel + Anhang vorhanden
- [ ] Forschungsfrage in Kap. 1 identisch mit Charter
- [ ] H1, H2, H3 in Kap. 2 theoretisch fundiert
- [ ] Hypothesen-Ergebnisse in Kap. 6 klar pro Hypothese strukturiert
- [ ] Kap. 7 diskutiert alle 3 Hypothesen gemeinsam
- [ ] Anhang A (Data Dictionary) vollständig
- [ ] Literaturverzeichnis: min. 10 Quellen, davon 3 Primärquellen (EDPB, ICO, Datensatz-Paper)
- [ ] Keine Plagiate (Eigenständigkeitserklärung unterzeichnet)
- [ ] Seitenzahl innerhalb Vorgabe

---

## Gate 6 — Repo-Hygiene

- [ ] `main`-Branch ist sauber (kein WIP-Code)
- [ ] Alle Feature-Branches gemerged oder bewusst offen gelassen
- [ ] `.gitignore` greift: `git status` zeigt keine `data/raw/` oder `data/processed/` Dateien
- [ ] `README.md` aktuell (Milestone-Status, Team)
- [ ] Commit-History lesbar (keine "fix fix fix"-Commits auf main)
- [ ] Keine Secrets, API-Keys, Passwörter in der Git-History

---

## Gate 7 — Präsentation

- [ ] Präsentation enthält: Frage → Methode → Ergebnisse → Empfehlung (max. 15 Folien)
- [ ] Alle 3 Hypothesen im Ergebnis-Teil adressiert
- [ ] Visualisierungen aus `outputs/figures/` (keine Screenshot-Fotos)
- [ ] Zeitplan eingehalten: ≤ 15 Min Vortrag + 5 Min Fragen

---

## Abzeichnung

| Gate | Status | Abgezeichnet von | Datum |
|------|--------|-----------------|-------|
| 1 — Reproduzierbarkeit | ⬜ offen | | |
| 2 — Daten-Qualität | ⬜ offen | | |
| 3 — Hypothesen | ⬜ offen | | |
| 4 — Code-Qualität | ⬜ offen | | |
| 5 — Bericht | ⬜ offen | | |
| 6 — Repo-Hygiene | ⬜ offen | | |
| 7 — Präsentation | ⬜ offen | | |

> **Freigabe zur Abgabe:** Alle Gates grün + alle 3 Personen haben abgezeichnet.
