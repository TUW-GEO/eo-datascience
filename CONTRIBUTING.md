# Contributing

Thanks for your interest in contributing to this project! Please take a
moment to review the following guidelines before submitting a pull
request. We accept contributions in the following forms:

- Reporting a Bug
- Submitting a Fix
- Discussing the current state of the code
- Proposing or Submitting new content

## Environment management

For convenience one can install the top level conda environment
(`environment.yml`).

```bash
conda create env --file environment.yml
conda activate eo-datascience
```

This environment contains all the tools needed for development.

## How this project is organized

This repository is connected to the [Project Pythia EO Data Science
Cookbook](https://github.com/ProjectPythia/eo-datascience-cookbook),
where the notebooks are rendered into a Jupyter Book. The Jupyter
notebooks from this repository are reformatted to comply with Jupyter
Book prerequisites and these are then pushed to the other repository.

> ![](assets/cookbook.png) A conceptual overview of the linked
> repositories and how new content can be added.

### Notebooks

The entrypoint for new content is therefore in the `notebooks`
directory, where the Jupyter notebooks are stored. Use the [notebook
template](https://github.com/TUW-GEO/eo-datascience/tree/0a455daf92f034795a6005549a3b04b1d787393b/assets/template.ipynb)
as a starting point and replace the `<ENTER TITLE>` and
`<ENTER KERNEl NAME>` with the notebook’s title and Jupyter kernel’s
name, respectively.

There are currently 3 sections to the book:

- **Courses** which is dedicated to notebooks from courses from TU Wien
- **Templates** which is dedicated to notebooks that can be used
  starting points for new projects
- **Tutorials** which is dedicated to notebooks that are tutorials on
  how to use the products developed by TU Wien.

Place new content in the appropriate section. Run the pre-commit hooks
by commiting the files or run without commiting.

```bash
pre-commit run --all-files
```

This will automatically format the code and convert all Jupyter
notebooks to Quarto equivalents.

### Data

If you notebook requires data, you need to be able to access the data
from an external repository over the internet (e.g. STAC or a
HuggingFace Repository). If this condition cannot be met, then the
notebook can still be included in the repository but not in the book.

### Book

As a last step, make sure to adapt the `_quarto.yml` file to include the
new content, so that it is visible in both the Quarto and Pythia books.

## Ground Rules

Please **ask first** before starting work on any significant new
features or notebooks. This will help avoid wasted effort on both sides.

Make sure your code is running and tested before submitting a pull
request.

Use the `pre-commit` hooks to ensure your code is formatted correctly.

If you are submitting a **new notebook**, please make sure it is done in
Jupyter `.ipynb` and the Quarto `.qmd` format. The latter makes the
source code more readable in a GitHub PR. Also provide a environment
`<environment>.yml` file which lists the minimal dependencies required
to run the notebook. Follow the [yaml
template](https://github.com/TUW-GEO/eo-datascience/tree/0a455daf92f034795a6005549a3b04b1d787393b/assets/template.yml)
and replace `<ENTER KERNEl NAME>` with the same name as used in the
accompanying notebook.

If you are submitting something other than a notebook, please make sure
it is well documented and tested. Also make sure that the `pre-commit`
hooks are running correctly.

## How Can I Contribute?

- Start of by **forking** this repository and **cloning** it to your
  local machine.
- Next create a descriptive **branch** for your changes.
- Read the [developing setup](#setting-up-for-developing) to make sure
  you have the necessary tools installed.
- Make your changes and **test** them.
- Make sure your code is formatted correctly. If you are submitting a
  notebook, make sure that the desired output is achieved by running the
  preview (`make preview`).
- Push your changes to your fork and **submit a pull request** to the
  main repository.

If you want to add new content to the cookbook, provide the `.ipynb` and `.qmd`
files, as well as the `<environment>.yml` file. Give the environment file a name
that is descriptive of the content of the notebook.

## Pull Requests

Fill out the pull request template with as much detail as possible. This
will help the maintainers understand the changes you are proposing.

## Development

### Environment management

For developing the notebooks, we recommend using `conda` to manage the
environment. We store all the dependencies as `.yml` files in the
notebooks directory.

In order to create an environment from a `.yml` file, run

```bash
conda env create -f <env.yml>
```

You also have the possibility to install all available environments by
running

```bash
make environment
```

### Linting and formatting

The pre-commit hooks can be used to check if the outputs of your
notebooks are empty and the code is formatted correctly. To install the
pre-commit hooks, run

```bash
pip install pre-commit
pre-commit install
```

### Task runner

Furthermore use the provided `Makefile` to:

- **preview** the notebook in Pythia Style (optional): `make preview`
- **setup** the environments with the necessary dependencies:
  `make environment`
- **install** the kernels to the environments: `make kernel`
- **convert** the notebooks: `make convert`
- **clean** the repository: `make clean`
