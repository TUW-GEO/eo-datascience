import nbformat
from pathlib import Path
import pytest
from eo_datascience.clean_nb import clean_up_frontmatter, convert_refs, quarto_ref_person_replace, quarto_ref_time_replace, convert_callout_notes

def test_remove_front_matter():
    assert clean_up_frontmatter("./tests", False)["cells"][0]["source"] == "# This a mock Jupyter file\nWe use it for testing\n"

def test_ref_regex():
    quarto = [r"lorem ipsum [@anon2024] and [@anon2025]", r"lorem ipsum @anon2024 and @anon2025"]
    quarto[0] = quarto_ref_person_replace(quarto[0])
    quarto[1] = quarto_ref_time_replace(quarto[1])
    assert quarto == [r"lorem ipsum {cite:p}`anon2024` and {cite:p}`anon2025`", r"lorem ipsum {cite:t}`anon2024` and {cite:t}`anon2025`"]

def test_conversion_of_refs():
    assert convert_refs("./tests", False)["cells"][1]["source"] == r"lorem ipsum {cite:p}`anon2024` and {cite:p}`anon2025` and lorem ipsum {cite:t}`anon2024` and {cite:t}`anon2025`"

def test_conversion_of_callout_notes():
    convert_callout_notes("./tests", False)
