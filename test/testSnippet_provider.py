from unittest import TestCase

import homology.snippet_provider as sp


class TestSnippetProvider(TestCase):
    def test_basic(self):
        provider = sp.SnippetProvider()

        self.assertEqual(provider['for'], "for # in !:\n\tpass")
        self.assertEqual(provider['i==5'], "i==5")
