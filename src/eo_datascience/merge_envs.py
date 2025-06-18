"""Merges all individual environment yaml files into one."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml  # type: ignore
from packaging.version import parse


def collect_yaml_files(root: Path) -> list[Path]:
    """Grab all yaml files that are in the directory."""
    files = list(root.glob("**/*.yml"))
    files.append(root.parent / "environment.yml")
    return files


def get_environment_from_yml(file: Path) -> dict:
    """Load a yaml into a dictionary."""
    with file.open("r") as f:
        return yaml.safe_load(f)


def aggregate_env_dependencies(files: list[Path]) -> tuple[list[str], list[str]]:
    """Grabs all dependencies from the yaml files and combines them into a list.

    The pip dependencies are extracted and returned separately.
    """
    unrefined_dependencies: list = []
    pip_dependencies: list = []
    for file in files:
        environment: dict = get_environment_from_yml(file)
        env_dependencies: list[str | dict] = environment.get("dependencies", [])
        regular_deps, sub_deps = extract_sub_dependencies(env_dependencies)
        unrefined_dependencies.extend(regular_deps)
        pip_dependencies.extend(sub_deps)
    return unrefined_dependencies, pip_dependencies


def extract_sub_dependencies(deps: list[str | dict]) -> tuple[list, list]:
    """Remove pip dependecies from a list of dependencies."""
    subdependencies: list = []
    regular_deps: list = []
    for dep in deps:
        if isinstance(dep, dict) and "pip" in dep:
            subdependencies.extend(dep["pip"])
        elif isinstance(dep, dict):
            # If it's a dict but not pip, we ignore it
            continue
        else:
            regular_deps.append(dep)
    return regular_deps, subdependencies


def separate_dependencies(dep: list[str]) -> tuple[set, dict]:
    """Separates all dependencies into unique and non-unique dependencies."""
    unique_deps = set()
    non_unique_deps: dict = {}
    for d in dep:
        parts = d.split("=")
        name = parts[0]
        # NOTE: All dependencies are added to the unique's
        unique_deps.add(name)
        # Check if version is specified
        if len(parts) > 1:
            version = parts[-1]
            if name in non_unique_deps:
                non_unique_deps[name].append(version)
            else:
                non_unique_deps[name] = [version]
    return unique_deps, non_unique_deps


def resolve_dependency_versions(unique_deps: set, non_unique_deps: dict) -> set:
    """Add latest versions from the non-unique to the unique dependencies."""
    final_dependencies = set()
    for name in unique_deps:
        if name in non_unique_deps:
            latest_version = max(non_unique_deps[name], key=parse)
            final_dependencies.add(f"{name}={latest_version}")
        else:
            final_dependencies.add(name)
    return final_dependencies


def resolve_versions(dep: list[str]) -> set:
    unique, non_unique = separate_dependencies(dep)

    # Update dependencies set with latest versions
    return resolve_dependency_versions(unique, non_unique)


def create_master_environment(
    final_dependencies: set,
    name: str = "eo-datascience-cookbook-dev",
    pip_deps: set[str] | None = None,
) -> dict:
    """Put a list of dependencies into the conda yaml environment format."""
    deps = sorted(final_dependencies)
    if pip_deps is not None:
        deps.append({"pip": sorted(pip_deps)})
    return {
        "name": name,
        "channels": ["conda-forge"],
        "dependencies": deps,
    }


def dump_environment(output_file: Path, master_env: dict) -> None:
    """Safe the environment dictionary as a yaml file."""
    with output_file.open("w") as f:
        yaml.dump(
            master_env,
            f,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=80,
        )


def fix_yml_indentation(output_file: Path) -> None:
    """Fix the indentation of a file, which has been yaml dumped."""
    with output_file.open() as f:
        lines = f.readlines()

    with output_file.open("w") as f:
        for line in lines:
            if line.strip().startswith("-"):
                f.write("  " + line)  # Add two spaces before the line
            else:
                f.write(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge environment files")
    parser.add_argument(
        "--out",
        type=str,
        default="environment.yml",
        help="Output file name",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the environment",
        default="eo-datascience-cookbook-dev",
    )
    args = parser.parse_args()

    root = Path("notebooks").resolve()
    files: list[Path] = collect_yaml_files(root)

    # Collect all dependencies from all YAML files
    env_dependencies: tuple[list[str], list[str]] = aggregate_env_dependencies(files)
    unrefined_dependencies, pip_dependencies = env_dependencies

    # Update dependencies set with latest versions
    final_dependencies: set = resolve_versions(unrefined_dependencies)
    final_pip_dependencies: set = resolve_versions(pip_dependencies)

    # Create master YAML file
    master_env: dict = create_master_environment(
        final_dependencies, name=args.name, pip_deps=final_pip_dependencies
    )
    dump_environment(Path(args.out), master_env)

    # Dirty fix: Read the file and add two spaces before
    fix_yml_indentation(Path(args.out))
    print("Environments have been merged.")
    print(f"{args.out} file created successfully.")


if __name__ == "__main__":
    main()
