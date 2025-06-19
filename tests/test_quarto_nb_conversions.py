import re
from pathlib import Path

import nbformat  # noqa
import pytest  # noqa
import yaml
from eo_datascience.clean_nb import (
    clean_up_frontmatter,
    convert_callout_notes,
    convert_refs,
    find_ipynb,
    quarto_note_replace,
    quarto_ref_person_replace,
    quarto_ref_time_replace,
    set_kernel_all_notebooks,
    substitute_path,
)
from eo_datascience.render_sfinx_toc import (
    _render_toc,
    extract_appendix,
    extract_main,
    rename_file_path,
    rename_keys_sections_appendix,
    rename_keys_sections_main,
    transform_appendix,
    transform_main,
)


def test_toc_conversion():
    mock_quarto_toc = """
    project:
      type: book
      pre-render:
        - make kernel
      post-render:
        - quarto convert chapters/references.qmd
        - make post-render

    book:
      title: "Earth Observation Datascience"
      author: ""
      date: "10 January 2025"
      chapters:
        - index.qmd
        - part: chapters/courses/microwave-remote-sensing.qmd
          chapters:
            - chapters/courses/microwave-remote-sensing/unit_01/01_in_class_exercise.qmd
            - chapters/courses/microwave-remote-sensing/unit_01/02_in_class_exercise.qmd
        - part: chapters/courses/environmental-remote-sensing.qmd
          chapters:
            - chapters/courses/environmental-remote-sensing/mozambique-droughts.qmd
      appendices:
        - part: chapters/templates/prereqs-templates.qmd
          chapters:
            - chapters/templates/classification.qmd
        - part: chapters/tutorials/prereqs-tutorials.qmd
          chapters:
            - chapters/tutorials/floodmapping.qmd
        - chapters/references.qmd
    """

    mock_jb_toc = """
    format: jb-book
    root: README
    parts:
    - caption: Preamble
      chapters:
        - file: notebooks/how-to-cite
    - caption: Courses
      chapters:
      - file: notebooks/courses/microwave-remote-sensing
        sections:
          - file: notebooks/courses/microwave-remote-sensing/unit_01/01_in_class_exercise
          - file: notebooks/courses/microwave-remote-sensing/unit_01/02_in_class_exercise
      - file: notebooks/courses/environmental-remote-sensing
        sections:
          - file: notebooks/courses/environmental-remote-sensing/mozambique-droughts
    - caption: Templates
      chapters:
      - file: notebooks/templates/prereqs-templates
        sections:
          - file: notebooks/templates/classification
    - caption: Tutorials
      chapters:
      - file: notebooks/tutorials/prereqs-tutorials
        sections:
          - file: notebooks/tutorials/floodmapping
    - caption: References
      chapters:
        - file: notebooks/references
    """

    quarto_toc = yaml.safe_load(mock_quarto_toc)

    main = extract_main(quarto_toc)
    assert len(main) == 2
    assert rename_file_path("tests/mock.qmd") == "tests/mock"

    ref_main_dict = {
        "caption": "Courses",
        "chapters": [
            {
                "file": "notebooks/courses/microwave-remote-sensing",
                "sections": [
                    {
                        "file": "notebooks/courses/microwave-remote-"
                        + "sensing/unit_01/01_in_class_exercise"
                    },
                    {
                        "file": "notebooks/courses/microwave-remote-"
                        + "sensing/unit_01/02_in_class_exercise"
                    },
                ],
            },
            {
                "file": "notebooks/courses/environmental-remote-sensing",
                "sections": [
                    {
                        "file": "notebooks/courses/environmental-remote-"
                        + "sensing/mozambique-droughts"
                    },
                ],
            },
        ],
    }

    assert rename_keys_sections_main(main) == ref_main_dict

    append = extract_appendix(quarto_toc)
    assert len(append) == 2

    ref_appendix_dict = [
        {
            "caption": "Templates",
            "chapters": [
                {
                    "file": "notebooks/templates/prereqs-templates",
                    "sections": [{"file": "notebooks/templates/classification"}],
                }
            ],
        },
        {
            "caption": "Tutorials",
            "chapters": [
                {
                    "file": "notebooks/tutorials/prereqs-tutorials",
                    "sections": [{"file": "notebooks/tutorials/floodmapping"}],
                }
            ],
        },
    ]

    assert rename_keys_sections_appendix(append) == ref_appendix_dict

    quarto_toc_transform = transform_main(quarto_toc)
    assert len(main) == len(quarto_toc_transform)

    quarto_toc_transform = transform_appendix(quarto_toc)
    assert len(append) == len(quarto_toc_transform)

    assert _render_toc(quarto_toc) == yaml.safe_load(mock_jb_toc)


def test_remove_front_matter():
    assert (
        clean_up_frontmatter("./tests", None, False)["cells"][0]["cell_type"]
        == "markdown"
    )
    incoming = clean_up_frontmatter("./tests", None, False)["cells"][0]["source"][:52]
    ref = r"# This a mock Jupyter file\n\*\*We use it for testing\*\*"
    assert re.match(ref, incoming)


def test_find_ipynb():
    assert find_ipynb("tests")[0].stem == "mock"


def test_substitute_path():
    nb_path = find_ipynb("tests")[0]
    assert substitute_path(nb_path, "./tests", "./tests/tests") == Path(
        "./tests/tests/mock.ipynb"
    )
    assert substitute_path(nb_path, "./tests", None) == Path("./tests/mock.ipynb")


def test_conversion_of_refs():
    quarto = [
        r"lorem ipsum [@anon2024] and [@anon2025]",
        r"lorem ipsum @anon2024 and @anon2025",
    ]
    quarto[0] = quarto_ref_person_replace(quarto[0])
    quarto[1] = quarto_ref_time_replace(quarto[1])
    assert quarto == [
        r"lorem ipsum {cite:p}`anon2024` and {cite:p}`anon2025`",
        r"lorem ipsum {cite:t}`anon2024` and {cite:t}`anon2025`",
    ]
    incoming = convert_refs("./tests", None, False)["cells"][0]["source"][245:]
    ref = r"lorem ipsum {cite:p}`anon2024` and {cite:p}`anon2025` and lorem ipsum {cite:t}`anon2024` and {cite:t}`anon2025`\n"
    assert re.match(ref, incoming)


def test_conversion_of_callout_notes():
    ref = r":::{note}\nThis a callout note.\n:::"
    incoming = quarto_note_replace(r"::: {.callout-note}\nThis a callout note.\n:::")
    assert re.match(ref, incoming)
    ref = convert_callout_notes("./tests", None, False)["cells"][0]["source"][199:233]
    assert re.match(ref, incoming)


def test_setting_kernelspec():
    meta_mock_nb = nbformat.read("tests/mock.ipynb", as_version=4).metadata
    kernel_display_name_mock_nb = meta_mock_nb.kernelspec.display_name
    kernel_name_mock_nb = meta_mock_nb.kernelspec.name
    new_meta_mock_nb = set_kernel_all_notebooks(dir="tests", save=False).metadata
    assert kernel_display_name_mock_nb != new_meta_mock_nb.kernelspec.display_name
    assert kernel_name_mock_nb != new_meta_mock_nb.kernelspec.name
