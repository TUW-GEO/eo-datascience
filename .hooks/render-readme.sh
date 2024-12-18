#!/bin/bash

# Check if README.qmd has been modified
if git diff --cached --name-only | grep -q "^README\.qmd$"; then
    echo "README.qmd has been modified. Rendering README.md..."
    if quarto render README.qmd --to markdown; then
        # Stage the updated README.md
        git add README.md
    else
        echo "Failed to render README.qmd. Commit aborted."
        exit 1
    fi
else
    echo "README.qmd has not been modified. Skipping rendering."
fi