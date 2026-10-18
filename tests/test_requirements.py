"""The hosting manifest must stay flat and match both service manifests."""
from pathlib import Path
import unittest


def requirements(path):
    result = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('-r '):
            result.update(requirements(path.parent / line[3:]))
        else:
            result.add(line)
    return result


class RequirementsManifest(unittest.TestCase):
    def test_root_is_flat_and_matches_service_requirements(self):
        root = Path('requirements.txt')
        self.assertFalse(any(line.strip().startswith('-') for line in root.read_text().splitlines()))
        expected = requirements(Path('api/requirements.txt')) | requirements(Path('ui/requirements.txt'))
        self.assertEqual(requirements(root), expected)
