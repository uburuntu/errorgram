.DEFAULT_GOAL := help

UV ?= uv
NPM ?= npm
SOURCE ?= ../telegram-bot-api
REF ?= HEAD
SNAPSHOT ?= .cache/upstream-next.json
BASELINE ?= catalogue/upstream.json
REPORT ?= .cache/upstream-diff.json

.PHONY: help setup generate check-generated validate lint test test-python test-js check build check-packages upstream-scan upstream-diff

help:
	@printf '%s\n' \
	  'make setup          Install locked development dependencies' \
	  'make generate       Regenerate bindings and catalogue docs' \
	  'make check          Validate, check generation, lint, and test' \
	  'make build          Build Python and npm distributions' \
	  'make check-packages Test built packages in clean environments' \
	  'make upstream-scan  Scan SOURCE at REF into SNAPSHOT' \
	  'make upstream-diff  Compare BASELINE with SNAPSHOT'

setup:
	$(UV) sync --locked --all-extras
	$(NPM) --prefix js ci --no-audit --no-fund

generate:
	$(UV) run --locked python tools/generate.py

check-generated:
	$(UV) run --locked python tools/generate.py --check

validate:
	$(UV) run --locked python tools/validate.py

lint:
	$(UV) run --locked ruff check python tools tests

test-python:
	$(UV) run --locked python -m pytest

test-js:
	$(NPM) --prefix js test

test: test-python test-js

check: validate check-generated lint test

build: check-generated
	$(UV) build --out-dir dist
	$(NPM) --prefix js run build
	cd js && $(NPM) pack --ignore-scripts --pack-destination ../dist

check-packages:
	$(UV) run --locked python tools/smoke_packages.py

upstream-scan:
	$(UV) run --locked python tools/upstream.py scan --source "$(SOURCE)" --ref "$(REF)" --output "$(SNAPSHOT)"

upstream-diff:
	$(UV) run --locked python tools/upstream.py diff "$(BASELINE)" "$(SNAPSHOT)" --output "$(REPORT)"
