#!/usr/bin/env python3
"""Create a proposal workspace from blank templates; never reuse an existing path."""
import argparse
from pathlib import Path
import shutil

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def initialize(destination):
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Refusing to overwrite existing path: {destination}')
    templates = sorted(p for p in ASSETS.iterdir() if p.is_file())
    if not templates or any(p.is_symlink() for p in templates):
        raise ValueError('Templates are missing or contain symlinks')
    destination.mkdir(parents=True, exist_ok=False)
    for source in templates:
        shutil.copy2(source, destination / source.name)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        print(initialize(args.output))
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
