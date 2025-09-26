#! /bin/bash

wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/README.md -nc -P ./${1}
wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/_config.yml -nc -P ./${1}
wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/.pre-commit-config.yaml -nc -P ./${1}
wget https://raw.githubusercontent.com/TUW-GEO/eo-datascience-cookbook/refs/heads/main/notebooks/how-to-cite.md -nc -P ./${1}/notebooks
