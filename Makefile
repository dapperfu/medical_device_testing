.PHONY: help build test run lint clean \
	strictdoc-init strictdoc-generate strictdoc-validate \
	strictdoc-export strictdoc-serve strictdoc-tree strictdoc-help

UV ?= uv
STRICTDOC ?= $(UV) run strictdoc

help:
	@echo "Targets: build test run lint clean"
	@echo "StrictDoc: strictdoc-init strictdoc-generate strictdoc-validate strictdoc-export strictdoc-serve strictdoc-tree strictdoc-help"

build:
	$(UV) sync

test: build
	mkdir -p docs
	$(UV) run pytest

run: build
	$(UV) run python -m medical_device_testing

lint: build
	$(UV) run ruff check src tests strictdoc_config.py

clean:
	rm -rf .venv .pytest_cache .ruff_cache .strictdoc_cache output src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

strictdoc-init:
	@echo "StrictDoc sources live in requirements/. Config is strictdoc_config.py."

strictdoc-validate: build
	mkdir -p /tmp/medical_device_testing-strictdoc-validate
	$(STRICTDOC) export requirements --output-dir /tmp/medical_device_testing-strictdoc-validate

strictdoc-generate: build
	mkdir -p docs
	$(STRICTDOC) export requirements --output-dir docs

strictdoc-export: strictdoc-generate

strictdoc-serve: build
	$(STRICTDOC) server requirements --host 127.0.0.1 --port 5111

strictdoc-tree:
	find requirements -type f -name '*.sdoc' | sort

strictdoc-help: help
