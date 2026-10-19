#!/usr/bin/env python3
"""Copy complete, independent skills. Existing destinations are never overwritten."""
import argparse
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def available():
    return {p.name: p for p in sorted((ROOT / 'skills').iterdir())
            if p.is_dir() and not p.is_symlink() and (p / 'SKILL.md').is_file()}


def install(names, destination, dry_run=False):
    catalog = available()
    names = list(dict.fromkeys(names))
    unknown = set(names) - set(catalog)
    if unknown:
        raise ValueError('Unknown skills: ' + ', '.join(sorted(unknown)))
    destination = Path(destination).expanduser().resolve()
    targets = [(catalog[name], destination / name) for name in names]
    for source, target in targets:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f'Refusing to overwrite: {target}')
        if any(p.is_symlink() for p in source.rglob('*')):
            raise ValueError(f'Symlinks are not supported: {source}')
        if source == destination or source in destination.parents:
            raise ValueError('Destination must not be inside a source skill')
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for source, target in targets:
            shutil.copytree(source, target,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    return [str(target) for _, target in targets]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--all', action='store_true')
    group.add_argument('--skill', action='append', help='Repeat to select several skills')
    default_root = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    parser.add_argument('--dest', type=Path, default=default_root / 'skills')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.list:
        print('\n'.join(available()))
        return
    try:
        targets = install(list(available()) if args.all else args.skill,
                          args.dest, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')
    print(('Would install:\n' if args.dry_run else 'Installed:\n') + '\n'.join(targets))


if __name__ == '__main__':
    main()
