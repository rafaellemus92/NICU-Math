"""Run after installing requirements.txt; offline-only installs skip these checks."""
import importlib.util
from importlib.metadata import requires, version
import io
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from packaging.requirements import Requirement


@unittest.skipUnless(importlib.util.find_spec('pdfplumber') and importlib.util.find_spec('fitz'),
                     'Optional PDF dependencies are not installed')
class OptionalPDFSmoke(unittest.TestCase):
    def test_pdf_pins_match_installed_dependency_contract(self):
        requirements = Path('requirements.txt').read_text().splitlines()
        for line in requirements:
            if line.startswith(('pdfplumber==', 'pdfminer.six==')):
                req = Requirement(line)
                self.assertIn(version(req.name), req.specifier, f'Install current {line}')
        dependency = next(Requirement(line) for line in requires('pdfplumber')
                          if Requirement(line).name == 'pdfminer.six')
        self.assertIn(version('pdfminer.six'), dependency.specifier)

    def test_in_memory_synthetic_pdf_text_extraction(self):
        import fitz
        import pdfplumber
        with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
            with fitz.open() as document:
                page = document.new_page()
                page.insert_text((72, 72), 'Synthetic research fixture')
                data = document.tobytes()
            with pdfplumber.open(io.BytesIO(data)) as document:
                self.assertEqual(document.pages[0].extract_text(), 'Synthetic research fixture')
