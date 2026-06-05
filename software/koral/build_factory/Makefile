# Koral Image Build Factory Makefile
# For Intel SGXv2 clients (Defaulting to non-secure execution with strict warnings)

SHELL := /usr/bin/bash
ENTITY ?= desertmonitor
.DEFAULT_GOAL := help

.PHONY: help build-all clean warn-security

help:
	@echo "Koral Build Factory CLI"
	@echo "Available commands:"
	@echo "  build-all       - Stitches base Koral Image and Patches using daemonless surgery"
	@echo "  clean           - Cleans up local build outputs and temporary layers"

warn-security:
	@echo "================================================================================"
	@echo "⚠️  SECURITY WARNING: UNSECURE SIGNING & EXECUTION RUNTIME IN USE"
	@echo "--------------------------------------------------------------------------------"
	@echo "Current environment lacks confidential hypervisor support (Intel TDX / SEV-SNP)."
	@echo "Falling back to non-secure execution on Intel SGXv2 host."
	@echo "Signing key material is exposed to the local host during build runtime."
	@echo "THIS BUILD MUST ONLY BE USED FOR LOCAL TESTING AND DEVELOPMENT PURPOSES!"
	@echo "================================================================================"
	@echo ""

build-all: warn-security synthesis-dev

synthesis-dev: warn-security
	@chmod +x scripts/koral_synthesis.sh
	@KORAL_ENV=dev ./scripts/koral_synthesis.sh --entity $(ENTITY)

synthesis-prod:
	@chmod +x scripts/koral_synthesis.sh
	@KORAL_ENV=prod ./scripts/koral_synthesis.sh --entity $(ENTITY)

clean:
	@echo "Cleaning Koral build workspace..."
	@rm -rf build_out/ tmp_layers/

