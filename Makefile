.DEFAULT_GOAL := help

UV ?= uv
NPM ?= npm
SOURCE ?= ../telegram-bot-api
REF ?= HEAD
SNAPSHOT ?= .cache/upstream-next.json
BASELINE ?= catalogue/upstream.json
REPORT ?= .cache/upstream-diff.json
LIVE_REPORT ?= .cache/live/report.json
LIVE_ARGS ?=

.PHONY: help setup generate check-generated validate lint test test-python test-js check build check-packages upstream-scan upstream-diff live-check docs-build docs-check docs-dev docs-browser-setup docs-browser-test

help:
	@printf '%s\n' \
	  'make setup          Install locked development dependencies' \
	  'make generate       Regenerate bindings and catalogue docs' \
	  'make check          Validate, check generation, lint, and test' \
	  'make build          Build Python and npm distributions' \
	  'make check-packages Test built packages in clean environments' \
	  'make docs-dev       Preview the documentation while editing' \
	  'make docs-check     Build and validate the documentation' \
	  'make docs-browser-setup Install Chromium for browser tests' \
	  'make docs-browser-test Check search and navigation in Chromium' \
	  'make upstream-scan  Scan SOURCE at REF into SNAPSHOT' \
	  'make upstream-diff  Compare BASELINE with SNAPSHOT' \
	  'make live-check     Run optional Bot API checks with test credentials'

setup:
	$(UV) sync --locked --all-extras
	$(NPM) --prefix js ci --no-audit --no-fund
	$(NPM) --prefix site ci --no-audit --no-fund

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

check: validate check-generated lint test docs-check

build: check-generated
	$(UV) build --out-dir dist
	$(NPM) --prefix js run build
	cd js && $(NPM) pack --ignore-scripts --pack-destination ../dist

check-packages:
	$(UV) run --locked python tools/smoke_packages.py

docs-build: check-generated
	$(NPM) --prefix site run check
	$(NPM) --prefix site run build

docs-check: docs-build
	$(UV) run --locked python tools/check_site.py

docs-dev: generate
	$(NPM) --prefix site run dev

docs-browser-setup:
	cd site && $(NPM) exec -- playwright install chromium

docs-browser-test: docs-build
	$(NPM) --prefix site run test:e2e

upstream-scan:
	$(UV) run --locked python tools/upstream.py scan --source "$(SOURCE)" --ref "$(REF)" --output "$(SNAPSHOT)"

upstream-diff:
	$(UV) run --locked python tools/upstream.py diff "$(BASELINE)" "$(SNAPSHOT)" --output "$(REPORT)"

live-check:
	$(UV) run --locked python tools/live_checks.py --output "$(LIVE_REPORT)" $(LIVE_ARGS)
