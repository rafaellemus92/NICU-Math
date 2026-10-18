"""Synthetic, no-network smoke coverage. Run: python -m unittest discover -s tests -v."""
import os
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch

os.environ['NICU_OFFLINE'] = '1'
os.environ.pop('OPENAI_API_KEY', None)
os.environ.pop('NICU_OPENAI_KEY', None)

from fastapi.testclient import TestClient
from main import app


class OfflineAPI(unittest.TestCase):
    def setUp(self):
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden'))
        self.network.start()
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.network.stop()

    def test_health_and_disabled_evidence(self):
        self.assertEqual(self.client.get('/healthz').json(), {'status': 'ok', 'mode': 'offline'})
        for path in ['/search', '/answer']:
            with self.subTest(path=path):
                self.assertEqual(self.client.post(path, json={'query': 'synthetic example'}).status_code, 503)
        self.assertEqual(self.client.get('/files/example.pdf').status_code, 404)

    def test_seeded_scenarios_and_probability_invariants(self):
        for path in ['/scenario', '/scenario/nec', '/scenario/extubation']:
            with self.subTest(path=path):
                payload = {'question': 'Synthetic demonstration', 'inputs': {}, 'n_samples': 1000, 'seed': 42, 'return_samples': True}
                response = self.client.post(path, json=payload)
                self.assertEqual(response.status_code, 200)
                result = response.json()
                self.assertEqual(result, self.client.post(path, json=payload).json())
                self.assertEqual(sum(result['hist_counts']), 1000)
                self.assertEqual(len(result['hist_bins']), len(result['hist_counts']) + 1)
                self.assertTrue(all(0 <= v <= 1 for v in result['summary'].values()))
                self.assertLessEqual(result['summary']['p05'], result['summary']['p50'])
                self.assertLessEqual(result['summary']['p50'], result['summary']['p95'])
                self.assertEqual(len(result['samples_preview']), 100)
                self.assertEqual(result['assumptions']['validation_status'], 'unvalidated toy model')

    def test_sample_limits_and_missing_fields(self):
        for n in [99, 20001]:
            self.assertEqual(self.client.post('/scenario', json={'question': 'synthetic', 'inputs': {}, 'n_samples': n}).status_code, 422)
        self.assertEqual(self.client.post('/scenario', json={}).status_code, 422)


class DefaultModeSmoke(unittest.TestCase):
    def test_default_ignores_dummy_credential_and_does_not_import_services(self):
        settings = os.environ.copy()
        settings.pop('NICU_OFFLINE', None)
        settings['OPENAI_API_KEY'] = 'synthetic-not-a-credential'
        result = subprocess.run([sys.executable, '-c',
            "import socket; from unittest.mock import patch; "
            "guard = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')); "
            "guard.start(); import main, sys; "
            "assert main.OFFLINE; assert 'openai' not in sys.modules; "
            "assert 'psycopg' not in sys.modules"],
            env=settings, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)


class StreamlitSmoke(unittest.TestCase):
    def test_initial_render_and_failed_scenario(self):
        from streamlit.testing.v1 import AppTest
        import requests
        # Exercise the real UI with an unavailable API; no outbound requests.
        with patch.object(requests.Session, 'get', side_effect=requests.ConnectionError('offline test')), \
             patch.object(requests.Session, 'post', side_effect=requests.ConnectionError('offline test')), \
             patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
            page = AppTest.from_file('app.py').run(timeout=15)
            self.assertEqual(len(page.exception), 0)
            self.assertIn('Synthetic research', page.warning[0].value)
            next(button for button in page.button if button.label == 'Run').click().run()
            self.assertEqual(len(page.exception), 0)
            self.assertTrue(any('offline test' in error.value for error in page.error))


if __name__ == '__main__':
    unittest.main()
