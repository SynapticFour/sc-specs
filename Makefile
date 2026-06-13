# sc-specs — specification validation (no runtime stack)

.PHONY: help validate

help:
	@echo "sc-specs — Synaptic Four Core stack (specifications only)"
	@echo ""
	@echo "  make validate   Validate OpenAPI examples and spec consistency"
	@echo ""
	@echo "No deploy targets — this repo holds API specifications."
	@echo "Start the reference server: cd ../Synaptic-Core && make up"

validate:
	python3 scripts/validate_examples.py
