.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean teardown convert

YML != find notebooks -type f \( -iname "*.yml" ! -iname "_*" \)
REQ := $(basename $(notdir $(YML)))
NB != find chapters -name "*.quarto_ipynb" -o  -name "*.ipynb" -not -path \
	"*/.jupyter_cache/*"
QN != find chapters notebooks -name "*.ipynb" -not -path "*/.jupyter_cache/*" -not -path */.ipynb_checkpoints/*

CONDA_ENV != conda info --base
CONDA_ACTIVATE := source $(CONDA_ENV)/etc/profile.d/conda.sh ; \
	conda activate ; conda activate
PREFIX = $(CURDIR)/.conda_envs
CONDA_ENV_DIR := $(foreach i,$(REQ),$(PREFIX)/$(i))
KERNEL_DIR != jupyter --data-dir
KERNEL_DIR := $(foreach i,$(REQ),$(KERNEL_DIR)/kernels/$(i))

help:
	@echo "Makefile for setting up environment, kernel, and rendering  book"
	@echo ""
	@echo "Usage:"
	@echo "  make environment  - Create Conda environments"
	@echo "  make kernel       - Create Conda environments and Jupyter kernels"
	@echo "  make post-render  - Post-render Quarto book"
	@echo "  make preview      - Preview Jupyter Book"
	@echo "  make convert      - Convert Jupyter notebooks to Quarto notebooks"
	@echo "  "
	@echo "  make teardown     - Remove Conda environments and Jupyter kernels"
	@echo "  make clean        - Removes ipynb_checkpoints and quarto \
		temporary files"
	@echo "  make help         - Display this help message"

$(CONDA_ENV_DIR):
	$(foreach f, $(YML), \
		conda env create --file $(f) \
			--prefix $(PREFIX)/$(basename $(notdir $(f))); )

environment: $(CONDA_ENV_DIR)
	@echo -e "conda environments are ready."

$(KERNEL_DIR):
	$(foreach f, $(REQ), \
		$(CONDA_ACTIVATE) $(PREFIX)/$(f); \
		python -m ipykernel install --user --name $(f) --display-name $(f); \
			conda deactivate; )

kernel: $(CONDA_ENV_DIR) $(KERNEL_DIR)
	@echo -e "jupyter kernels are ready."

convert:
	./convert-quarto.sh && pre-commit run --all-files

preview:
	python -m pip install .
	./preview-pythia.sh _preview
	cd _preview && pre-commit run --all-files
	conda env create --file environment.yml --prefix $(PREFIX)/eo-datascience-cookbook
	$(CONDA_ACTIVATE) $(PREFIX)/eo-datascience-cookbook
	jupyter-book build .
	jupyter-book build .

clean:
	rm --force --recursive .ipynb_checkpoints/ **/.ipynb_checkpoints/ _book/ \
		_freeze/ .quarto/ _preview/ ./pytest_cache ./**/**/**/.jupyter_cache \
		./**/**/.jupyter_cache *.quarto_ipynb **/*.quarto_ipynb \
		**/**/*.quarto_ipynb **/__pycache__ **/**/__pycache__ __pycache__

teardown:
	$(foreach f, $(REQ), \
		$(CONDA_ACTIVATE) $(PREFIX)/$(f); \
		jupyter kernelspec uninstall -y $(f); \
		conda deactivate; \
		conda remove --prefix $(PREFIX)/$(f) --all -y ; \
		conda deactivate; )
