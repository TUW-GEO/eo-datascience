.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean environment kernel teardown post-render dev

YML = $(wildcard notebooks/**/*.yml)
REQ := $(basename $(notdir $(YML)))
NB != find chapters -name "*.quarto_ipynb" -o  -name "*.ipynb" -not -path \
	"*/.jupyter_cache/*"
QN != git diff --cached --name-only "***.ipynb"

CONDA_ENV != conda info --base
CONDA_ACTIVATE := source $(CONDA_ENV)/etc/profile.d/conda.sh ; \
	conda activate ; conda activate
PREFIX = $(CURDIR)/.conda_envs
CONDA_ENV_DIR := $(foreach i,$(REQ),$(PREFIX)/$(i))
KERNEL_DIR != $(CONDA_ACTIVATE) eo-datascience; jupyter --data-dir
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

$(CONDA_ENV)/envs/eo-datascience:
	- conda update -n base -c conda-forge conda -y
	conda env create --file environment.yml

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

kernel: $(CONDA_ENV)/envs/eo-datascience $(CONDA_ENV_DIR) $(KERNEL_DIR)
	@echo -e "jupyter kernels are ready."

post-render:
	$(foreach f, $(NB), \
		mv $(f) "$(subst chapters,notebooks,$(subst .quarto_ipynb,.ipynb,$(f)))"; )
	cp ./Makefile ./notebooks/
	cp -r ./chapters/images ./notebooks

convert:
	$(foreach f, $(QN), \
		quarto convert $(f); \
		mv $(subst .ipynb,.qmd, $(f)) $(subst notebooks,chapters,$(subst .ipynb,.qmd,$(f))); )

preview: $(CONDA_ENV)/envs/eo-datascience $(CONDA_ENV_DIR) $(KERNEL_DIR)
	$(CONDA_ACTIVATE) $(PREFIX)/eo-datascience
	- mkdir -p _preview/notebooks
	python -m pip install .
	cp ./chapters/references.bib ./_preview/notebooks/
	cp -r ./chapters/images ./_preview/notebooks
	wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/README.md -nc -P ./_preview
	wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/_config.yml -nc -P ./_preview
	wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/notebooks/how-to-cite.md -nc -P ./_preview/notebooks
	render_sfinx_toc ./_preview
	clean_nb ./notebooks ./_preview/notebooks
	merge_envs --out environment.yml --name eo-datascience-dev
	jupyter-book build ./_preview
	jupyter-book build ./_preview

clean:
	rm --force --recursive .ipynb_checkpoints/ **/.ipynb_checkpoints/ _book/ \
		_freeze/ .quarto/ _preview/ ./pytest_cache ./**/**/**/.jupyter_cache \
		./**/**/.jupyter_cache

teardown:
	conda remove -n $(PREFIX)/eo-datascience --all -y
	$(foreach f, $(REQ), \
		$(CONDA_ACTIVATE) $(PREFIX)/$(f); \
		jupyter kernelspec uninstall -y $(f); \
		conda deactivate; \
		conda remove --prefix $(PREFIX)/$(f) --all -y ; \
		conda deactivate; )

master:
	python -m pip install .
	merge_envs --out environment.yml --name eo-datascience-dev
