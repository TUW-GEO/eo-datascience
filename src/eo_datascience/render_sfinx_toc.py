import argparse
from pathlib import Path

import yaml
from eo_datascience.clean_nb import substitute_path


def render_toc(p, out="."):
    with open(p, "r") as ff:
        quarto_toc = yaml.safe_load(ff)
    toc = _render_toc(quarto_toc)
    with open((Path(out) / "_toc.yml").resolve().as_posix(), "w+") as ff:
        yaml.dump(toc, ff)


def _render_toc(toc):
    ls = [dict(caption="Preamble", chapters=[dict(file="notebooks/how-to-cite")])]
    ls += [transform_main(toc)] + transform_appendix(toc)
    ls += [dict(caption="References", chapters=[dict(file="notebooks/references")])]
    return dict(format="jb-book", root="README", parts=ls)


def extract_main(toc):
    return toc["book"]["chapters"][1:]


def extract_appendix(toc):
    return toc["book"]["appendices"][:-1]


def transform_main(toc):
    return rename_keys_sections_main(extract_main(toc))


def transform_appendix(toc):
    return rename_keys_sections_appendix(extract_appendix(toc))


def rename_keys_sections_main(sections):
    sections = sections.copy()
    list_of_chapters_files = []
    new_struct_toc = dict()
    for i, section in enumerate(sections):
        sections[i] = _rename_keys_section(section, ("part", "caption"))
        restructure_section_main(sections, i, list_of_chapters_files)
    new_struct_toc["caption"] = "Courses"
    new_struct_toc["chapters"] = list_of_chapters_files
    return new_struct_toc


def rename_keys_sections_appendix(sections):
    sections = sections.copy()
    for i, section in enumerate(sections):
        sections[i] = _rename_keys_section(section, ("part", "caption"))
        restructure_section_appendix(sections, i)
    return sections


def restructure_section_main(sections, i, list_of_chapters_files):
    return list_of_chapters_files.append(
        {
            "file": sections[i]["caption"][0]["file"],
            "sections": sections[i]["chapters"],
        }
    )


def restructure_section_appendix(sections, i):
    restruct = [
        {
            "file": sections[i]["caption"][0]["file"],
            "sections": sections[i]["chapters"],
        }
    ]
    name = sections[i]["caption"][0]["file"].split("/")[1]
    sections[i]["chapters"] = restruct
    sections[i]["caption"] = name.capitalize()


def _rename_keys_section(section, key_rename):
    keys = [i.replace(*key_rename) for i in section.keys()]
    section = dict(zip(keys, section.values()))

    for key in section.keys():
        try:
            file_path = section[key]
            if not isinstance(file_path, list):
                file_path = [file_path]
            section[key] = [{"file": rename_file_path(i)} for i in file_path]
        except KeyError:
            pass
    return section


def rename_file_path(file_path):
    if Path(file_path).exists():
        file_path = str(
            substitute_path(file_path, "chapters", "notebooks").with_suffix("")
        )
    return file_path


def main():
    parser = argparse.ArgumentParser(description="Convert Quarto to Jupyter Book")
    parser.add_argument("out", type=str, help="Destination directory")
    args = parser.parse_args()
    render_toc(p=Path("_quarto.yml").absolute().as_posix(), out=args.out)


if __name__ == "__main__":
    main()
