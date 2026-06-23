PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup install generate build validate run clean metabase

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -r requirements.txt

install:
	$(BIN)/python -m pip install -r requirements.txt

generate:
	$(BIN)/python scripts/generate_data.py

build:
	$(BIN)/python scripts/build_warehouse.py

validate:
	$(BIN)/python scripts/validate_warehouse.py

run: generate build validate

metabase:
	cd metabase && docker compose up --build

clean:
	rm -rf data/raw/*.csv data/warehouse/*.duckdb data/warehouse/*.duckdb.wal data/exports/*.csv

