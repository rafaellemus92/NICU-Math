"""Synthetic, no-network smoke coverage. Run: python -m unittest discover -s tests -v."""
import os
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch, Mock

os.environ['NICU_OFFLINE'] = '1'
os.environ.pop('OPENAI_API_KEY', None)
os.environ.pop('NICU_OPENAI_KEY', None)

from fastapi.testclient import TestClient
from api.app.main import app


class OfflineAPI(unittest.TestCase):
    def setUp(self):
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden'))
        self.network.start()
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.network.stop()

    def test_homepage_scope_and_resource_links(self):
        from html.parser import HTMLParser

        class PageParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links = []
                self.references = []
                self.tags = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                self.tags.append(tag)
                if tag == 'a':
                    self.links.append(attrs.get('href'))
                # Every attribute that can fetch a resource, on any tag.
                for name in ('href', 'src', 'srcset', 'action', 'data', 'poster', 'formaction'):
                    if attrs.get(name) is not None:
                        self.references.append(attrs[name])

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers['content-type'])
        parser = PageParser()
        parser.feed(response.text)
        self.assertEqual(set(parser.links), {'#content', '/docs', '/healthz'})
        self.assertEqual(set(parser.references), {'#content', '/docs', '/healthz'})
        self.assertEqual(parser.tags.count('h1'), 1)
        self.assertFalse({'form', 'input', 'iframe', 'script', 'link', 'img', 'object', 'embed',
                          'video', 'audio', 'source', 'base', 'meta-refresh'} & set(parser.tags))
        # No external asset anywhere, including inline CSS (@import, url()) and absolute URLs in text.
        self.assertNotIn('://', response.text)
        self.assertNotIn('@import', response.text)
        self.assertNotIn('url(', response.text)
        for text in ['NICU-Math', 'Offline mode', 'Synthetic research and education only',
                     'Do not enter patient data', 'unvalidated',
                     'loads its script and stylesheet from a public CDN',
                     'two-compartment passive-emptying model', 'this API does not serve it',
                     'Streamlit research interface runs separately and is not hosted at this endpoint']:
            self.assertIn(text, response.text)
        self.assertEqual(self.client.get('/docs').status_code, 200)
        self.assertEqual(self.client.get('/healthz').status_code, 200)

    def test_homepage_evidence_mode_copy(self):
        from api.app.homepage import render_homepage
        offline, evidence = render_homepage(True), render_homepage(False)
        for page in (offline, evidence):
            self.assertNotIn('{{', page)
            self.assertNotIn('://', page)
            self.assertEqual(page.count('<h1>'), 1)
        self.assertIn('Offline mode', offline)
        self.assertNotIn('Offline mode', evidence)
        self.assertIn('Evidence mode · unvalidated', evidence)
        self.assertIn('Legacy evidence services are enabled but not integration-validated.', evidence)
        self.assertIn('Evidence search and generated answers are disabled in this mode.', offline)

    def test_compatibility_entrypoint(self):
        from main import app as compatibility_app
        self.assertIs(compatibility_app, app)

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
            "guard.start(); import api.app.main as main, sys; "
            "assert main.OFFLINE; assert 'openai' not in sys.modules; "
            "assert 'psycopg' not in sys.modules"],
            env=settings, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)


class StreamlitSmoke(unittest.TestCase):
    def test_evidence_sources_keep_excerpt_without_unserved_pdf_link(self):
        from streamlit.testing.v1 import AppTest
        import requests
        response = Mock()
        response.json.return_value = {
            'answer_markdown': 'Synthetic answer',
            'sources': [{'title': 'Synthetic source', 'path': '/library/example.pdf',
                         'excerpt': 'Synthetic excerpt', 'score': 0.5}],
        }
        with patch.object(requests.Session, 'get', side_effect=requests.ConnectionError('offline test')), \
             patch.object(requests.Session, 'post', return_value=response), \
             patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
            page = AppTest.from_file('ui/app.py').run(timeout=15)
            page.text_input[0].set_value('Synthetic question')
            next(button for button in page.button if button.label == 'Search & Answer').click().run()
            self.assertEqual(len(page.exception), 0)
            rendered = '\n'.join(item.value for item in page.markdown)
            self.assertIn('Synthetic excerpt', rendered)
            self.assertNotIn('/files/', rendered)
            self.assertNotIn('Open PDF', rendered)

    def test_initial_render_and_failed_scenario(self):
        from streamlit.testing.v1 import AppTest
        import requests
        # Exercise the real UI with an unavailable API; no outbound requests.
        with patch.object(requests.Session, 'get', side_effect=requests.ConnectionError('offline test')), \
             patch.object(requests.Session, 'post', side_effect=requests.ConnectionError('offline test')), \
             patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
            page = AppTest.from_file('ui/app.py').run(timeout=15)
            self.assertEqual(len(page.exception), 0)
            self.assertIn('Synthetic research', page.warning[0].value)
            next(button for button in page.button if button.label == 'Run').click().run()
            self.assertEqual(len(page.exception), 0)
            self.assertTrue(any('offline test' in error.value for error in page.error))


if __name__ == '__main__':
    unittest.main()
