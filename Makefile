.PHONY: setup lint test notebook clean help

# === Config ===
PYTHON := python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
RUFF   := $(VENV)/bin/ruff
MYPY   := $(VENV)/bin/mypy

# === Setup ===
setup:  ## Virtualenv erstellen + Dependencies installieren
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✓ Setup abgeschlossen. Aktivieren: source $(VENV)/bin/activate"

# === Lint ===
lint:   ## Ruff Linter + Mypy Type Check
	$(RUFF) check src/ notebooks/
	$(MYPY) src/

format: ## Ruff Auto-Format
	$(RUFF) format src/

# === Tests ===
test:   ## pytest ausführen (falls vorhanden)
	$(VENV)/bin/pytest tests/ -v

# === Notebooks ===
notebook: ## Jupyter Lab starten
	$(VENV)/bin/jupyter lab notebooks/

# === Clean ===
clean:  ## Caches und temp-Dateien löschen
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Clean abgeschlossen"

# === Help ===
help:   ## Alle Targets anzeigen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
