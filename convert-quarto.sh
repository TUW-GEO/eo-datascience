#! /bin/bash


FILES_SUB=$(git submodule foreach --quiet '
  for file in $(git diff --name-only --cached | grep "\.ipynb$"); do
    echo "$name/$file"
  done
  for file in $(git diff --name-only | grep "\.ipynb$"); do
    echo "$name/$file"
  done
'|| true)

FILES=$(git diff --name-only -- '*.ipynb'; git diff --cached --name-only -- '*.ipynb' || true)

FILES=("${FILES_SUB[@]} ${FILES[@]}")

for file in $FILES; do
    NEW_PATH=$(echo $file | sed 's|notebooks|chapters|' | sed 's|ipynb|qmd|')
    quarto convert "$file" --output $NEW_PATH
done
