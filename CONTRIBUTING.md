# Contributing

Thanks for your interest in contributing to this project! Please take a moment to review the following guidelines before submitting a pull request.

## How this project is organized

This repository is connected to the [Pythia Cookbook](https://github.com/ProjectPythia/eo-datascience-cookbook), where the notebooks are rendered into a website. The quarto notebooks from this repository are converted into jupyter notebooks and these are then pushed to the other repository. The notebooks are then rendered into a website using the Jupyter Book.

The entrypoint for new content is therfore in the chapters directory, where the quarto notebooks are stored. There are at the time beeing 3 sections to the book:

- **Courses** which is dedicated to notebooks from courses from TU Wien
- **Templates** which is dedicated to notebooks that can be used starting points for new projects
- **Tutorials** which is dedicated to notebooks that are tutorials on how to use the products developed by TU Wien.

## Ground Rules

Please **ask first** before starting work on any significant new features or notebooks. This will help avoid wasted effort on both sides.

Make sure your code is running and tested before submitting a pull request.

Use the `pre-commit` hooks to ensure your code is formatted correctly.

If you are submitting a **new notebook**, please make sure it is done in the Quarto `.qmd` format. This makes the source code more readable. Also provide a environment `env.yml` file which lists
the minimal dependencies required to run the notebook.

If you are submitting something other than a notebook, please make sure it is well documented and tested.
Also make sure that the `pre-commit` hooks are running correctly.

## How Can I Contribute?

- Start of by **forking** this repository and **cloning** it to your local machine.
- Next create a descriptive **branch** for your changes.
- Read the [developing setup](#setting-up-for-developing) to make sure you have the necessary tools installed.
- Make your changes and **test** them.
- Make sure your code is formatted correctly. If you are submitting a notebook, make sure that the desired output is achieved by running the preview (`make preview`).
- Push your changes to your fork and **submit a pull request** to the main repository.

## Pull Requests

Fill out the pull request template with as much detail as possible. This will help the maintainers understand the changes you are proposing.

## Setting up for developing

The pre-commit hooks can be used to check if the outputs of your notebooks are empty and the code is formatted correctly. To install the pre-commit hooks, run

```bash
pip install pre-commit
pre-commit install
```

Furthermore use the provided `Makefile` to:

- **preview** the notebook in Pythia Style with: `make preview`
- **setup** the environment with the necessary dependencies: `make environment`
- **convert** the notebooks with: `make convert`
- **clean** the repository with: `make clean`
