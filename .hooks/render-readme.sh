#!/bin/bash
# Render README.qmd to README.md using Quarto
if [ -f README.qmd ]; then
    echo "Rendering README.qmd to README.md..."
    quarto render README.qmd --to markdown
else
    echo "README.qmd not found. Skipping rendering."
fi
