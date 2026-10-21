"""Research state selection and initialization must preserve task identity and work."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
from pathlib import Path
import unittest

from test_tools import temporary_workspace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('workflow_state', ROOT / 'skills/phd-workflow/scripts/state.py')
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class WorkflowState(unittest.TestCase):
    def test_initialization_keeps_templates_in_project(self):
        with temporary_workspace() as project:
            directory = state.initialize(project, 'goat-proposal', '山羊开题')
            self.assertEqual(directory, project / '.phd-workflow/goat-proposal')
            self.assertEqual({p.name for p in directory.iterdir()}, set(state.FILES))
            self.assertIn('山羊开题', (directory / 'task_plan.md').read_text(encoding='utf-8'))

    def test_reinitialize_never_overwrites_research_notes(self):
        with temporary_workspace() as project:
            directory = state.initialize(project, 'goat', '山羊')
            note = directory / 'findings.md'
            note.write_text('S1: verified evidence', encoding='utf-8')
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            with self.assertRaises(FileExistsError):
                state.initialize(project, 'goat', 'another task')
            self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_invalid_ids_cannot_escape_project(self):
        with temporary_workspace() as project:
            for identifier in ('../outside', '/outside', 'a/b', 'a\\b', '.', 'a--b'):
                with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                    state.initialize(project, identifier, 'task')
            self.assertFalse((project / '.phd-workflow').exists())

    def test_explicit_missing_task_never_falls_back(self):
        with temporary_workspace() as project:
            (project / 'status.md').write_text('unrelated root state', encoding='utf-8')
            state.initialize(project, 'present', 'Present')
            with self.assertRaises(FileNotFoundError):
                state.select_task(project, 'missing')

    def test_multiple_tasks_are_ambiguous_even_with_root_status(self):
        with temporary_workspace() as project:
            (project / 'status.md').write_text('root task', encoding='utf-8')
            state.initialize(project, 'first', 'First')
            state.initialize(project, 'second', 'Second')
            with self.assertRaisesRegex(ValueError, 'Multiple tasks'):
                state.select_task(project)
            self.assertEqual(state.select_task(project, 'first').name, 'first')

    def test_legacy_status_is_read_without_migration_or_writes(self):
        with temporary_workspace() as project:
            path = project / 'status.md'
            path.write_text('已有工作\n下一步', encoding='utf-8')
            before = path.read_bytes()
            result = state.inspect_task(project)
            self.assertEqual(result['mode'], 'light')
            self.assertEqual(result['files']['status.md']['preview'], '已有工作\n下一步')
            self.assertEqual(path.read_bytes(), before)
            self.assertFalse((project / '.phd-workflow').exists())

    def test_legacy_three_file_plan_is_reused(self):
        with temporary_workspace() as project:
            (project / 'task_plan.md').write_text('existing plan', encoding='utf-8')
            result = state.inspect_task(project)
            self.assertEqual(result['directory'], str(project))
            self.assertFalse(result['files']['progress.md']['exists'])
            self.assertFalse((project / 'progress.md').exists())

    def test_preview_is_bounded_and_findings_are_not_dumped(self):
        with temporary_workspace() as project:
            directory = state.initialize(project, 'task', 'Task')
            (directory / 'task_plan.md').write_text(''.join(f'P{i}\n' for i in range(100)), encoding='utf-8')
            (directory / 'progress.md').write_text(''.join(f'L{i}\n' for i in range(100)), encoding='utf-8')
            (directory / 'findings.md').write_text('large evidence body', encoding='utf-8')
            files = state.inspect_task(project, 'task', 5)['files']
            self.assertEqual(files['task_plan.md']['preview'], 'P0\nP1\nP2\nP3\nP4\n')
            self.assertEqual(files['progress.md']['preview'], 'L95\nL96\nL97\nL98\nL99\n')
            self.assertTrue(files['task_plan.md']['truncated'])
            self.assertNotIn('preview', files['findings.md'])

    def test_concurrent_initializers_do_not_mix_two_tasks(self):
        with temporary_workspace() as project:
            def attempt(title):
                try:
                    state.initialize(project, 'shared', title)
                    return title
                except FileExistsError:
                    return None
            with ThreadPoolExecutor(max_workers=2) as pool:
                winners = [v for v in pool.map(attempt, ('First', 'Second')) if v]
            self.assertEqual(len(winners), 1)
            for path in (project / '.phd-workflow/shared').iterdir():
                self.assertIn(winners[0], path.read_text(encoding='utf-8'))

    def test_linked_state_outside_project_is_refused(self):
        with temporary_workspace() as project, temporary_workspace() as outside:
            try:
                (project / '.phd-workflow').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('This host does not permit directory symlink creation')
            with self.assertRaises(ValueError):
                state.initialize(project, 'escape', 'Escape')
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
