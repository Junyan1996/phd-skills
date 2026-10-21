#!/usr/bin/env python3
"""Create isolated research state or inspect a selected task without modifying it.

Python standard library only. This tool does not run analyses or evaluate completion.
"""
import argparse
from collections import deque
from itertools import islice
import json
from pathlib import Path
import re

FILES = ('task_plan.md', 'findings.md', 'progress.md')
ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def project_root(value):
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Project root must be an existing directory')
    return root


def task_id(value):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value) or len(value) > 64:
        raise ValueError('Task ID must be 1-64 lowercase letters/digits with internal hyphens')
    return value


def contained(path, root):
    cursor = root
    for part in path.relative_to(root).parts:
        cursor = cursor / part
        if cursor.is_symlink() or getattr(cursor, 'is_junction', lambda: False)():
            raise ValueError(f'Refusing linked state path: {cursor}')
    path.resolve().relative_to(root)
    return path


def initialize(project, identifier, title):
    root = project_root(project)
    identifier = task_id(identifier)
    if not title.strip() or len(title) > 200 or any(c in title for c in '\r\n\0'):
        raise ValueError('Title must be a nonempty single line of at most 200 characters')
    directory = contained(root / '.phd-workflow' / identifier, root)
    if directory.exists():
        raise FileExistsError(f'Existing task preserved; resume instead: {directory}')
    templates = {name: (ASSETS / name).read_text(encoding='utf-8') for name in FILES}
    directory.parent.mkdir(exist_ok=True)
    directory.mkdir(exist_ok=False)  # One initializer wins; no existing task is overwritten.
    for name, template in templates.items():
        with (directory / name).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(template.replace('{{TITLE}}', title).replace('{{TASK_ID}}', identifier))
    return directory


def select_task(project, identifier=None):
    root = project_root(project)
    parent = contained(root / '.phd-workflow', root)
    if identifier is not None:
        selected = contained(parent / task_id(identifier), root)
        if not selected.is_dir() or not contained(selected / 'task_plan.md', root).is_file():
            raise FileNotFoundError(f'Selected task is missing its plan: {selected}')
        return selected
    if parent.exists() and not parent.is_dir():
        raise ValueError('The .phd-workflow path must be a directory')
    named = sorted(contained(p, root) for p in parent.iterdir() if p.is_dir()) if parent.exists() else []
    if len(named) > 1:
        raise ValueError('Multiple tasks; specify --task-id: ' + ', '.join(p.name for p in named))
    if named:
        return select_task(root, named[0].name)
    if any(contained(root / name, root).is_file() for name in ('task_plan.md', 'status.md')):
        return root
    raise FileNotFoundError('No task state found; select a task or initialize a new one')


def inspect_task(project, identifier=None, max_lines=60):
    if not 1 <= max_lines <= 500:
        raise ValueError('--max-lines must be between 1 and 500')
    root = project_root(project)
    directory = select_task(root, identifier)
    primary = contained(directory / 'task_plan.md', root)
    names = FILES if primary.is_file() else ('status.md',)
    result = {'directory': str(directory), 'mode': 'tracked' if len(names) == 3 else 'light', 'files': {}}
    for name in names:
        path = contained(directory / name, root)
        item = {'path': str(path), 'exists': path.is_file()}
        if item['exists']:
            item['bytes'] = path.stat().st_size
            if name != 'findings.md':
                limit = min(16, max_lines) if name == 'progress.md' else max_lines
                with path.open(encoding='utf-8') as stream:
                    if name == 'progress.md':
                        lines = deque(stream, maxlen=limit + 1)
                    else:
                        lines = list(islice(stream, limit + 1))
                lines = list(lines)
                item['truncated'] = len(lines) > limit
                preview = lines[-limit:] if name == 'progress.md' else lines[:limit]
                item['preview_kind'] = 'tail' if name == 'progress.md' else 'head'
                item['preview'] = ''.join(preview)
        result['files'][name] = item
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    new = commands.add_parser('init', help='Create a new named task without overwriting existing work')
    new.add_argument('--project-root', required=True)
    new.add_argument('--task-id', required=True)
    new.add_argument('--title', required=True)
    show = commands.add_parser('show', help='Inspect selected state with bounded previews')
    show.add_argument('--project-root', required=True)
    show.add_argument('--task-id')
    show.add_argument('--max-lines', type=int, default=60)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            directory = initialize(args.project_root, args.task_id, args.title)
            result = {'directory': str(directory), 'created': list(FILES), 'research_steps_executed': False}
        else:
            result = inspect_task(args.project_root, args.task_id, args.max_lines)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
