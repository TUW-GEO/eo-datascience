.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean environment kernel teardown post-render dev

YML = $(wildcard notebooks/*.yml)
QMD = $(wildcard chapters/*.qmd)
REQ = $(basename $(notdir $(YML)))
BASENAME = $(CURDIR)

CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
CONDA_ENV_DIR := $(foreach i,$(REQ),$(shell conda info --base)/envs/$(i))
CONDA_ENV_DEV_DIR := $(shell conda info --base)/envs/eo-datascience
KERNEL_DIR := $(foreach i,$(REQ),$(shell jupyter --data-dir)/kernels/$(i))

help:
	@echo "Makefile for setting up environment, kernel, and pulling notebooks"
	@echo ""
	@echo "Usage:"
	@echo "  make environment  - Create Conda environments"
	@echo "  make kernel       - Create Conda environments and Jupyter kernels"
	@echo "  "
	@echo "  make teardown     - Remove Conda environments and Jupyter kernels"
	@echo "  make clean        - Removes ipynb_checkpoints"
	@echo "  make help         - Display this help message"

clean:
	rm --force --recursive .ipynb_checkpoints/ **/.ipynb_checkpoints/ _book/ \
		_freeze/ .quarto/ _preview/

teardown:
	$(foreach f, $(REQ), \
		$(CONDA_ACTIVATE) $(f); \
		jupyter kernelspec uninstall -y $(f); \
		conda deactivate; \
		conda remove -n $(f) --all -y ; \
		conda deactivate; )

$(CONDA_ENV_DIR): $(YML)
	- conda update -n base -c conda-forge conda -y
	$(foreach f, $^, conda env create --file $(f); )

environment: $(CONDA_ENV_DIR)
	@echo -e "conda environments are ready."

$(KERNEL_DIR): $(CONDA_ENV_DIR)
	- python -m pip install --upgrade pip
	python -m pip install jupyter
	$(foreach f, $(REQ), \
		$(CONDA_ACTIVATE) $(f); \
		python -m ipykernel install --user --name $(f) --display-name $(f); \
		conda deactivate; )

kernel: $(KERNEL_DIR)
	@echo -e "conda jupyter kernel is ready."

$(CONDA_ENV_DEV_DIR): environment.yml
	conda env create --file $^ -y

dev: $(CONDA_ENV_DEV_DIR)
	@echo -e "conda development environment is ready."

post-render: dev
	$(CONDA_ACTIVATE) eo-datascience
	nbstripout **/*.ipynb
	- mv chapters/*.ipynb notebooks/ >/dev/null 2>&1
	- $(foreach f, chapters/*.quarto_ipynb, \
			mv -- "$f" "${f%.quarto_ipynb}.ipynb" >/dev/null 2>&1; )
	cp Makefile notebooks/

preview: $(KERNEL_DIR) dev
	$(CONDA_ACTIVATE) eo-datascience
	- mkdir -p _preview/notebooks
	python -m pip install .
	wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/README.md -nc -P ./_preview
	wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/notebooks/how-to-cite.md -nc -P ./_preview/notebooks
	render_sfinx_toc ./_preview
	clean_nb ./notebooks ./_preview/notebooks
	jupyter-book build ./_preview ; jupyter-book build ./_preview