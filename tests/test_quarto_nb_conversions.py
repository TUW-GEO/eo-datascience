import nbformat
from pathlib import Path
import pytest
from eo_datascience.clean_nb import clean_up_frontmatter, convert_refs

def test_remove_front_matter():
    assert clean_up_frontmatter("./tests", False)["cells"][0]["source"] == "# This a mock Jupyter file\nWe use it for testing\n"

def test_conversion_of_refs():
    assert convert_refs("./tests", False)["cells"][1]["source"] == r'{cite}`ref1` '