"""Behavioral checks for installing and initializing without data loss."""
import importlib.util
from contextlib import contextmanager
from pathlib import Path
import shutil
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def temporary_workspace():
    # Keep test writes in the checkout; normal inherited ACLs work in Windows sandboxes.
    base = (ROOT / '.build' / 'tests').resolve()
    base.mkdir(parents=True, exist_ok=True)
    path = base / uuid.uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        resolved = path.resolve()
        if resolved.parent != base or path.is_symlink():
            raise RuntimeError('Refusing to clean an unexpected test path')
        shutil.rmtree(resolved)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('installer', ROOT / 'scripts' / 'install.py')
initializer = load('initializer', ROOT / 'skills' / 'phd-proposal' / 'scripts' / 'init_project.py')
validator = load('validator', ROOT / 'scripts' / 'validate.py')


class PackageTools(unittest.TestCase):
    def test_individual_install_is_complete(self):
        with temporary_workspace() as folder:
            installer.install(['phd-proposal'], folder)
            installed = Path(folder) / 'phd-proposal'
            self.assertEqual((installed / 'SKILL.md').read_bytes(),
                             (ROOT / 'skills' / 'phd-proposal' / 'SKILL.md').read_bytes())
            self.assertTrue((installed / 'references' / 't2t.md').is_file())
            self.assertTrue((installed / 'assets' / 'evidence-matrix.csv').is_file())

    def test_conflict_blocks_entire_install_and_preserves_files(self):
        with temporary_workspace() as folder:
            existing = Path(folder) / 'phd-writing'
            existing.mkdir()
            sentinel = existing / 'SKILL.md'
            sentinel.write_text('my existing skill', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                installer.install(['phd-proposal', 'phd-writing'], folder)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'my existing skill')
            self.assertFalse((Path(folder) / 'phd-proposal').exists())

    def test_dry_run_does_not_create_destination(self):
        with temporary_workspace() as folder:
            destination = Path(folder) / 'new'
            targets = installer.install(['phd-proposal'], destination, dry_run=True)
            self.assertEqual(len(targets), 1)
            self.assertFalse(destination.exists())

    def test_unknown_skill_rejected_before_writing(self):
        with temporary_workspace() as folder:
            destination = Path(folder) / 'new'
            with self.assertRaises(ValueError):
                installer.install(['../bad'], destination)
            self.assertFalse(destination.exists())

    def test_all_skills_can_install(self):
        with temporary_workspace() as folder:
            names = list(installer.available())
            installer.install(names, folder)
            self.assertEqual(sorted(p.name for p in Path(folder).iterdir()), sorted(names))

    def test_initialize_creates_only_blank_templates(self):
        with temporary_workspace() as folder:
            result = initializer.initialize(Path(folder) / 'proposal')
            expected = {p.name: p.read_bytes() for p in initializer.ASSETS.iterdir() if p.is_file()}
            self.assertEqual({p.name: p.read_bytes() for p in result.iterdir()}, expected)

    def test_initialize_refuses_existing_workspace(self):
        with temporary_workspace() as folder:
            path = Path(folder) / 'proposal'
            initializer.initialize(path)
            status = path / 'status.md'
            status.write_text('completed work', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                initializer.initialize(path)
            self.assertEqual(status.read_text(encoding='utf-8'), 'completed work')

    def test_collection_resource_integrity(self):
        errors, count = validator.validate()
        self.assertGreater(count, 0)
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
