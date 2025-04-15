#! /bin/bash

FILES=$(git diff --cached --name-only -- 'notebooks/*.ipynb' || true)

for file in $FILES; do
    NEW_PATH=$(echo $file | sed 's|notebooks|chapters|' | sed 's|ipynb|qmd|')
    quarto convert "$file" --output $NEW_PATH
done
