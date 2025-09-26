#! /bin/bash


COPY_DIRS=$(find notebooks -type d -name "images" -o -name "src")

for dir in $COPY_DIRS; do
    cp -rf --parents $dir ./${1}
done

COPY_FILES=$(find notebooks -type f -name "references.bib" -o -name "pyproject.toml" -o -iname ".env")

for file in $COPY_FILES; do
    cp -rf --parents $file ./${1}
done
