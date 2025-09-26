import argparse
from pathlib import Path

from eo_datascience.render_sfinx_toc import render_toc
from eo_datascience.clean_nb import clean_nb
from eo_datascience.merge_envs import merge_envs


def main():
    parser = argparse.ArgumentParser(description="Convert Quarto to Jupyter Book")
    parser.add_argument("--out", type=str, help="Destination directory")
    parser.add_argument(
        "--dir",
        type=str,
        help="Input Directory",
        default=str(Path("notebooks").absolute().as_posix()),
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the environment",
        default="eo-datascience-cookbook",
    )
    args = parser.parse_args()
    render_toc(p=Path("_quarto.yml").absolute().as_posix(), out=args.out)
    clean_nb(args.dir, Path(args.out) / Path("notebooks"))
    merge_envs(args.name, Path(args.out))


if __name__ == "__main__":
    main()
