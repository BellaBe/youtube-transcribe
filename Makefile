URL := $(lastword $(MAKECMDGOALS))

.PHONY: install transcript clean

install:
	poetry install

# Default values for configurable parameters
OUTPUT_DIR ?= output
MAX_RETRIES ?= 3
PARALLEL ?= 5
VERBOSE ?= 1

transcript:
ifndef URL
	$(error You must provide a URL. Usage: make transcript URL="https://www.youtube.com/watch?v=...")
endif
	@echo "Fetching transcript with the following configuration:"
	@echo "URL=$(URL)"
	@echo "OUTPUT_DIR=$(OUTPUT_DIR)"
	@echo "VERBOSE=$(VERBOSE)"
	@echo "MAX_RETRIES=$(MAX_RETRIES)"
	@echo "PARALLEL=$(PARALLEL)"

	poetry run python src/main.py "$(URL)" \
		--output-dir "$(OUTPUT_DIR)" \
		$(if $(VERBOSE),--verbose,) \
		--max-retries $(MAX_RETRIES) \
		--parallel $(PARALLEL)

clean:
	@echo "Cleaning output directory: $(OUTPUT_DIR)"
	rm -rf "$(OUTPUT_DIR)"

# Prevent make from treating the URL as a target
%:
	@:
