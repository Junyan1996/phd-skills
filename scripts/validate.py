#!/usr/bin/env python3
"""Validate this collection's quoted YAML subset, local links and resource portability.

This is a package check, not a general YAML parser or scientific validation engine.
"""
import csv
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path):
    content = path.read_text(encoding='utf-8')
    parts = content.split('---', 2)
    if len(parts) != 3 or parts[0] != '':
        raise ValueError('Missing frontmatter')
    fields = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.startswith(' '):
            continue
        key, value = line.split(':', 1)
        value = value.strip()
        fields[key] = json.loads(value) if value.startswith('"') else value
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', fields.get('name', '')):
        raise ValueError('Invalid skill name')
    if len(fields['name']) >= 64 or fields['name'] != path.parent.name:
        raise ValueError('Name/folder mismatch or overly long name')
    description = fields.get('description')
    if not isinstance(description, str) or not description or len(description) > 1024:
        raise ValueError('Missing or overly long description')
    return fields


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []
    skill_files = sorted((root / 'skills').glob('*/SKILL.md'))
    if not skill_files:
        errors.append('No skills discovered')
    for path in skill_files:
        try:
            frontmatter(path)
            ui = (path.parent / 'agents' / 'openai.yaml').read_text(encoding='utf-8')
            if '$' + path.parent.name not in ui:
                errors.append(f'{path}: default_prompt does not invoke the skill')
        except (OSError, ValueError) as error:
            errors.append(f'{path}: {error}')
        for resource in path.parent.rglob('*'):
            if resource.is_symlink():
                errors.append(f'{resource}: symlink is not portable')
    for path in root.rglob('*'):
        if not path.is_file() or any(p in {'.git', '.build', '.publish', '__pycache__'} for p in path.parts):
            continue
        if path.suffix == '.md':
            content = path.read_text(encoding='utf-8')
            # Only inspect Markdown links, not code literals or prose paths.
            for target in re.findall(r'\]\(([^)]+)\)', content):
                target = target.strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith('#'):
                    continue
                local = (path.parent / unquote(parsed.path)).resolve()
                if local != root and root not in local.parents:
                    errors.append(f'{path}: link escapes package: {target}')
                elif not local.exists():
                    errors.append(f'{path}: missing link: {target}')
                elif 'skills' in path.relative_to(root).parts:
                    owner = root / 'skills' / path.relative_to(root).parts[1]
                    if local != owner and owner not in local.parents:
                        errors.append(f'{path}: cross-skill resource dependency: {target}')
            if re.search(r'[A-Z]:[\\/](?:Users|Program Files)[\\/]', content):
                errors.append(f'{path}: machine-specific path')
        elif path.suffix == '.csv':
            with path.open(encoding='utf-8', newline='') as stream:
                rows = list(csv.reader(stream))
            if not rows or len(set(rows[0])) != len(rows[0]):
                errors.append(f'{path}: missing or duplicate CSV fields')
            elif any(len(row) != len(rows[0]) for row in rows[1:]):
                errors.append(f'{path}: inconsistent CSV widths')
    return errors, len(skill_files)


def main():
    errors, count = validate()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f'PASS: {count} independent skills; local links, UI invocations and CSV schemas checked.')


if __name__ == '__main__':
    main()
