# sc-specs — specification validation (no runtime stack)

.PHONY: help validate

help:
	@echo "sc-specs — Synaptic Four Core stack (specifications only)"
	@echo ""
	@echo "  make validate   Spectral + AsyncAPI + pytest + example schemas"
	@echo "                  (same gate as .github/workflows/validate.yml)"
	@echo ""
	@echo "No deploy targets — this repo holds API specifications."
	@echo "Start the reference server: cd ../Synaptic-Core && make up"

validate:
	./scripts/hooks/ci-check.sh
